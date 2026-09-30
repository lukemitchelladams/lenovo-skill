# Lenovo Press documents

These are Lenovo's copyrighted documents. They are **not** redistributed in this repo (`docs/lenovo-press/` is git-ignored).

Fetch them from lenovopress.lenovo.com for your own personal reference:

    python docs/get_lenovo_docs.py            # downloads 44 documents into docs/lenovo-press (~230 MB)
    python docs/get_lenovo_docs.py --only lp2165   # or just one document

A few references are live-database web pages with no PDF; those are saved as HTML under `docs/lenovo-press/html`. Files already present are skipped unless you pass `--force`. Set `LENOVO_DOCS_DIR` to keep the documents somewhere else.

Then build the page-level full-text index (needs `pip install pymupdf`):

    python kb/build_kb_index.py --docs-only

Search it with `python kb/kb.py docs <query>` and read a full page with `python kb/kb.py page <lp> <page>`.
