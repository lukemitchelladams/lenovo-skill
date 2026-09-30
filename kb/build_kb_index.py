#!/usr/bin/env python3
'''Token-cheap retrieval layer for the /lenovo skill.

Adds three search surfaces to dcsc_kb.sqlite:
  fact / fact_fts - curated hand-verified rules (kb_facts.py). Query these FIRST, they are tiny.
  doc_fts         - page-level full-text index of the Lenovo Press corpus, so we
                    search sentences instead of grepping hundreds of MB of PDF.
                    Sources: pdf/*.pdf (needs pymupdf), html/*.html, and pages/*.txt from
                    docs/crawl_lenovo_press.py (an id that has a PDF or HTML is not indexed twice).
  press_part      - every part-number / feature-code row of the product-guide tables, with the
                    guide's own TCE column (kb/press_parts.py; pdf > html > pages per id).
                    (fetch the docs first: python docs/get_lenovo_docs.py, python docs/crawl_lenovo_press.py)

Re-runnable; facts and doc_fts rebuild from scratch each time, press_part re-extracts only the
documents whose file changed (--force re-extracts everything).
Usage: python build_kb_index.py [--facts-only|--docs-only|--parts-only] [--force]
'''
import os, sqlite3, sys, glob, re, csv
from paths import KB_DIR, DB, DOCS_DIR, PDF_DIR as PDF, HTML_DIR as HTML, INDEX_CSV as IDX

if KB_DIR not in sys.path:
    sys.path.insert(0, KB_DIR)

PAGES = os.path.join(DOCS_DIR, 'pages')
PAGES_IDX = os.path.join(PAGES, 'INDEX.csv')
CHUNK = 6000


def norm(s):
    for a, b in ((chr(8217), chr(39)), (chr(8220), chr(34)), (chr(8221), chr(34)),
                 (chr(8211), '-'), (chr(8212), '-'), (chr(160), ' ')):
        s = s.replace(a, b)
    return re.sub(r'[ \t]+', ' ', s)


def titles():
    out = {}
    for f_ in (IDX, PAGES_IDX):  # get_lenovo_docs titles win, crawled titles fill the rest
        if os.path.exists(f_):
            with open(f_, newline='', encoding='utf-8-sig') as f:
                for r in csv.DictReader(f):
                    out.setdefault(r['id'], r['title'])
    return out


def chunk_lines(text, size=CHUNK):
    '''Normalised lines of a crawled page and each line's 1-based chunk number (whole lines, ~size chars).
    press_parts.py uses the same split so its `page` numbers line up with `kb.py page <lp> <n>`.'''
    lines, out, n, used = norm(text).split('\n'), [], 1, 0
    for ln in lines:
        if used and used + len(ln) + 1 > size:
            n, used = n + 1, 0
        out.append(n)
        used += len(ln) + 1
    return lines, out


def build_facts(cx):
    from kb_facts import FACTS
    cx.executescript('''
    DROP TABLE IF EXISTS fact_fts;
    DROP TABLE IF EXISTS fact;
    CREATE TABLE fact(
      id INTEGER PRIMARY KEY, topic TEXT NOT NULL, scope TEXT NOT NULL,
      status TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL,
      source TEXT NOT NULL, verified TEXT NOT NULL);
    CREATE VIRTUAL TABLE fact_fts USING fts5(
      topic, title, body, scope, source, fact_id UNINDEXED);
    ''')
    cx.executemany('INSERT INTO fact(topic,scope,status,title,body,source,verified)'
                   ' VALUES(?,?,?,?,?,?,?)', FACTS)
    cx.execute('INSERT INTO fact_fts(topic,title,body,scope,source,fact_id)'
               ' SELECT topic,title,body,scope,source,id FROM fact')
    return cx.execute('SELECT COUNT(*) FROM fact').fetchone()[0]


