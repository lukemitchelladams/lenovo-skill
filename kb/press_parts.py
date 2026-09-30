#!/usr/bin/env python3
'''Part tables of the Lenovo Press product guides -> sqlite table press_part.

Every "Part number | Feature code | Description | Top Choice Express ..." row of every guide, with the
guide's own TCE column and the page it sits on (page = the number `kb.py page <lp> <n>` prints).
Sources per id, first hit wins: pdf/<id>.pdf (pymupdf table finder), html/<id>.html, pages/<id>.txt
(crawler output, tables kept as "| cell | cell |" rows).

  press_part(lp, platform, pn, fc, descr, tce, page, tbl)
    platform  model named in the doc title; a multi-model TCE header ('HX650 V4' | 'HX650 V4 Storage')
              gets one row per model
    pn        part number as the guide prints it ('CTO only', 'None'); '' when the table has no PN column
    tce       'TCE' | 'Not TCE' | ''  ('' = that table has no TCE column)
    page      PDF page, or crawled-page chunk; 0 for html
    tbl       table caption / group heading

usage:
  python press_parts.py [parts] <platform|lpNNNN> <regex>   rows of that guide (regex on fc, pn, description)
  python press_parts.py [parts] --fc <FC>                   every guide + platform a feature code is in, with its TCE column
  python press_parts.py build [--force]                     (re)extract from the local docs (also: build_kb_index.py --parts-only)
platform is a substring of the model, spaces ignored: SR630, "SR630 V4", sr630v4, HX650. Quote multi-word args.
The guide's TCE column is a snapshot: TCE membership rotates per MTM per date, only a DCSC BU1E config proves it.
'''
import contextlib, csv, glob, io, os, pathlib, re, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from paths import DB, DOCS_DIR, PDF_DIR, HTML_DIR, INDEX_CSV, REPO_DIR

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PAGES_DIR = os.path.join(DOCS_DIR, 'pages')
VERSION = 1  # bump when extraction changes: invalidates the per-document cache

SCHEMA = '''
CREATE TABLE IF NOT EXISTS press_part(
  lp TEXT NOT NULL, platform TEXT NOT NULL, pn TEXT NOT NULL, fc TEXT NOT NULL,
  descr TEXT NOT NULL, tce TEXT NOT NULL, page INTEGER NOT NULL, tbl TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS press_part_fc ON press_part(fc);
CREATE INDEX IF NOT EXISTS press_part_lp ON press_part(lp);
CREATE TABLE IF NOT EXISTS press_part_src(lp TEXT PRIMARY KEY, sig TEXT NOT NULL);
'''

# --------------------------------------------------------------- cell classifiers
PN = re.compile(r'^(?=[0-9A-Z]*\d)[0-9A-Z]{7,10}$')      # 4XB7A93140, 4Y37A09730, 7S02003GWW, 00YK026
FC = re.compile(r'^[0-9A-Z]{4}$')                         # C286, B8NZ, 2302
NOPN = re.compile(r'^(CTO only|None|N/A|-)\*?$', re.I)
TCEV = re.compile(r'^(Not\s+TCE|TCE)\W*$', re.I)
H_FC = re.compile(r'^feature(\s*codes?)?$', re.I)
H_PN = re.compile(r'^part(\s*numbers?)?$', re.I)
H_TCE = re.compile(r'^top\s*choice(\s*express)?$|^tce$', re.I)
H_DESC = re.compile(r'^(product\s+|option\s+)?description', re.I)
CAP = re.compile(r'Table\s+\d+\.[^\n]*')
MODEL = re.compile(r'\b((?:SR|ST|SE|SD|SN|HX|VX|MX|FX|HS|DM|DE|DG|DS)\d{2,4}[A-Za-z]?|D\d{4})\b(?:\s+(V\d)\b)?')


def cl(s):
    '''one line, single spaces, private-use icon glyphs dropped'''
    return re.sub(r'\s+', ' ', re.sub('[-]', ' ', s or '')).strip()


