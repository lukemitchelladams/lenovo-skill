#!/usr/bin/env python3
'''Token-cheap retrieval layer for the /lenovo skill.

Adds two search surfaces to dcsc_kb.sqlite:
  fact / fact_fts - curated hand-verified rules (kb_facts.py). Query these FIRST, they are tiny.
  doc_fts         - page-level full-text index of the Lenovo Press corpus, so we
                    search sentences instead of grepping hundreds of MB of PDF.
                    (fetch the docs first: python docs/get_lenovo_docs.py; needs pymupdf)

Re-runnable; rebuilds from scratch each time.
Usage: python build_kb_index.py [--facts-only|--docs-only]
'''
import os, sqlite3, sys, glob, re, csv
from paths import KB_DIR, DB, DOCS_DIR, PDF_DIR as PDF, HTML_DIR as HTML, INDEX_CSV as IDX

if KB_DIR not in sys.path:
    sys.path.insert(0, KB_DIR)


def norm(s):
    for a, b in ((chr(8217), chr(39)), (chr(8220), chr(34)), (chr(8221), chr(34)),
                 (chr(8211), '-'), (chr(8212), '-'), (chr(160), ' ')):
        s = s.replace(a, b)
    return re.sub(r'[ \t]+', ' ', s)


def titles():
    out = {}
    if os.path.exists(IDX):
        with open(IDX, newline='', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                out[r['id']] = r['title']
    return out


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
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
    except ImportError:
        print('  PyMuPDF missing (pip install pymupdf), skipping doc index')
        return 0
    if not (os.path.isdir(PDF) or os.path.isdir(HTML)):
        print('  no docs under ' + DOCS_DIR + ' - run: python docs/get_lenovo_docs.py')
        return 0
    cx.executescript('''
    DROP TABLE IF EXISTS doc_fts;
    CREATE VIRTUAL TABLE doc_fts USING fts5(lp, title, page UNINDEXED, text);
    ''')
    tt, rows, n = titles(), [], 0
    for path in sorted(glob.glob(os.path.join(PDF, '*.pdf'))):
        lp = os.path.splitext(os.path.basename(path))[0]
        try:
            d = fitz.open(path)
        except Exception as e:
            print('  !! ' + lp + ': ' + str(e))
            continue
        pages = len(d)
        for pno in range(pages):
            t = norm(d[pno].get_text())
            if t.strip():
                rows.append((lp, tt.get(lp, lp), pno + 1, t))
                n += 1
        d.close()
        print('  ' + lp + ': ' + str(pages) + ' pages')
    for path in sorted(glob.glob(os.path.join(HTML, '*'))):
        lp = os.path.splitext(os.path.basename(path))[0]
        try:
            raw = open(path, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        txt = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', raw, flags=re.S | re.I)
        txt = norm(re.sub(r'<[^>]+>', ' ', txt))
        for i in range(0, len(txt), 6000):
            chunk = txt[i:i + 6000]
            if chunk.strip():
                rows.append((lp, tt.get(lp, lp), i // 6000 + 1, chunk))
                n += 1
        print('  ' + lp + ': html')
    cx.executemany('INSERT INTO doc_fts(lp,title,page,text) VALUES(?,?,?,?)', rows)
    return n


if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else ''
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    cx = sqlite3.connect(DB)
    if only != '--docs-only':
        print('Building fact index...')
        print('  ' + str(build_facts(cx)) + ' facts')
    if only != '--facts-only':
        print('Building doc index...')
        print('  ' + str(build_docs(cx)) + ' pages indexed')
    cx.commit()
    cx.execute('PRAGMA optimize')
    cx.close()
    print('Done.')
