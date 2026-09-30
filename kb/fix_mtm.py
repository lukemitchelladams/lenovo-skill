import sqlite3, re
from paths import DB

cx = sqlite3.connect(DB)
MTM_RE = re.compile(r"^7[A-Z0-9]{3}CTO[0-9A-Z]WW$")
# software / services MTM prefixes that are not the machine being configured
SW = ("7S0", "7S1", "7Q0", "7Q1")
MODEL_RE = re.compile(r"(ThinkSystem\s+[A-Za-z0-9]+(?:\s+V\d)?|ThinkAgile\s+[A-Za-z0-9]+(?:\s+V\d)?|ThinkEdge\s+[A-Za-z0-9]+(?:\s+V\d)?)")

rows = cx.execute("SELECT id FROM config").fetchall()
fixed = 0
for (cid,) in rows:
    cands = cx.execute(
        "SELECT fc, descr, qty FROM part WHERE cfg=? ", (cid,)).fetchall()
    best = None
    for fc, descr, qty in cands:
        if not MTM_RE.match(fc or ""):
            continue
        if fc.startswith(SW):
            continue
        d = descr or ""
        # the machine line looks like "Server : ThinkSystem X" or "... Base Warranty"
        score = 0
        if "Base Warranty" in d: score += 3
        if d.startswith("Server"): score += 2
        if MODEL_RE.search(d): score += 2
        if "Rack Cabinet" in d or "48U" in d: score -= 1
        if score <= 0:
            continue
        if best is None or score > best[0] or (score == best[0] and qty > best[3]):
            best = (score, fc, d, qty)
    if best:
        _, fc, d, qty = best
        m = MODEL_RE.search(d)
        model = m.group(1).strip() if m else d[:40]
        cx.execute("UPDATE config SET mtm=?, model=?, nodes=? WHERE id=?", (fc, model, qty, cid))
        fixed += 1
    else:
        cx.execute("UPDATE config SET mtm='', model='' WHERE id=?", (cid,))
cx.commit()
print(f"re-attributed {fixed}/{len(rows)} configs\n")

print("=== SERVER MTM -> model, config count, TCE-validated count ===")
for mtm, model, n, t, c in cx.execute("""
        SELECT mtm, MIN(model), COUNT(*), SUM(tce), SUM(criticals>0)
        FROM config WHERE mtm<>'' GROUP BY mtm ORDER BY COUNT(*) DESC"""):
    print(f"  {mtm}  {str(model)[:26]:<28} configs={n:<4} TCE={t:<4} errors={c}")
