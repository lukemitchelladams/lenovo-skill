"""DCSC configurator RULES (not configs): required sections, single-entry sections, min/max and legal
quantities, per-section TCE flags, withdraw dates, the complete option list per MTM, and the gating
messages DCSC emits.

The data file kb/data/dcsc-rules.json.gz ships with the repo. Prices were stripped at build time.
It is a snapshot of each MTM's DEFAULT configuration state on the crawl date:
  - legal quantities change as other selections change, so q=[0] means 'not selectable in the
    default state', NOT 'illegal'
  - TCE flags are PER SECTION and rotate; only BU1E in a live export proves TCE
Always confirm in the live DCSC configurator.

usage:
  python dcsc_rules.py rules <MTM|model> [--required] [--section <regex>] [--tce]
  python dcsc_rules.py rules --fc <FC>           every MTM/section holding a feature code
  python dcsc_rules.py find <MTM|model> <regex> [--tce]   search the COMPLETE option list of an MTM
  python dcsc_rules.py gates <regex> [--sev critical|warning|normal]
  python dcsc_rules.py models [regex] | --retired   MTMs in the snapshot, or CTOs DCSC has retired
  python dcsc_rules.py build <launch.json> <static.json> [<kb.sqlite>]   maintainer only: regenerate the data file
"""
import gzip, json, os, re, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "dcsc-rules.json.gz")
SEVS = ("critical", "error", "warning", "normal", "info")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load():
    if not os.path.exists(DATA):
        sys.exit(f"missing {DATA}")
    with gzip.open(DATA, "rt", encoding="utf-8") as f:
        return json.load(f)


def resolve(db, q):
    q = q.strip().upper()
    if q in db["models"]:
        return [q]
    toks = re.sub(r"[^A-Z0-9]+", " ", q).split()
    hits = sorted(m for m, v in db["models"].items() if all(t in re.sub(r"[^A-Z0-9]+", " ", v["name"].upper()).split() for t in toks))
    if len(hits) > 1:  # prefer the plain base model over DWC / Workstation / SAP HANA / AI variants
        base = [m for m in hits if re.search(r"base warranty", db["models"][m]["name"], re.I)
                and not re.search(r"dwc|workstation|hana|for ai|neptune|water|storage|robo", db["models"][m]["name"], re.I)]
        if len(base) == 1:
            print("(also: " + ", ".join(f"{m} {db['models'][m]['name']}" for m in hits if m != base[0]) + ")\n")
            return base
    return hits


def fmt_q(q):
    if not q:
        return "-"
    return ",".join(map(str, q)) if len(q) <= 8 else f"{q[0]}..{q[-1]} ({len(q)} values)"


def rules(db, args):
    if "--fc" in args:
        fc = args[args.index("--fc") + 1].upper()
        n = 0
        for mtm, m in sorted(db["models"].items()):
            legal = {(s["n"], f[0]): f[4] for s in m["secs"] for f in s["f"]}
            for tab, sub, sec, c, d, mn, mx, tc, wd, ty in options(db, mtm):
                if c == fc:
                    n += 1
                    q = legal.get((sec, c))
                    print(f"{mtm}  {m['name'][:34]:<34} {tab}/{sec[:28]:<28} tce={'Y' if tc else '-'} min={mn} max={mx}"
                          f"{' q=' + fmt_q(q) if q is not None else ''}{'  withdrawn ' + wd if wd else ''}")
        print(f"{fc}: {n} section entries" if n else f"{fc}: not in the rules snapshot")
        return
    if not args:
        print(__doc__); return
    mtms = resolve(db, args[0])
    if len(mtms) != 1:
        print("matches: " + (", ".join(f"{x} ({db['models'][x]['name']})" for x in mtms[:20]) or "none")); return
    mtm = mtms[0]; m = db["models"][mtm]
    req = "--required" in args; tce_only = "--tce" in args
    rx = re.compile(args[args.index("--section") + 1], re.I) if "--section" in args else None
    print(f"{mtm}  {m['name']}  ({len(m['secs'])} sections, snapshot {db['meta']['crawled']})\n")
    for s in m["secs"]:
        if req and not s["req"]:
            continue
        if rx and not rx.search(s["n"] + " " + s["tab"] + " " + s["sub"]):
            continue
        feats = [f for f in s["f"] if f[5] or not tce_only]
        if tce_only and not feats:
            continue
        flags = (" REQUIRED" if s["req"] else "") + (" single-entry" if s["single"] else "")
        print(f"--- {s['tab']} / {s['sub']} / {s['n']}{flags}")
        if rx or not req:
            for c, d, mn, mx, q, tc, wd in feats:
                print(f"    {c:<6} tce={'Y' if tc else '-'} min={mn} max={mx} q={fmt_q(q):<14} {d[:70]}{'  [withdrawn ' + wd + ']' if wd else ''}")