def toks(cell):
    return [t for t in re.split(r'[\s,;/]+', cell.rstrip('*')) if t]


def tce_norm(v):
    return 'Not TCE' if re.match(r'not', v, re.I) else 'TCE'


def platform_of(title):
    m = MODEL.search(title or '')
    if m:
        return m.group(1) + (' ' + m.group(2) if m.group(2) else '')
    return re.sub(r'^(Lenovo\s+)?(ThinkSystem|ThinkAgile|ThinkEdge)\s+', '', (title or '').strip())[:50]


def doc_titles():
    out = {}
    for f_ in (INDEX_CSV, os.path.join(PAGES_DIR, 'INDEX.csv')):
        if os.path.exists(f_):
            with open(f_, newline='', encoding='utf-8-sig') as f:
                for r in csv.DictReader(f):
                    out.setdefault(r['id'], r['title'])
    return out


# --------------------------------------------------------------- grid -> rows
def header_map(g, hi):
    '''Column map from the header row g[hi]; None when it is not a part-table header.'''
    h = g[hi]
    fi = next((k for k, c in enumerate(h) if H_FC.match(c)), None)
    pi = next((k for k, c in enumerate(h) if H_PN.match(c)), None)
    di = next((k for k, c in enumerate(h) if H_DESC.match(c)), None)
    if fi is None or (pi is None and di is None):
        return None
    tj = next((k for k, c in enumerate(h) if H_TCE.match(c)), None)
    te = next((k for k in range(tj + 1, len(h)) if h[k]), len(h)) if tj is not None else None
    return dict(has_pn=pi is not None, d=di, tj=tj, te=te, variants=[], ncols=len(h), blind=False,
                multi_fc=sum(1 for c in h if H_FC.match(c)) > 1)


def data_like(c):
    v = c.rstrip('*')
    return bool(PN.match(v) or NOPN.match(v) or FC.match(v) or TCEV.match(v))


def is_fc(v):
    ts = toks(v)
    return bool(ts) and all(FC.match(t) for t in ts)


def find_pf(cells, has_pn, multi_fc=False):
    '''(pn list, fc list, index of the last fc cell) for a data row, None for headings/notes.
    multi_fc: tables with several feature-code columns (riser slot variants) contribute every one.'''
    ne = [(k, v) for k, v in enumerate(cells) if v]
    if not ne:
        return None
    if not has_pn:
        ts = toks(ne[0][1])
        return ([''] * len(ts), ts, ne[0][0]) if ts and all(FC.match(t) for t in ts) and len(ne) > 1 else None
    for x, (k, v) in enumerate(ne):
        vv = v.rstrip('*')
        if NOPN.match(vv):
            pns = [vv]
        else:
            pns = toks(vv)
            if not pns or not all(PN.match(t) for t in pns):
                continue
        if x + 1 >= len(ne) or not is_fc(ne[x + 1][1]):
            return None
        k2, fcs = ne[x + 1][0], toks(ne[x + 1][1])
        y = x + 2
        while multi_fc and y < len(ne) and is_fc(ne[y][1]):
            k2, fcs = ne[y][0], fcs + toks(ne[y][1])
            y += 1
        if len(pns) == len(fcs):
            return pns, fcs, k2
        if len(pns) == 1:
            return pns * len(fcs), fcs, k2
        if len(fcs) == 1:
            return pns, fcs * len(pns), k2
        return None
    return None


