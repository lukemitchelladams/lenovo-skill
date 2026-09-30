"""Rebuild the DCSC knowledge base from your DCSC exports.
Run this after any DCSC work session:   python refresh.py <folder> [<folder> ...]
Folders are forwarded to scan_dcsc.py (else env LENOVO_DCSC_DIRS, else ~/Downloads and ~/Desktop).
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONIOENCODING="utf-8")
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass
for step in (["scan_dcsc.py"] + sys.argv[1:], ["build_kb.py"], ["fix_mtm.py"], ["build_kb_index.py", "--facts-only"]):
    print(f"\n>>> {' '.join(step)}")
    r = subprocess.run([sys.executable, os.path.join(HERE, step[0])] + step[1:], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env)
    print(r.stdout[-3000:])
    if r.returncode:
        print("STDERR:", r.stderr[-1500:])
        sys.exit(f"\n{step[0]} FAILED (exit {r.returncode}) - knowledge base NOT refreshed")
print("\ndone. query with:  python kb.py configs   (also: fact, docs, part, tce)")
