"""One-call answer brief: pulls every source linked to the entities in a question, in one process.

The skill's fast path. Instead of 6-10 separate lookups (fact, rules, dfind, part, parts, gates, docs),
`ask` resolves the feature codes, MTMs and model names in the question, follows their links
(fact <-> FC/model, FC <-> MTM rules, FC <-> exports, FC <-> guide tables) and prints a compact brief.
Nothing is dropped from the knowledge base: the brief is a ranked view, the full commands still work.

usage:
  python kb.py ask "<question>" [--mtm <MTM|model>] [--deep]
    --deep   more rows per section, plus Lenovo Press page snippets even when facts answer it

The DCSC rules snapshot (kb/data/dcsc-rules.json.gz) is indexed into kb/data/rules-cache.sqlite on
first use and rebuilt automatically when the snapshot changes.
"""
import gzip, json, os, pathlib, re, sqlite3, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from paths import DB
import dcsc_rules

CACHE = os.path.join(HERE, "data", "rules-cache.sqlite")
CACHE_VER = "2"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

STOP = set("""a an and are as at be but by can could do does did for from has have how i if in into is it its
me my need needs of on or our should so than that the their them then there these they this to too up us was
we what when where which who why will with would you your yes no not any all also just get got go use using
used add added adding put make makes want wants like does work works one two three four five six eight per
please tell show give find there here same other only much many more most very really still ok okay""".split())
ACRO = set("TCE RAID NVME SATA SAS DCSC HBA OCP PCIE CPU GPU DIMM SSD HDD BOM DAC LFF SFF AMD INTEL CTO MTM VMWARE "
           "ISCSI WHAT WHY HOW DOES THE AND FOR WITH THIS THAT NEED SFP QSFP OM4 LC-LC".split())
# words that carry no lookup value for facts and options (kept for gating-message search)
WEAK = set("""error errors issue issues problem problems message wrong allowed option options config configuration
configure build server servers node nodes support supported difference between work right correct sure tce
express top choice dcsc lenovo thinksystem thinkagile""".split())
# question words -> DCSC description vocabulary
SYN = {"dimm": ["rdimm", "dimm"], "dimms": ["rdimm", "dimm"], "memory": ["rdimm", "dimm"], "ram": ["rdimm", "dimm"],
       "nic": ["ethernet"], "nics": ["ethernet"], "network": ["ethernet"], "drive": ["ssd", "hdd"], "drives": ["ssd", "hdd"],
       "disk": ["ssd", "hdd"], "disks": ["ssd", "hdd"], "psu": ["power"], "cpu": ["processor"], "cpus": ["processor"],
       "fiber": ["lc-lc", "om4", "mmf"], "fibre": ["lc-lc", "om4", "mmf"], "optic": ["transceiver"], "optics": ["transceiver"],
       "boot": ["m.2", "boot"], "rails": ["rail"], "cables": ["cable"], "gpus": ["gpu"], "hba": ["hba"], "raid": ["raid"]}
MODEL_RX = re.compile(r"\b((?:SR|ST|SE|SD|SN|HX|VX|MX|FX|HS|DE|DM|DG|DS)\s?-?\d{2,4}[a-zA-Z]?|D\d{4})"
                      r"(?:\s+(V\d)\b)?(?:\s+(Storage|Storage Node|ROBO|Edge))?", re.I)
MTM_RX = re.compile(r"\b(\d[A-Z0-9]{3}CTO[0-9A-Z]{1,2}WW|\d[A-Z0-9]{3})\b")