def options(db, mtm):
    """Complete option list for an MTM (static catalog layer), falling back to the default-state sections."""
    m = db["models"][mtm]
    if m.get("opts"):
        return m["opts"]
    return [[s["tab"], s["sub"], s["n"], c, d, mn, mx, tc, wd, ""] for s in m["secs"] for c, d, mn, mx, q, tc, wd in s["f"]]


def find(db, mtm_q, pat, tce_only=False):
    rx = re.compile(pat, re.I)
    for mtm in resolve(db, mtm_q)[:6]:
        n = 0
        for tab, sub, sec, c, d, mn, mx, tc, wd, ty in options(db, mtm):
            if (rx.search(d) or rx.search(c)) and (tc or not tce_only):
                n += 1
                print(f"{mtm} {sec[:28]:<28} {c:<6} tce={'Y' if tc else '-'} max={mx if mx is not None else '-':<3} {d[:74]}{'  [withdrawn ' + wd + ']' if wd else ''}")
        print(f"-- {n} options matched on {mtm} (complete option list, snapshot {db['meta']['crawled']})")


def gates(db, args):
    sev = None
    if "--sev" in args:
        i = args.index("--sev"); sev = args[i + 1].lower(); args = args[:i] + args[i + 2:]
    rx = re.compile(" ".join(args), re.I) if args else None
    n = 0
    for g in db["gates"]:
        if sev and g["sev"].lower() != sev:
            continue
        if rx and not rx.search(g["text"]):
            continue
        n += 1
        print(f"[{g['sev']}] x{g['n']}  {', '.join(g['mtms'][:6])}{' ...' if len(g['mtms']) > 6 else ''}\n    {g['text']}\n")
    print(f"{n} gating rules matched")


def models(db, pat=None):
    if pat == "--retired":
        rt = db["meta"].get("retired", [])
        print(f"{len(rt)} CTOs DCSC no longer opens for configuration ('Not found CTO') as of {db['meta']['crawled']}:")
        for r in rt:
            print(f"  {r['mtm']}  {r['name']}")
        return
    rx = re.compile(pat, re.I) if pat else None
    for mtm, m in sorted(db["models"].items(), key=lambda x: x[1]["name"]):
        if rx and not rx.search(m["name"] + " " + mtm):
            continue
        print(f"{mtm}  {m['name']}")