def parse_grid(raw, plat, page, cap, carry):
    '''raw: list of rows of cell strings. page: int, or one int per row. Returns (rows, carry, caption).
    A row is (platform, pn, fc, descr, tce, page, tbl). carry lets a header-less continuation reuse the map.'''
    g = [[cl(c) for c in r] for r in raw]
    w = max((len(r) for r in g), default=0)
    g = [r + [''] * (w - len(r)) for r in g]
    pg = (lambda i: page[i]) if isinstance(page, list) else (lambda i: page)
    for i in range(min(6, len(g))):
        if any(H_FC.match(c) for c in g[i]):
            m = header_map(g, i)
            if m:
                caps = CAP.findall(' '.join(c for r in raw[:i] for c in r if c))
                if caps:
                    cap = cl(caps[-1])
                out, m = read_rows(g, m, i + 1, plat, pg, cap, True)
                return out, m, cap
    # no header row: a continuation of the previous table, or the finder merged the header into a text
    # blob. Try the carried column map first, then read the rows by content alone.
    tries = []
    if carry and carry['ncols'] == w:
        tries.append(dict(carry, variants=list(carry['variants'])))
    if w >= 3:
        tries.append(dict(has_pn=True, d=None, tj=0, te=w, variants=[], ncols=w, blind=True, multi_fc=True))
    for m in tries:
        out, m = read_rows(g, m, 0, plat, pg, cap, False)
        if out:
            return out, m, cap
    return [], None, cap


def read_rows(g, m, start, plat, pg, cap, has_header):
    if has_header and m['tj'] is not None and start < len(g):
        sub = g[start]
        span = range(m['tj'], m['te'])
        if not any(data_like(c) for c in sub) and any(sub[k] for k in span):
            m['variants'] = [sub[k] for k in span if sub[k]]
            start += 1
    var = m['variants']
    plats = [plat]
    if len(var) > 1:
        plats = [v if MODEL.search(v) else (plat + ' ' + v).strip() for v in var]
    out, sect = [], ''
    for i in range(start, len(g)):
        r = g[i]
        ne = [c for c in r if c]
        if not ne or any(H_FC.match(c) for c in r):
            continue
        pf = find_pf(r, m['has_pn'], m['multi_fc'])
        if pf is None:
            if len(ne) == 1 and not data_like(ne[0]) and len(ne[0]) < 160:
                sect = ne[0]
            continue
        pns, fcs, fk = pf
        dsc = r[m['d']] if m['d'] is not None and m['d'] < len(r) else ''
        if not dsc:
            dsc = next((c for k, c in enumerate(r) if k > fk and c and ' ' in c and len(c) >= 8
                        and not TCEV.match(c)), '')
        tv = []
        if m['tj'] is not None:
            tv = [tce_norm(r[k]) for k in range(m['tj'], min(m['te'], len(r))) if TCEV.match(r[k])]
            if not tv:
                tv = [tce_norm(c) for c in ne if TCEV.match(c)][:max(1, len(var))]
        pls = plats if len(plats) == 1 or not m['blind'] or len(tv) == len(plats) else plats[:1]
        tbl = (cap + (' / ' + sect if sect else ''))[:160]
        for pn, fc in zip(pns, fcs):
            for j, pl in enumerate(pls):
                out.append((pl, pn, fc, dsc, tv[j] if j < len(tv) else '', pg(i), tbl))
    m['variants'] = var
    return out, m


# --------------------------------------------------------------- sources
def pdf_rows(path, plat):
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            raise RuntimeError('PyMuPDF missing (pip install pymupdf)')
    d = fitz.open(path)
    if not hasattr(d[0] if len(d) else None, 'find_tables'):
        raise RuntimeError('PyMuPDF too old for find_tables (need >= 1.23)')
    hdr = re.compile(r'^\s*Feature(\s+codes?)?\s*$|Feature code|Part\s*number', re.M | re.I)
    out, carry, cap = [], None, ''
    for pno in range(len(d)):
        pg = d[pno]
        txt = pg.get_text()
        if not (hdr.search(txt) or (carry and re.search(r'\b[0-9][0-9A-Z]{6,9}\b', txt))):
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                tabs = pg.find_tables().tables
                blocks = pg.get_text('blocks')
        except Exception:
            continue
        caps = [(b[3], CAP.search(b[4]).group(0)) for b in blocks if CAP.search(b[4])]
        for tb in tabs:
            above = [c for y, c in caps if y <= tb.bbox[1] + 3]
            rows, carry2, cap2 = parse_grid(tb.extract(), plat, pno + 1, cl(above[-1]) if above else cap, carry)
            if carry2 is not None:
                carry, cap = carry2, cap2
            out += rows
    d.close()
    return out