# ------------------------------------------------------------------ rules cache
def cache():
    src = dcsc_rules.DATA
    sig = f"{CACHE_VER}:{os.path.getsize(src)}:{int(os.path.getmtime(src))}" if os.path.exists(src) else ""
    if os.path.exists(CACHE):
        try:
            cx = sqlite3.connect(CACHE)
            if cx.execute("SELECT v FROM meta WHERE k='sig'").fetchone() == (sig,):
                return cx
            cx.close()
        except sqlite3.DatabaseError:
            pass
        os.remove(CACHE)
    if not sig:
        return None
    t0 = time.time()
    db = dcsc_rules.load()
    cx = sqlite3.connect(CACHE)
    cx.executescript("""
      CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
      CREATE TABLE model(mtm TEXT PRIMARY KEY, name TEXT);
      CREATE TABLE opt(mtm TEXT, tab TEXT, sub TEXT, sec TEXT, fc TEXT, descr TEXT, mn INT, mx INT, tc INT, ta INT, wd TEXT, ty TEXT);
      CREATE TABLE dflt(mtm TEXT, sec TEXT, fc TEXT, q TEXT, req INT);
      CREATE TABLE gate(sev TEXT, text TEXT, mtms TEXT, n INT);
      CREATE VIRTUAL TABLE opt_fts USING fts5(descr, sec, content='opt', content_rowid='rowid');
      CREATE VIRTUAL TABLE gate_fts USING fts5(text, content='gate', content_rowid='rowid');""")
    for mtm, m in db["models"].items():
        cx.execute("INSERT INTO model VALUES(?,?)", (mtm, m.get("name", "")))
        cx.executemany("INSERT INTO opt VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                       [(mtm, *o[:3], o[3], o[4], o[5], o[6], o[7], o[10] if len(o) > 10 else None, o[8], o[9])
                        for o in dcsc_rules.options(db, mtm)])
        cx.executemany("INSERT INTO dflt VALUES(?,?,?,?,?)",
                       [(mtm, s["n"], f[0], dcsc_rules.fmt_q(f[4]), s["req"]) for s in m["secs"] for f in s["f"]])
    for r in db["meta"].get("retired", []):
        cx.execute("INSERT OR IGNORE INTO model VALUES(?,?)", (r["mtm"], (r.get("name") or "") + " [RETIRED: DCSC no longer opens this CTO]"))
    cx.executemany("INSERT INTO gate VALUES(?,?,?,?)", [(g["sev"], g["text"], ",".join(g["mtms"]), g["n"]) for g in db["gates"]])
    cx.executescript("""
      CREATE INDEX opt_fc ON opt(fc); CREATE INDEX opt_mtm ON opt(mtm); CREATE INDEX dflt_k ON dflt(mtm, fc);
      INSERT INTO opt_fts(rowid, descr, sec) SELECT rowid, descr, sec FROM opt;
      INSERT INTO gate_fts(rowid, text) SELECT rowid, text FROM gate;""")
    meta = {k: v for k, v in db["meta"].items() if k != "retired"}
    cx.executemany("INSERT INTO meta VALUES(?,?)", [("sig", sig), ("crawled", meta.get("crawled", "")),
                                                    ("lists", json.dumps(meta.get("lists") or {}))])
    cx.commit()
    print(f"(indexed the DCSC rules snapshot in {time.time() - t0:.1f}s, one time)", file=sys.stderr)
    return cx


def kbdb():
    if not os.path.exists(DB):
        return None
    try:
        return sqlite3.connect(pathlib.Path(DB).as_uri() + "?mode=ro", uri=True)
    except sqlite3.Error:
        return None


def has(cx, t):
    return cx is not None and cx.execute("SELECT 1 FROM sqlite_master WHERE name=?", (t,)).fetchone() is not None


def fq(words):
    """FTS5 OR-query of quoted words (safe for hyphens and punctuation)."""
    return " OR ".join('"%s"' % w.replace('"', '') for w in words)


# ------------------------------------------------------------------ entity resolution
def models_for(rc, name_q):
    toks = re.sub(r"[^A-Z0-9]+", " ", name_q.upper()).split()
    toks = [t for t in toks if t]
    if not toks:
        return []
    # "SR650a" -> token SR650A must match a whole name token
    hits = []
    for mtm, nm in rc.execute("SELECT mtm, name FROM model"):
        nt = re.sub(r"[^A-Z0-9]+", " ", nm.upper()).split()
        if all(t in nt for t in toks):
            hits.append((mtm, nm))
    if len(hits) > 1:
        plain = [h for h in hits if re.search(r"base warranty", h[1], re.I) and "RETIRED" not in h[1]
                 and not re.search(r"dwc|workstation|hana|for ai|neptune|water|storage|robo|edge", h[1], re.I)
                 and not re.search(r"storage|edge|robo", name_q, re.I)]
        if plain:
            return plain[:1]
    return hits[:3]


