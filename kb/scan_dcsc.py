"""Find DCSC configurator exports (.xlsx, or .xlsx inside .zip) and list them in dcsc_files.txt.

usage:
  python scan_dcsc.py <folder> [<folder> ...]
  env LENOVO_DCSC_DIRS=<folder>[<pathsep><folder>...]   used when no folder args are given
  default (no args, no env): ~/Downloads and ~/Desktop
"""
import os, re, sys, zipfile, shutil, pathlib
from paths import KB_DIR

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

args = [a for a in sys.argv[1:] if a]
if args:
    ROOTS = args
elif os.environ.get("LENOVO_DCSC_DIRS"):
    ROOTS = [p for p in os.environ["LENOVO_DCSC_DIRS"].split(os.pathsep) if p]
else:
    home = pathlib.Path.home()
    ROOTS = [str(home / "Downloads"), str(home / "Desktop")]
ROOTS = list(dict.fromkeys(os.path.abspath(os.path.expanduser(r)) for r in ROOTS))

SKIP = {"node_modules", ".git"}
# DCSC exports arrive as .zip. Extract any xlsx inside so those get scanned too.
CACHE = os.path.join(KB_DIR, "_zipcache")
LIST = os.path.join(KB_DIR, "dcsc_files.txt")
ZIP_PREFIX = re.compile(r"^\d{4}_")

found, zips = [], []
for root in ROOTS:
    if not os.path.isdir(root):
        print(f"skipping (not a folder): {root}")
        continue
    for dirpath, dirs, files in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        parts = [] if rel == "." else rel.split(os.sep)
        if SKIP.intersection(parts) or dirpath.startswith(CACHE) or len(parts) > 3:
            dirs[:] = []
            continue
        for f in files:
            if f.lower().endswith(".xlsx") and not f.startswith("~$"):
                found.append(os.path.join(dirpath, f))
            elif f.lower().endswith(".zip"):
                zips.append(os.path.join(dirpath, f))

if os.path.isdir(CACHE):
    shutil.rmtree(CACHE, ignore_errors=True)
os.makedirs(CACHE, exist_ok=True)
zx = 0
for zp in zips:
    try:
        with zipfile.ZipFile(zp) as z:
            for member in z.namelist():
                if not member.lower().endswith(".xlsx") or os.path.basename(member).startswith("~$"):
                    continue
                base = os.path.basename(member)
                if not base:
                    continue
                dest = os.path.join(CACHE, f"{zx:04d}_{base}")
                with z.open(member) as fh, open(dest, "wb") as out:
                    shutil.copyfileobj(fh, out)
                mt = os.path.getmtime(zp)
                os.utime(dest, (mt, mt))
                found.append(dest)
                zx += 1
    except Exception:
        pass

print(f"scan roots         : {', '.join(ROOTS)}")
print(f"zips inspected     : {len(zips)}  (xlsx extracted: {zx})")

dcsc = []
for p in found:
    try:
        with zipfile.ZipFile(p) as z:
            wb = z.read("xl/workbook.xml").decode("utf-8", "ignore")
        if "Message History" in wb or "ConfigGroupView" in wb:
            dcsc.append(p)
    except Exception:
        pass

# de-dupe: same basename+size means the loose copy and the zip copy are the same export
def dkey(p):
    b = os.path.basename(p)
    if p.startswith(CACHE):
        b = ZIP_PREFIX.sub("", b)
    return (b.lower(), os.path.getsize(p))

seen, uniq = set(), []
for p in sorted(dcsc, key=lambda x: (x.startswith(CACHE), x)):
    k = dkey(p)
    if k in seen:
        continue
    seen.add(k)
    uniq.append(p)

print(f"xlsx scanned       : {len(found)}")
print(f"DCSC exports found : {len(uniq)}  ({len(dcsc)-len(uniq)} dupes dropped)\n")
with open(LIST, "w", encoding="utf-8") as fh:
    fh.write("\n".join(uniq))
print(f"wrote {LIST} ({len(uniq)} paths)")
if not uniq:
    print("no DCSC exports found - pass the folder(s) that hold your exports: python scan_dcsc.py <folder>")
