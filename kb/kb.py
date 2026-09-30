"""
Query the DCSC knowledge base built from validated exports.

Ground-truth rule: if a feature code appears in a config that carries BU1E and
has zero Critical messages, that part is PROVEN TCE-buildable on that MTM.
Everything else is "not seen", which is not the same as "not available".

usage:
  python kb.py fact <terms> [--titles]  curated hand-verified rules, top 3 (--titles: top 8 titles only)
                                      works even with no db built (falls back to kb_facts.py)
  python kb.py docs <query> [--lp lpNNNN]  full-text search of the Lenovo Press page index
  python kb.py page <lp> <page>       print one full Lenovo Press page (lp id + page from `docs`)
  python kb.py sql "<SELECT ...>"     read-only ad-hoc query, 200 rows max
  python kb.py tce <MTM>              proven-TCE parts on that MTM, by category
  python kb.py part <FC>              every MTM a part is proven on, + price history
  python kb.py find <MTM> <regex>     search parts seen on an MTM
  python kb.py errors                 every Critical/Error message ever recorded
  python kb.py configs [regex]        list configs
  python kb.py cmp <cfgA> <cfgB>      diff two configs by id

no db yet?  python refresh.py <folder holding your DCSC exports>
"""
import sqlite3, sys, re, os, pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from paths import DB

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

NO_DB = (f"No knowledge base at {DB}\n"
         "Build one from your own DCSC exports:  python refresh.py <folder holding your DCSC exports>")
cx = None

def connect():
    global cx
    if not os.path.exists(DB):
        sys.exit(NO_DB)
    cx = sqlite3.connect(pathlib.Path(DB).as_uri() + "?mode=ro", uri=True)
    return cx

def has_table(name):
    return cx.execute("SELECT 1 FROM sqlite_master WHERE name=?", (name,)).fetchone() is not None

def fts(sql, q, lp=None):
    # raw FTS5 syntax first; if it does not parse (e.g. a hyphenated part number), retry with quoted terms
    mk = lambda s: f"lp:{lp} AND ({s})" if lp else s
    try:
        return cx.execute(sql, (mk(q),)).fetchall()
    except sqlite3.OperationalError:
        safe = " ".join('"%s"' % t.replace('"', '""') for t in q.split())
        try:
            return cx.execute(sql, (mk(safe),)).fetchall()
        except sqlite3.OperationalError as e:
            sys.exit(f"search error: {e}")

def cat(d):
    d = (d or "").lower()
    if "backplane" in d: return "BACKPLANE"
    if "chassis" in d: return "CHASSIS"
    if "processor" in d and ("xeon" in d or "epyc" in d): return "CPU"
    if "rdimm" in d or "truddr5" in d: return "MEMORY"
    if "m.2" in d: return "M.2 / BOOT"
    if "nvme" in d and ("ssd" in d or "u.2" in d or "u.3" in d): return "NVMe DRIVE"
    if "hdd" in d: return "HDD"
    if "ssd" in d: return "SSD (SAS/SATA)"
    if "raid" in d or "hba" in d or "vroc" in d: return "CONTROLLER"
    if "ethernet" in d or "gbe" in d or "connectx" in d: return "NETWORK"
    if "power supply" in d: return "PSU"
    if "riser" in d: return "RISER"
    if "fan" in d or "heatsink" in d: return "THERMAL"
    if "premier" in d or "warranty" in d or "month" in d: return "SERVICE"
    return "other"

def fact(args):
    titles_only = "--titles" in args
    terms = [a for a in args if a != "--titles"]
    if not terms: print(__doc__); return
    q, n, rows = " ".join(terms), (8 if titles_only else 3), None
    if os.path.exists(DB):
        try:
            connect()
            if has_table("fact_fts"):
                rows = fts("""SELECT f.topic, f.scope, f.status, f.title, f.body, f.source, f.verified
                              FROM fact_fts JOIN fact f ON f.id = fact_fts.fact_id
                              WHERE fact_fts MATCH ? ORDER BY bm25(fact_fts) LIMIT %d""" % n, q)
        except sqlite3.DatabaseError:
            rows = None
    if rows is None:
        sys.path.insert(0, HERE)
        try:
            from kb_facts import FACTS
        except ImportError:
            sys.exit("No fact table in the db and kb_facts.py not found.\n" + NO_DB)
        print("(no fact table in the db, using substring match on kb_facts.py)", file=sys.stderr)
        ts, scored = q.lower().split(), []
        for f in FACTS:
            blob = " ".join(str(f[i]) for i in (0, 1, 3, 4, 5)).lower()
            if all(t in blob for t in ts):
                head = (str(f[0]) + " " + str(f[3])).lower()
                scored.append((-sum(t in head for t in ts), f))
        rows = [f for _, f in sorted(scored, key=lambda x: x[0])][:n]
    if not rows:
        print(f"no facts matched: {q}"); return
    for topic, scope, status, title, body, source, verified in rows:
        if titles_only:
            print(f"[{topic}] {title}  ({status})")
        else:
            print(f"[{topic}] {title}\n  status: {status} | scope: {scope} | verified: {verified}\n  {body}\n  source: {source}\n")