def entities(q, rc, kc, mtm_opt):
    mtms, fcs, used, labels = [], [], set(), []
    for m in MTM_RX.finditer(q.upper()):
        tok = m.group(1)
        if len(tok) > 4 and rc and rc.execute("SELECT 1 FROM model WHERE mtm=?", (tok,)).fetchone():
            mtms.append((tok, rc.execute("SELECT name FROM model WHERE mtm=?", (tok,)).fetchone()[0])); used.add(tok)
    for m in MODEL_RX.finditer(q):
        label = " ".join(x for x in m.groups() if x)
        labels.append(label)
        if rc:
            for h in models_for(rc, label):
                if h[0] not in [x[0] for x in mtms]:
                    mtms.append(h)
        used.update(w.upper() for w in label.split())
    if mtm_opt and rc:
        for h in ([(mtm_opt.upper(), "")] if rc.execute("SELECT 1 FROM model WHERE mtm=?", (mtm_opt.upper(),)).fetchone()
                  else models_for(rc, mtm_opt)):
            nm = h[1] or rc.execute("SELECT name FROM model WHERE mtm=?", (h[0],)).fetchone()[0]
            if h[0] not in [x[0] for x in mtms]:
                mtms.insert(0, (h[0], nm))
    for raw in re.findall(r"[A-Za-z0-9]{4}", q):
        t = raw.upper()
        if t in used or t in ACRO or t in fcs:
            continue
        if not (re.search(r"\d", t) or raw.isupper()):
            continue
        known = (rc and rc.execute("SELECT 1 FROM opt WHERE fc=? LIMIT 1", (t,)).fetchone()) or \
                (has(kc, "part") and kc.execute("SELECT 1 FROM part WHERE fc=? LIMIT 1", (t,)).fetchone()) or \
                (has(kc, "press_part") and kc.execute("SELECT 1 FROM press_part WHERE fc=? LIMIT 1", (t,)).fetchone())
        if known:
            fcs.append(t)
    words = [w.strip(".?,:;") for w in re.findall(r"[A-Za-z][A-Za-z0-9.+/-]{1,}|\d+(?:\.\d+)?(?:[A-Za-z]+[A-Za-z0-9/]*)", q)]
    words = [w for w in words if w and w.lower() not in STOP and w.upper() not in used and w.upper() not in fcs
             and (len(w) > 2 or re.match(r"\d", w))]
    return mtms, fcs, words, labels


# ------------------------------------------------------------------ sections
def _model_keys(labels):
    """'SR635 V3' -> {'sr635 v3', 'sr635v3'}; the generation token alone (V3) is too common to rank on."""
    ks = set()
    for lb in labels:
        b = " ".join(lb.lower().split())
        ks |= {b, b.replace(" ", "")}
    return ks


def sec_facts(kc, q_words, fcs, labels, n):
    """Facts ranked by links to the question: names an FC (+3), names the model (+2), each keyword (+1)."""
    q_words = [w for w in q_words if w.lower() not in WEAK]
    core = fcs + q_words
    mk = _model_keys(labels)
    rows = []
    if has(kc, "fact_fts"):
        for fc in fcs:  # graph edge: facts that name the feature code
            rows += kc.execute("SELECT topic,status,title,body,source,scope FROM fact WHERE body LIKE ? OR title LIKE ? LIMIT 5",
                               (f"%{fc}%", f"%{fc}%")).fetchall()
        terms = core or [t for lb in labels for t in lb.split() if not re.fullmatch(r"v\d", t, re.I)]
        if terms:
            try:
                rows += kc.execute("SELECT f.topic,f.status,f.title,f.body,f.source,f.scope FROM fact_fts x JOIN fact f ON f.id=x.fact_id "
                                   "WHERE fact_fts MATCH ? ORDER BY bm25(fact_fts) LIMIT 15", (fq(terms),)).fetchall()
            except sqlite3.OperationalError:
                pass
    else:
        try:
            from kb_facts import FACTS
        except ImportError:
            FACTS = []
        rows = [(f[0], f[2], f[3], f[4], f[5], f[1]) for f in FACTS]
    scored, seen = [], set()
    for topic, status, title, body, source, scope in rows:
        if topic in seen:
            continue
        seen.add(topic)
        blob = f"{title} {body} {scope}".lower()
        flat = blob.replace(" ", "")
        s = 3 * sum(fc.lower() in blob for fc in fcs) + 2 * any(k in blob or k in flat for k in mk) \
            + sum(w.lower() in blob for w in q_words)
        need = 2 if len(core) + bool(mk) >= 2 else 1
        if s >= need:
            scored.append((-s, len(scored), status, title, body, source))
    out = []
    for _, _, status, title, body, source in sorted(scored)[:n]:
        b = " ".join(body.split())
        out.append(f"  [{status}] {title}\n    {b[:360]}{'...' if len(b) > 360 else ''}\n    src: {source}")
    return out