def build(launch_p, static_p, kb_p=None):
    launch = json.load(open(launch_p, encoding="utf-8"))
    static = json.load(open(static_p, encoding="utf-8"))
    names = {x["mtm"]: x.get("name") or "" for x in launch.get("models", [])}
    wd, opts = {}, {}
    for mtm, cats in static["data"].items():
        seen = set()
        for cat, feats in cats.items():
            for f in feats:
                w = f["wd"][:10] if f.get("wd") and f["wd"][:4] < "2099" else ""  # DCSC uses 2999-12-31 for 'not withdrawn'
                if w:
                    wd[(mtm, f["c"])] = w
                k = (f.get("s"), f["c"])
                if k in seen:
                    continue
                seen.add(k)
                # complete option list: [tab, sub, section, fc, descr, min, max, tce, withdrawn, type]
                opts.setdefault(mtm, []).append([cat, f.get("t", ""), f.get("s", ""), f["c"], f.get("d", ""), f.get("mn"),
                                                 f.get("mx"), f.get("tc", 0), w, f.get("ty", "")])
    out = {}
    for mtm, m in launch["data"].items():
        secs = []
        for s in m["secs"]:
            secs.append({"tab": s["tab"], "sub": s["sub"], "n": s["n"], "req": s["req"], "single": s["single"],
                         "f": [[f["c"], f.get("d", ""), f.get("mn"), f.get("mx"), f.get("q") or [], f.get("tc", 0),
                                wd.get((mtm, f["c"]), "")] for f in s["f"]]})
        out[mtm] = {"name": names.get(mtm) or m.get("desc") or "", "secs": secs, "opts": opts.get(mtm, [])}
    gl = []
    if kb_p:
        cx = sqlite3.connect(f"file:{kb_p}?mode=ro", uri=True)
        rows = cx.execute("SELECT m.severity, m.text, c.mtm, c.name FROM msg m JOIN config c ON c.id=m.cfg").fetchall()
        # DCSC prefixes every message with the configuration name, which carries customer names. Strip the
        # prefix, then drop any message whose body still contains a word from a configuration or export name,
        # unless that word is generic (it appears in message bodies of 3+ different configurations).
        tok = lambda s: {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", s)}
        parsed, spread = [], {}
        for sev, text, mtm, fname in rows:
            if (sev or "").lower() not in SEVS or not text:
                continue
            head, sep, body = text.partition(": ")
            body = EMAIL.sub("<Lenovo sales configuration support>", (body if sep else text).strip())
            owner = (head if sep else "") + "|" + (fname or "")
            parsed.append((sev.title(), body, mtm, owner))
            for w in tok(body):
                spread.setdefault(w, set()).add(owner)
        generic = {w for w, s in spread.items() if len(s) >= 3}
        generic |= {w for w in spread if re.fullmatch(r"(sr|st|hx|vx|mx|fx|de|dm|dg|ds|se)\d+[a-z]?|[a-z]\d{2,}[a-z]?", w)}
        generic |= {"swap", "replacement", "example"}  # reviewed 2026-09-30: plain words, not names
        leak = set()
        for *_, owner in parsed:
            leak |= tok(owner.replace("|", " "))
        leak -= generic
        bag, dropped = {}, []
        for sev, body, mtm, owner in parsed:
            hit = tok(body) & leak
            if hit:
                dropped.append((sev, body, sorted(hit)))
                continue
            g = bag.setdefault((sev, body), {"mtms": set(), "n": 0})
            g["n"] += 1
            if mtm:
                g["mtms"].add(mtm)
        # stored messages were cut at a fixed length, so stripping names of different lengths leaves truncated
        # copies of the same message: fold each into the longest message it is a prefix of
        keep = {}
        for (s, b), g in sorted(bag.items(), key=lambda x: -len(x[0][1])):
            base = next((k for k in keep if k[0] == s and k[1].startswith(b)), None)
            if base:
                keep[base]["n"] += g["n"]; keep[base]["mtms"] |= g["mtms"]
            else:
                keep[(s, b)] = {"n": g["n"], "mtms": set(g["mtms"])}
        gl = [{"sev": s, "text": b, "mtms": sorted(g["mtms"]), "n": g["n"]} for (s, b), g in sorted(keep.items(), key=lambda x: -x[1]["n"])]
        uniq_drop = {(s, b): h for s, b, h in dropped}
        print(f"gates: {len(gl)} kept, {len(uniq_drop)} distinct messages dropped for possible name leaks")
        if os.environ.get("DCSC_RULES_DROPLOG"):
            with open(os.environ["DCSC_RULES_DROPLOG"], "w", encoding="utf-8") as f:
                for (s, b), h in uniq_drop.items():
                    f.write(f"[{s}] {h} :: {b[:200]}\n")
    prev = {}
    if os.path.exists(DATA):  # keep names for CTOs that DCSC no longer opens (launch 404 on the crawl)
        try:
            with gzip.open(DATA, "rt", encoding="utf-8") as f:
                p = json.load(f)
            prev = {m: v.get("name", "") for m, v in p.get("models", {}).items()}
            prev.update({r["mtm"]: r["name"] for r in p.get("meta", {}).get("retired", []) if isinstance(r, dict)})
        except Exception:
            pass
    retired = [dict(mtm=m, name=prev.get(m, "")) for m in launch["meta"].get("retired", []) if m not in out]
    meta = {"crawled": launch["meta"].get("crawledAt", "")[:10], "source": "DCSC launch + static rules snapshot, prices removed",
            "retired": retired,
            "note": "Default-state snapshot. q = legal quantities in the default state ([0] = not selectable in that state, not illegal). "
                    "TCE flags are per section and rotate. Confirm in live DCSC."}
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with gzip.open(DATA, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump({"meta": meta, "models": out, "gates": gl}, f, separators=(",", ":"))
    print(f"models={len(out)} features={sum(len(s['f']) for m in out.values() for s in m['secs'])} "
          f"withdraw_dates={len(wd)} -> {DATA} ({os.path.getsize(DATA) / 1e6:.2f} MB)")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return
    c, a = argv[0], argv[1:]
    if c == "build":
        build(*a[:3]); return
    db = load()
    if c == "rules": rules(db, a)
    elif c == "find" and len(a) >= 2:
        t = "--tce" in a
        a = [x for x in a if x != "--tce"]
        find(db, a[0], " ".join(a[1:]), t)
    elif c == "gates": gates(db, a)
    elif c == "models": models(db, a[0] if a else None)
    else: print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