def docs(args):
    args, lp = list(args), None
    if "--lp" in args:
        i = args.index("--lp")
        lp = args[i + 1].lower()
        del args[i:i + 2]
        if lp.isdigit(): lp = "lp" + lp.zfill(4)
    if not args: print(__doc__); return
    connect()
    if not has_table("doc_fts"):
        sys.exit("No doc index in the db. Fetch the docs, then index them:\n"
                 "  python docs/get_lenovo_docs.py\n  python kb/build_kb_index.py --docs-only")
    rows = fts("SELECT lp, page, snippet(doc_fts,3,'>>','<<','...',20) FROM doc_fts "
               "WHERE doc_fts MATCH ? ORDER BY bm25(doc_fts) LIMIT 6", " ".join(args), lp)
    for lp_, page, snip in rows:
        print(f"{lp_} p{page}: {' '.join(snip.split())}\n")
    if not rows: print("no doc pages matched")
    else: print("full page:  python kb.py page <lp> <page>")

def page(lp, pg):
    connect()
    lp = lp.lower()
    if lp.isdigit(): lp = "lp" + lp.zfill(4)
    if not has_table("doc_fts"):
        sys.exit("No doc index in the db. Run: python kb/build_kb_index.py --docs-only")
    r = cx.execute("SELECT title, text FROM doc_fts WHERE lp=? AND page=?", (lp, int(pg))).fetchone()
    if not r: print(f"{lp} page {pg}: not found"); return
    print(f"{lp} p{pg}  {r[0]}\n\n{r[1]}")

def sql(q):
    if not re.match(r"\s*(select|with)\b", q, re.I):
        sys.exit("sql: SELECT/WITH statements only (the db is opened read-only)")
    connect()
    try:
        cur = cx.execute(q)
        rows = cur.fetchmany(201)
    except sqlite3.Error as e:
        sys.exit(f"sql error: {e}")
    cell = lambda v: "" if v is None else " ".join(str(v).split())[:60]
    head = [d[0] for d in cur.description]
    body = [[cell(v) for v in r] for r in rows[:200]]
    w = [max(len(h), *(len(r[i]) for r in body)) if body else len(h) for i, h in enumerate(head)]
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(head)))
    print("  ".join("-" * x for x in w))
    for r in body: print("  ".join(v.ljust(w[i]) for i, v in enumerate(r)).rstrip())
    print(f"({len(body)} rows{', truncated at 200' if len(rows) > 200 else ''})")

def tce(mtm):
    rows = cx.execute("""
      SELECT p.fc, MIN(p.descr), COUNT(DISTINCT c.id), MAX(p.unit)
      FROM part p JOIN config c ON c.id=p.cfg
      WHERE c.mtm=? AND c.tce=1 AND c.criticals=0
      GROUP BY p.fc ORDER BY p.fc""", (mtm,)).fetchall()
    n = cx.execute("SELECT COUNT(*),MIN(model) FROM config WHERE mtm=? AND tce=1 AND criticals=0",(mtm,)).fetchone()
    print(f"{mtm}  {n[1]}  -  proven from {n[0]} TCE-validated, error-free config(s)")
    print(f"{len(rows)} parts proven TCE-buildable\n")
    buckets = {}
    for fc, d, seen, price in rows:
        buckets.setdefault(cat(d), []).append((fc, d, seen, price))
    for k in sorted(buckets):
        print(f"--- {k}")
        for fc, d, seen, price in sorted(buckets[k], key=lambda r: -(r[3] or 0)):
            pr = f"${price:,.2f}" if price else ""
            print(f"    {fc:<7}{pr:>12}  x{seen:<3} {d[:62]}")
        print()

def part(fc):
    rows = cx.execute("""
      SELECT c.mtm, MIN(c.model), SUM(c.tce=1 AND c.criticals=0), COUNT(*), MIN(p.descr), MAX(p.unit)
      FROM part p JOIN config c ON c.id=p.cfg
      WHERE p.fc=? AND c.mtm<>'' GROUP BY c.mtm ORDER BY COUNT(*) DESC""", (fc,)).fetchall()
    if not rows:
        print(f"{fc}: never seen in any validated config"); return
    print(f"{fc}  {rows[0][4]}\n")
    print(f"{'MTM':<12}{'model':<24}{'TCE-proven':>11}{'seen':>6}")
    for mtm, model, tceok, seen, d, price in rows:
        flag = "YES" if tceok else "no"
        print(f"{mtm:<12}{str(model)[:22]:<24}{flag:>11}{seen:>6}")
    pr = cx.execute("SELECT DISTINCT unit FROM part WHERE fc=? AND unit>0 ORDER BY unit",(fc,)).fetchall()
    if pr: print("\nprices seen: " + ", ".join(f"${p[0]:,.2f}" for p in pr))