def sec_rules_fc(rc, fc, mtms, n):
    want = [m for m, _ in mtms]
    rows = rc.execute("SELECT o.mtm, m.name, o.tab, o.sec, o.descr, o.mn, o.mx, o.tc, o.ta, o.wd, d.q FROM opt o "
                      "JOIN model m ON m.mtm=o.mtm LEFT JOIN dflt d ON d.mtm=o.mtm AND d.fc=o.fc AND d.sec=o.sec WHERE o.fc=?",
                      (fc,)).fetchall()
    if not rows:
        return [f"  {fc}: not in the DCSC rules snapshot"], None
    descr = rows[0][4]
    if want:
        mine = [r for r in rows if r[0] in want]
        other = len({r[0] for r in rows}) - len({r[0] for r in mine})
        rows = mine
    else:
        other = 0
    out = []
    for mtm, nm, tab, sec, d, mn, mx, tc, ta, wd, q in rows[:n]:
        out.append(f"  {fc} on {mtm} {nm[:30]}: {tab}/{sec} tce={dcsc_rules.tce_tag(tc, ta)} min={mn} max={mx}"
                   f"{' default-q=' + q if q else ''}{' WITHDRAWN ' + wd if wd else ''}")
    if want and not rows:
        out.append(f"  {fc} is NOT an option on {', '.join(want)} in the snapshot")
    tot = rc.execute("SELECT COUNT(DISTINCT mtm), SUM(tc>0) FROM opt WHERE fc=?", (fc,)).fetchone()
    out.append(f"  ({fc} = {descr[:70]}; offered on {tot[0]} MTMs{', ' + str(other) + ' others not shown' if other else ''})")
    return out, descr


def opt_query(rc, mtm, words):
    """AND of the word groups that exist on this MTM (synonyms OR'd inside a group); OR of them as the fallback."""
    groups = []
    for w in words:
        if w.lower() in WEAK:
            continue
        g = "(" + fq(SYN.get(w.lower(), [w])) + ")"
        try:
            if rc.execute("SELECT 1 FROM opt_fts f JOIN opt o ON o.rowid=f.rowid WHERE opt_fts MATCH ? AND o.mtm=? LIMIT 1",
                          (g, mtm)).fetchone():
                groups.append(g)
        except sqlite3.OperationalError:
            pass
    return (" AND ".join(groups), " OR ".join(groups)) if groups else (None, None)


def opt_rows(rc, mtm, words, lim):
    qa, qo = opt_query(rc, mtm, words)
    rows = []
    for qq in (qa, qo):
        if not qq:
            continue
        rows = rc.execute("SELECT o.sec, o.fc, o.descr, o.mx, o.tc, o.ta, o.wd FROM opt_fts f JOIN opt o ON o.rowid=f.rowid "
                          "WHERE opt_fts MATCH ? AND o.mtm=? ORDER BY o.wd!='', bm25(opt_fts) LIMIT ?", (qq, mtm, lim)).fetchall()
        if rows:
            break
    return rows


def sec_options(rc, mtm, words, n):
    if not words:
        return []
    rows = opt_rows(rc, mtm, words, n * 3)
    out, seen = [], set()
    for sec, fc, d, mx, tc, ta, wd in rows:
        if (sec, fc) in seen:
            continue
        seen.add((sec, fc))
        out.append(f"  {fc:<6} tce={dcsc_rules.tce_tag(tc, ta):<5} max={mx if mx is not None else '-':<3} {sec[:24]:<24} {d[:70]}"
                   f"{' WITHDRAWN ' + wd if wd else ''}")
        if len(out) >= n:
            break
    return out