def text_rows(text, plat, chunked):
    '''Rows from crawler-style text: consecutive "| a | b |" lines are one table, the line above is its caption.'''
    if chunked:
        from build_kb_index import chunk_lines
        lines, ck = chunk_lines(text)
    else:
        lines, ck = text.split('\n'), None
    out, carry, i = [], None, 0
    while i < len(lines):
        if not lines[i].startswith('|'):
            i += 1
            continue
        j = i
        while j < len(lines) and lines[j].startswith('|'):
            j += 1
        raw = [[c for c in ln.strip().strip('|').split('|')] for ln in lines[i:j]]
        c0 = lines[i - 1] if i and lines[i - 1].startswith('Table') else ''
        rows, carry2, cap2 = parse_grid(raw, plat, ck[i:j] if ck else 0, cl(c0), carry)
        carry = carry2
        out += rows
        i = j
    return out


def html_rows(path, plat):
    sys.path.insert(0, os.path.join(REPO_DIR, 'docs'))
    import crawl_lenovo_press as crawl
    raw = open(path, encoding='utf-8', errors='ignore').read()
    return text_rows(crawl.extract(raw)[3], plat, False)


def sources():
    '''{lp: (kind, path)}, pdf > html > pages'''
    src = {}
    for kind, pat in (('pages', os.path.join(PAGES_DIR, '*.txt')), ('html', os.path.join(HTML_DIR, '*.html')),
                      ('pdf', os.path.join(PDF_DIR, '*.pdf'))):
        for p in glob.glob(pat):
            src[os.path.splitext(os.path.basename(p))[0]] = (kind, p)
    return src


def pdf_title(path):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    d = fitz.open(path)
    t = (d.metadata or {}).get('title') or ''
    d.close()
    return t


def extract(lp, kind, path, tt):
    title = tt.get(lp) or (pdf_title(path) if kind == 'pdf' else '')
    plat = platform_of(title) or lp
    if kind == 'pdf':
        rows = pdf_rows(path, plat)
    elif kind == 'html':
        rows = html_rows(path, plat)
    else:
        rows = text_rows(open(path, encoding='utf-8', errors='replace').read(), plat, True)
    seen, out = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def build(cx, force=False):
    '''Fill press_part; documents whose file is unchanged since the last build are kept as they are.'''
    cx.executescript(SCHEMA)
    src, tt = sources(), doc_titles()
    have = dict(cx.execute('SELECT lp, sig FROM press_part_src'))
    for lp in set(have) - set(src):
        cx.execute('DELETE FROM press_part WHERE lp=?', (lp,))
        cx.execute('DELETE FROM press_part_src WHERE lp=?', (lp,))
    docs = 0
    for lp, (kind, path) in sorted(src.items()):
        st = os.stat(path)
        sig = '%d:%s:%d:%d' % (VERSION, kind, st.st_size, int(st.st_mtime))
        if not force and have.get(lp) == sig:
            continue
        try:
            rows = extract(lp, kind, path, tt)
        except Exception as e:
            print('  !! %s: %s' % (lp, e))
            continue
        cx.execute('DELETE FROM press_part WHERE lp=?', (lp,))
        cx.executemany('INSERT INTO press_part VALUES(?,?,?,?,?,?,?,?)', [(lp,) + r for r in rows])
        cx.execute('INSERT OR REPLACE INTO press_part_src VALUES(?,?)', (lp, sig))
        cx.commit()
        docs += 1
        if rows or kind != 'pages':
            print('  %s: %d rows (%s)' % (lp, len(rows), kind))
    print('  %d documents extracted, %d unchanged' % (docs, len(src) - docs))
    return cx.execute('SELECT COUNT(*) FROM press_part').fetchone()[0]


