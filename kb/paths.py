"""Single place for path resolution. Override with env vars, no edits needed.

LENOVO_KB_DB      sqlite file       (default: kb/dcsc_kb.sqlite)
LENOVO_DOCS_DIR   Lenovo Press docs (default: <repo>/docs/lenovo-press)
"""
import os

KB_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(KB_DIR)

DB = os.path.abspath(os.path.expanduser(
    os.environ.get("LENOVO_KB_DB") or os.path.join(KB_DIR, "dcsc_kb.sqlite")))
DOCS_DIR = os.path.abspath(os.path.expanduser(
    os.environ.get("LENOVO_DOCS_DIR") or os.path.join(REPO_DIR, "docs", "lenovo-press")))

PDF_DIR = os.path.join(DOCS_DIR, "pdf")
HTML_DIR = os.path.join(DOCS_DIR, "html")
INDEX_CSV = os.path.join(DOCS_DIR, "INDEX.csv")