def sec_exports(kc, fc, mtms, quiet=False):
    if not has(kc, "part"):
        return None
    rows = kc.execute("SELECT c.model, COUNT(DISTINCT c.id), SUM(c.tce=1 AND c.criticals=0), MAX(substr(c.mtime,1,10)) "
                      "FROM part p JOIN config c ON c.id=p.cfg WHERE p.fc=? GROUP BY c.model ORDER BY 3 DESC, 2 DESC", (fc,)).fetchall()
    if not rows:
        return None if quiet else f"  {fc}: in 0 of your exports (unproven, not prohibited)"
    s = "; ".join(f"{m or '?'} {n} cfg{'s' if n > 1 else ''}/{t or 0} TCE-proven (last {d})" for m, n, t, d in rows[:5])
    return f"  {fc}: {s}{' ...' if len(rows) > 5 else ''}"


def sec_guide(kc, fc):
    if not has(kc, "press_part"):
        return None
    rows = kc.execute("SELECT lp, platform, tce, pn, MIN(page) FROM press_part WHERE fc=? GROUP BY lp, platform "
                      "ORDER BY tce='' , lp DESC LIMIT 3", (fc,)).fetchall()
    if not rows:
        return None
    return f"  {fc}: " + "; ".join(f"{lp} {pl[:24]} PN {pn or '-'} {tce or ''} p{pg}".replace("  ", " ") for lp, pl, tce, pn, pg in rows)


def sec_gates(rc, words, mtms, n):
    if not words:
        return []
    try:
        rows = rc.execute("SELECT g.sev, g.text, g.mtms FROM gate_fts f JOIN gate g ON g.rowid=f.rowid WHERE gate_fts MATCH ? "
                          "ORDER BY bm25(gate_fts) LIMIT 12", (fq(words),)).fetchall()
    except sqlite3.OperationalError:
        return []
    want = {m for m, _ in mtms}
    if want:
        rows = sorted(rows, key=lambda r: not (want & set(r[2].split(","))))
    return [f"  [{s}] {' '.join(re.sub(r'<[^>]+>', ' ', t).split())[:260]}  ({m[:40]})" for s, t, m in rows[:n]]


def sec_docs(kc, words, mtms, n):
    if not has(kc, "doc_fts") or not words:
        return []
    lps = []
    try:
        import specs
        for _, nm in mtms[:2]:
            p = specs.find(re.sub(r"-.*", "", nm))
            lps += [x["source"] for x in p[:1]]
    except Exception:
        pass
    out = []
    for lp in (lps or [None]):
        q = fq(words)
        if lp:
            q = f"lp:{lp} AND ({q})"
        try:
            rows = kc.execute("SELECT lp, page, snippet(doc_fts,3,'>>','<<','...',18) FROM doc_fts WHERE doc_fts MATCH ? "
                              "ORDER BY bm25(doc_fts) LIMIT ?", (q, n)).fetchall()
        except sqlite3.OperationalError:
            rows = []
        out += [f"  {l} p{p}: {' '.join(s.split())}" for l, p, s in rows]
    return out[:n]