# --------------------------------------------------------------- query
def connect():
    if not os.path.exists(DB):
        sys.exit('No knowledge base at %s\nBuild the part index:  python kb/build_kb_index.py --parts-only' % DB)
    cx = sqlite3.connect(pathlib.Path(DB).as_uri() + '?mode=ro', uri=True)
    if not cx.execute("SELECT 1 FROM sqlite_master WHERE name='press_part'").fetchone():
        sys.exit('No press_part table in the db. Fetch the guides, then:  python kb/build_kb_index.py --parts-only')
    return cx


def key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def cmd_fc(cx, fc):
    rows = cx.execute('SELECT lp, platform, tce, pn, page, descr FROM press_part WHERE fc=? ORDER BY platform, lp, page',
                      (fc.upper(),)).fetchall()
    if not rows:
        print('%s: not in any indexed guide table' % fc.upper())
        return
    print('%s  %s\n' % (fc.upper(), rows[0][5][:90]))
    print('%-7s%-20s%-9s%-13s%s' % ('guide', 'platform', 'TCE', 'part number', 'pages'))
    grp = {}
    for lp, pl, tce, pn, page, _ in rows:
        g = grp.setdefault((lp, pl, tce or '-', pn), [])
        if page and page not in g:
            g.append(page)
    for (lp, pl, tce, pn), pages in grp.items():
        print('%-7s%-20s%-9s%-13s%s' % (lp, pl[:19], tce, pn[:12], ','.join(map(str, pages)) or '-'))
    print('\n(guide TCE column = snapshot at the guide date; only a DCSC BU1E config proves TCE)')


def cmd_parts(cx, sel, rx, limit=200):
    if re.fullmatch(r'lp\d+', sel.lower()):
        where, args = 'lp=?', (sel.lower(),)
        rows = cx.execute('SELECT lp, platform, pn, fc, descr, tce, page, tbl FROM press_part WHERE ' + where +
                          ' ORDER BY rowid', args).fetchall()
    else:
        k = key(sel)
        plats = [p for (p,) in cx.execute('SELECT DISTINCT platform FROM press_part') if k and k in key(p)]
        if not plats:
            sys.exit('no guide platform matches %r. Known: %s' % (sel, ', '.join(sorted(
                p for (p,) in cx.execute('SELECT DISTINCT platform FROM press_part')))[:600]))
        rows = cx.execute('SELECT lp, platform, pn, fc, descr, tce, page, tbl FROM press_part WHERE platform IN (%s) '
                          'ORDER BY lp, rowid' % ','.join('?' * len(plats)), plats).fetchall()
    try:
        r_ = re.compile(rx, re.I)
    except re.error as e:
        sys.exit('bad regex: %s' % e)
    hits = [r for r in rows if r_.search(' '.join((r[3], r[2], r[4])))]
    multi = len({(r[0], r[1]) for r in hits}) > 1
    print('%d of %d rows match /%s/\n' % (len(hits), len(rows), rx))
    for lp, pl, pn, fc, d, tce, page, tbl in hits[:limit]:
        pre = ('%-7s%-18s' % (lp, pl[:17])) if multi else ''
        print('%s%-6s%-13s%-9s%-5s%s' % (pre, fc, pn[:12], tce or '-', 'p%d' % page if page else '-', d[:80]))
    if len(hits) > limit:
        print('... %d more, narrow the regex' % (len(hits) - limit))


def main(argv):
    a = list(argv)
    if a and a[0] == 'parts':
        a = a[1:]
    if a and a[0] in ('-h', '--help', 'help'):
        print(__doc__)
        return
    if a and a[0] == 'build':
        os.makedirs(os.path.dirname(DB), exist_ok=True)
        cx = sqlite3.connect(DB)
        print('%d part rows' % build(cx, '--force' in a))
        cx.close()
        return
    if len(a) >= 2 and a[0] == '--fc':
        cmd_fc(connect(), a[1])
    elif len(a) >= 1 and a[0] != '--fc':
        cmd_parts(connect(), a[0], a[1] if len(a) > 1 else '.')
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