def find(mtm, pat):
    rx = re.compile(pat, re.I)
    rows = cx.execute("""
      SELECT p.fc, MIN(p.descr), SUM(c.tce=1 AND c.criticals=0), COUNT(*), MAX(p.unit)
      FROM part p JOIN config c ON c.id=p.cfg
      WHERE c.mtm=? GROUP BY p.fc""", (mtm,)).fetchall()
    hits = [r for r in rows if rx.search(r[1] or "")]
    print(f"{mtm}: {len(hits)} parts matching /{pat}/\n")
    print(f"{'FC':<7}{'TCE':>5}{'seen':>6}{'price':>12}  description")
    for fc, d, tceok, seen, price in sorted(hits, key=lambda r: -(r[2] or 0)):
        pr = f"${price:,.2f}" if price else ""
        print(f"{fc:<7}{('YES' if tceok else '-'):>5}{seen:>6}{pr:>12}  {d[:60]}")

def errors():
    rows = cx.execute("""
      SELECT m.severity, m.text, c.model, c.mtm, c.name
      FROM msg m JOIN config c ON c.id=m.cfg
      WHERE LOWER(m.severity) IN ('critical','error')
      ORDER BY m.severity, m.text""").fetchall()
    seen=set(); n=0
    for sev, txt, model, mtm, name in rows:
        k=(sev,txt[:120])
        if k in seen: continue
        seen.add(k); n+=1
        print(f"[{sev}] {mtm}  {model}")
        print(f"   {txt[:400]}")
        print(f"   seen in: {name[:70]}\n")
    print(f"{n} distinct Critical/Error rules recorded")

def configs(pat=None):
    rows = cx.execute("""SELECT id,mtime,mtm,model,nodes,tce,criticals,total,name
                         FROM config ORDER BY mtime DESC""").fetchall()
    rx = re.compile(pat, re.I) if pat else None
    print(f"{'id':>4} {'date':<11}{'MTM':<12}{'model':<22}{'n':>4}{'TCE':>5}{'err':>4}{'total':>14}  file")
    for i,dt,mtm,model,nodes,t,c,tot,name in rows:
        if rx and not rx.search(name): continue
        print(f"{i:>4} {dt:<11}{mtm:<12}{str(model)[:20]:<22}{(nodes or 0):>4.0f}{('Y' if t else '-'):>5}{c:>4}{tot:>14,.0f}  {name[:52]}")

def cmp(a,b):
    def load(cid):
        return {fc:(q,d) for fc,q,d in cx.execute(
            "SELECT fc,SUM(qty),MIN(descr) FROM part WHERE cfg=? GROUP BY fc",(cid,))}
    A,B=load(int(a)),load(int(b))
    na=cx.execute("SELECT name FROM config WHERE id=?",(a,)).fetchone()[0]
    nb=cx.execute("SELECT name FROM config WHERE id=?",(b,)).fetchone()[0]
    print(f"A = {na}\nB = {nb}\n")
    print("--- only in A"); [print(f"   -{A[k][0]:>5.0f}  {k:<7} {A[k][1][:60]}") for k in sorted(set(A)-set(B))]
    print("--- only in B"); [print(f"   +{B[k][0]:>5.0f}  {k:<7} {B[k][1][:60]}") for k in sorted(set(B)-set(A))]
    print("--- qty changed")
    for k in sorted(set(A)&set(B)):
        if A[k][0]!=B[k][0]: print(f"    {k:<7} {A[k][0]:.0f} -> {B[k][0]:.0f}   {A[k][1][:52]}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "help"): print(__doc__); sys.exit()
    c = a[0]
    try:
        if   c=="fact":    fact(a[1:])
        elif c=="docs":    docs(a[1:])
        elif c=="page":    page(a[1], a[2])
        elif c=="sql":     sql(" ".join(a[1:]))
        elif c in ("tce","part","find","errors","configs","cmp"):
            connect()
            if   c=="tce":     tce(a[1].upper())
            elif c=="part":    part(a[1].upper())
            elif c=="find":    find(a[1].upper(), a[2])
            elif c=="errors":  errors()
            elif c=="configs": configs(a[2] if len(a)>2 else (a[1] if len(a)>1 else None))
            else:              cmp(a[1], a[2])
        else: print(__doc__)
    except IndexError:
        print(__doc__)
    except sqlite3.OperationalError as e:
        sys.exit(f"database error: {e}\nRebuild with:  python refresh.py <folder holding your DCSC exports>")