# ------------------------------------------------------------------ router
# Decides, before any lookup, what the question needs. Order matters only for display.
INTENTS = [
    ("aix", r"\bai[ -]?express\b|\baix\b"),
    ("tce", r"\btce\b|top choice|\bexpress\b|quick ?ship|ship (fast|quick)|lead ?time|\bbu1e\b"),
    ("error", r"\berror|warning|won'?t let|not allowed|gr[ae]yed|blocked|conflict|critical|invalid|can'?t (add|select|pick)|cannot"),
    ("price", r"\bprice|\bcost|\$\d|how much|discount|list price|street|cheaper|expensive"),
    ("lifecycle", r"\beol\b|end of (life|sale|support)|withdraw|\blod\b|\bltb\b|last[ -]time|discontinu|retired|still (available|sold|orderable)"),
    ("compete", r"\bdell\b|\bhpe?\b|cisco|supermicro|poweredge|proliant|\bucs\b|\bnx-?\d|\br[4-9]\d{2}[a-z]*\b|\bc\d{3}\s*m\d\b|\bdl\d{3}\b|competitor|equivalent to"),
    ("spec", r"how many|\bmax(imum)?\b|\bslots?\b|\bbays?\b|sockets?|form factor|depth|weight|dimensions|\bwatts?\b|thermal|ambient|\bfit\b|supports?\b"),
    ("compat", r"compatib|work with|works with|attach|connect|\bcables?\b|required|requires|\bneed\b|which .*(adapter|card|cable|riser|kit)"),
    ("build", r"\bbuild\b|\bbom\b|convert|replace|spec (it )?out|sizing|\bsize\b|configure (a|an|the)|quote (me|a|an)"),
    ("concept", r"^\s*(what is|what's|whats|explain|difference between|what does .* mean|how does)\b"),
]
KEY_CATS = r"Processor|RDIMM|GPU|RTX|NVMe|SSD|HDD|Ethernet|ConnectX|InfiniBand|Power Supply|Chassis|Backplane|RAID|HBA|Base"


def route(q, mtms, fcs):
    hit = [n for n, rx in INTENTS if re.search(rx, q, re.I)]
    if "aix" in hit and "tce" not in hit:
        hit.append("tce")
    if not hit:
        hit = ["lookup"]
    return hit


def aix_mtms(rc, mtms):
    """AI Express lives on specific CTOs (SR650a V4 7DGDCTO2WW, SR675 V3 for AI 7D9RCTO1WW): swap a resolved model
    for the sibling CTO (same machine type) that actually carries tceAudience 2."""
    have = {m for (m,) in rc.execute("SELECT DISTINCT mtm FROM opt WHERE ta & 6")}
    out = []
    for m, nm in mtms:
        if m in have:
            out.append((m, nm)); continue
        sib = [x for x in have if x[:4] == m[:4]]
        out += [(x, rc.execute("SELECT name FROM model WHERE mtm=?", (x,)).fetchone()[0]) for x in sorted(sib)] or [(m, nm)]
    if not mtms:
        out = [(x, rc.execute("SELECT name FROM model WHERE mtm=?", (x,)).fetchone()[0]) for x in sorted(have)]
    return list(dict.fromkeys(out)), have


def key_opts(rc, mtm, ta=None, tce=False, n=24):
    """The parts that define a build (CPU, memory, GPU, drives, NIC, PSU) within an audience, one row per FC."""
    rows = rc.execute("SELECT sec, fc, descr, mx, tc, ta FROM opt WHERE mtm=? AND wd='' " +
                      ("AND (ta & ?) " if ta else "AND tc=1 " if tce else "") + "ORDER BY rowid",
                      (mtm, ta) if ta else (mtm,)).fetchall()
    rx = re.compile(KEY_CATS, re.I)
    out, seen = [], set()
    for sec, fc, d, mx, tc, t in rows:
        if fc in seen or not rx.search(d) or re.search(r"ARRAY|INSTALLATION|RAID_CONFIG|_HS$|HOTSPARE", sec):
            continue
        seen.add(fc)
        out.append(f"  {fc:<6} tce={dcsc_rules.tce_tag(tc, t):<5} max={mx if mx is not None else '-':<3} {sec[:24]:<24} {d[:72]}")
        if len(out) >= n:
            break
    return out


def sec_specs(labels, mtms):
    try:
        import specs
    except Exception:
        return []
    for q in labels + [re.sub(r"-.*|\s+3yr.*", "", nm) for _, nm in mtms]:
        hits = specs.find(q)
        if hits:
            return ["  " + l for l in specs.render(hits[0]).splitlines()]
    return []