def build_docs(cx):
    fitz = None
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
    except ImportError:
        print('  PyMuPDF missing (pip install pymupdf), skipping PDFs')
    pages = sorted(glob.glob(os.path.join(PAGES, '*.txt')))
    if not (os.path.isdir(PDF) or os.path.isdir(HTML) or pages):
        print('  no docs under ' + DOCS_DIR + ' - run: python docs/get_lenovo_docs.py')
        return 0
    cx.executescript('''
    DROP TABLE IF EXISTS doc_fts;
    CREATE VIRTUAL TABLE doc_fts USING fts5(lp, title, page UNINDEXED, text);
    ''')
    tt, rows, n, seen = titles(), [], 0, set()
    for path in (sorted(glob.glob(os.path.join(PDF, '*.pdf'))) if fitz else []):
        lp = os.path.splitext(os.path.basename(path))[0]
        try:
            d = fitz.open(path)
        except Exception as e:
            print('  !! ' + lp + ': ' + str(e))
            continue
        pages_n = len(d)
        for pno in range(pages_n):
            t = norm(d[pno].get_text())
            if t.strip():
                rows.append((lp, tt.get(lp, lp), pno + 1, t))
                n += 1
        d.close()
        seen.add(lp)
        print('  ' + lp + ': ' + str(pages_n) + ' pages')
    for path in sorted(glob.glob(os.path.join(HTML, '*'))):
        lp = os.path.splitext(os.path.basename(path))[0]
        try:
            raw = open(path, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        txt = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', raw, flags=re.S | re.I)
        txt = norm(re.sub(r'<[^>]+>', ' ', txt))
        for i in range(0, len(txt), CHUNK):
            chunk = txt[i:i + CHUNK]
            if chunk.strip():
                rows.append((lp, tt.get(lp, lp), i // CHUNK + 1, chunk))
                n += 1
        seen.add(lp)
        print('  ' + lp + ': html')
    todo = [p for p in pages if os.path.splitext(os.path.basename(p))[0] not in seen]
    for k, path in enumerate(todo, 1):
        lp = os.path.splitext(os.path.basename(path))[0]
        try:
            lines, ck = chunk_lines(open(path, encoding='utf-8', errors='replace').read())
        except Exception as e:
            print('  !! ' + lp + ': ' + str(e))
            continue
        groups = {}
        for ln, c in zip(lines, ck):
            groups.setdefault(c, []).append(ln)
        for c, g in groups.items():
            chunk = '\n'.join(g)
            if chunk.strip():
                rows.append((lp, tt.get(lp, lp), c, chunk))
                n += 1
        if k % 250 == 0 or k == len(todo):
            print('  crawled pages: ' + str(k) + '/' + str(len(todo)) + ' documents')
    cx.executemany('INSERT INTO doc_fts(lp,title,page,text) VALUES(?,?,?,?)', rows)
    return n


def build_parts(cx, force=False):
    import press_parts
    return press_parts.build(cx, force=force)


if __name__ == '__main__':
    args = sys.argv[1:]
    modes = [a for a in args if a in ('--facts-only', '--docs-only', '--parts-only')]
    bad = [a for a in args if a not in modes and a != '--force']
    if bad or len(modes) > 1:
        sys.exit('usage: python build_kb_index.py [--facts-only|--docs-only|--parts-only] [--force]')
    only = modes[0] if modes else ''
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    cx = sqlite3.connect(DB)
    if only in ('', '--facts-only'):
        print('Building fact index...')
        print('  ' + str(build_facts(cx)) + ' facts')
    if only in ('', '--docs-only'):
        print('Building doc index...')
        print('  ' + str(build_docs(cx)) + ' pages indexed')
    cx.commit()
    if only in ('', '--parts-only'):
        print('Building part-table index...')
        print('  ' + str(build_parts(cx, '--force' in args)) + ' part rows')
    cx.commit()
    cx.execute('PRAGMA optimize')
    cx.close()
    print('Done.')