def sec_price(kc, fc):
    if not has(kc, "part"):
        return None
    r = kc.execute("SELECT p.unit, substr(c.mtime,1,10), c.model, p.descr FROM part p JOIN config c ON c.id=p.cfg WHERE p.fc=? AND p.unit>0 "
                   "ORDER BY c.mtime DESC", (fc,)).fetchall()
    if not r:
        return f"  {fc}: no price in your exports"
    us = [x[0] for x in r]
    vol = re.search(r"RDIMM|SSD|HDD|NVMe", r[0][3] or "")
    return (f"  {fc}: latest ${r[0][0]:,.2f} per unit ({r[0][1]}, {r[0][2]}); range ${min(us):,.2f}-${max(us):,.2f} over {len(r)} lines"
            + ("  [memory/drive prices moved 50-100% in weeks: re-price in DCSC]" if vol else ""))


def sec_compete(q):
    try:
        import compete
        return ["  " + s for s in compete.suggest(q, 5)]
    except Exception as e:
        return [f"  competitor map unavailable ({type(e).__name__})"]


def main(argv):
    a = [x for x in argv if x != "ask"]
    deep = "--deep" in a
    a = [x for x in a if x != "--deep"]
    mtm_opt = None
    if "--mtm" in a:
        i = a.index("--mtm"); mtm_opt = a[i + 1]; del a[i:i + 2]
    q = " ".join(a).strip()
    if not q:
        print(__doc__); return 2
    t0 = time.time()
    rc, kc = cache(), kbdb()
    mtms, fcs, words, labels = entities(q, rc, kc, mtm_opt)
    intents = route(q, mtms, fcs)
    n = 6 if deep else 3
    crawled = rc.execute("SELECT v FROM meta WHERE k='crawled'").fetchone()[0] if rc else "-"
    gaps, used = [], ["facts"]
    if "aix" in intents and rc:
        mtms, aix_have = aix_mtms(rc, mtms)
    fact_words = words + (["AI Express"] if "aix" in intents else []) + (["LOD", "LTB"] if "lifecycle" in intents else [])
    out = [f"Q: {q}",
           "entities: " + (", ".join(f"{m} ({nm[:40]})" for m, nm in mtms) or "no model") + " | FC: " + (", ".join(fcs) or "none")
           + " | keywords: " + (" ".join(words[:10]) or "-")]
    body = []
    f = sec_facts(kc, fact_words, fcs, labels, n)
    body += ["\nFACTS (curated, carry the status word into the answer):"] + (f or ["  none matched"])
    if "build" in intents:
        gaps.append("BUILD request: follow the BUILD PATH (reference.md: match/check, export history) and end with the DCSC paste")
    if rc and (fcs or mtms):
        used.append("DCSC rules")
        body.append(f"\nDCSC RULES (snapshot {crawled}; tce flag is per section, BU1E in a live export is proof):")
        for fc in fcs[:6]:
            lines, _ = sec_rules_fc(rc, fc, mtms, 8 if deep else 4)
            body += lines
        for mtm, nm in mtms[:2]:
            if "RETIRED" in nm:
                body.append(f"  {mtm}: {nm}"); gaps.append(f"{mtm} is retired in DCSC: quote a current platform")
                continue
            ow = [w for w in words if w.lower() not in nm.lower()]
            opts = sec_options(rc, mtm, ow, 12 if deep else 8) if ow and not fcs else []
            if "aix" in intents and not opts:
                ko = key_opts(rc, mtm, ta=6)
                if ko:
                    body += [f"  AI Express parts on {mtm} {nm[:36]} (AIX = SM, proof CU1B; AIX-L = LG, proof CU1A):"] + ko
                else:
                    body.append(f"  {mtm}: no AI Express parts in the snapshot")
            elif "tce" in intents and not opts and not fcs:
                body += [f"  TCE parts on {mtm} {nm[:36]} (key categories):"] + key_opts(rc, mtm, tce=True, n=18)
            elif opts:
                body += [f"  options on {mtm} {nm[:36]} matching '{' '.join(ow[:6])}':"] + opts
    elif rc and {"tce", "compat", "spec", "error", "lookup"} & set(intents) and "aix" not in intents:
        gaps.append("no model or feature code named: ask which platform (or pass --mtm) before quoting parts")
    # export proof: only when the question is about TCE, compatibility, errors or names a part
    if intents != ["concept"] and (fcs or {"tce", "aix", "compat", "error"} & set(intents)):
        proof_fcs, quiet = list(fcs), not fcs
        if not proof_fcs and rc and mtms and words:
            proof_fcs = list(dict.fromkeys(r[1] for r in opt_rows(rc, mtms[0][0], words, 12)))[:5]
        ex = [x for x in (sec_exports(kc, fc, mtms, quiet) for fc in proof_fcs[:6]) if x]
        if ex:
            used.append("export proof")
            body += ["\nYOUR EXPORTS (BU1E + 0 criticals = TCE-proven):"] + ex
            gaps += [f"{fc} has no export proof: TCE status is snapshot-only (say flagged)" for fc in fcs if f"{fc}: in 0 of" in " ".join(ex)]
        elif kc is None or not has(kc, "part"):
            gaps.append("no personal export KB: TCE can only be shown from the rules snapshot, not proven")
    if "price" in intents:
        used.append("export prices")
        pr = [x for x in (sec_price(kc, fc) for fc in fcs[:6]) if x]
        body += ["\nPRICES SEEN IN YOUR EXPORTS (per unit; the rules snapshot carries no prices):"] + (pr or ["  name a feature code to see its price history"])
        gaps.append("prices are history only: the current number comes from a fresh DCSC export (memory and drive prices move fast)")
    gd = [x for x in (sec_guide(kc, fc) for fc in fcs[:6]) if x]
    if gd:
        used.append("guide part tables")
        body += ["\nLENOVO PRESS PART TABLES (guide TCE column is a dated snapshot):"] + gd
    if "spec" in intents and (labels or mtms):
        sp = sec_specs(labels, mtms)
        if sp:
            used.append("platform specs")
            body += ["\nPLATFORM SPECS (Lenovo Press, paraphrased):"] + sp
    if "compete" in intents:
        used.append("competitor map")
        body += ["\nLENOVO COMPETITOR MAP:"] + (sec_compete(q) or ["  no match in the map"])
        gaps.append("for a full competitor BOM, run match on the file (BUILD PATH)")
    if rc and "error" in intents:
        used.append("gating messages")
        g = sec_gates(rc, words + fcs, mtms, 4 if deep else 3)
        body += ["\nDCSC GATING MESSAGES:"] + (g or ["  none matched"])
        if not re.search(r"[\"'“].{12,}[\"'”]|:\s*\S.{15,}", q):
            gaps.append("the exact DCSC error text was not given: ask the user to paste it (it names the conflicting rule)")
    elif rc and {"compat", "tce"} & set(intents) and (words or fcs):
        g = sec_gates(rc, words + fcs, mtms, 2)
        if g:
            used.append("gating messages")
            body += ["\nDCSC GATING MESSAGES:"] + g
    if deep or not f or {"spec", "concept", "lifecycle"} & set(intents):
        d = sec_docs(kc, words + fcs, mtms, 4 if deep else 3)
        if d:
            used.append("Lenovo Press pages")
            body += ["\nLENOVO PRESS PAGES (kb.py page <lp> <page> for the full page):"] + d
    if "lifecycle" in intents:
        gaps.append("internal LOD/LTB dates are Lenovo-internal: customer text says only 'approaching end of sale'")
    if not f and len(used) <= 2 and "concept" not in intents:
        gaps.append("thin brief: try kb.py docs <terms> or ask ... --deep before answering from general knowledge")
    if "concept" in intents and not (fcs or mtms):
        gaps.append("concept question: general knowledge is fine for the concept, Lenovo specifics only from the facts above")
    nxt = ("ask the user first" if any("ask the user" in g or "ask which" in g for g in gaps)
           else "BUILD PATH" if "build" in intents else "answer now (2-6 lines)")
    out.append(f"ROUTE: {'+'.join(intents)} -> used: {', '.join(dict.fromkeys(used))}")
    out.append("GAPS: " + ("; ".join(dict.fromkeys(gaps)) if gaps else "none"))
    out.append(f"NEXT: {nxt}")
    print("\n".join(out + body))
    print(f"\n({time.time() - t0:.2f}s. Deeper: kb.py dfind <MTM> <regex> [--tce|--aix] | rules --fc <FC> | part <FC> | docs <terms> | ask ... --deep)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


