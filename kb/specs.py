"""
Platform hardware specs (sockets, DIMM slots, drive bays, PCIe/OCP, GPU, PSU),
paraphrased from Lenovo Press product guides. Data: kb/data/platform-specs.json.

usage:
  python specs.py spec <name or MTM>   e.g. "sr630 v4", "HX650 V4 Storage", 7DG9CTO1WW, 7DG9
  python specs.py spec --list          every platform, one line each

A bare machine type (7DGD) can be shared by two platforms (SR650 V4 / SR650a V4);
every match is printed. Always confirm against the guide named in `source`.
"""
import difflib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "platform-specs.json")
_cache = None
_BRAND = re.compile(r"thinksystem|thinkagile|thinkedge|lenovo", re.I)
_MTM = re.compile(r"^7[A-Z0-9]{3}(CTO[0-9A-Z]{1,2}(WW)?)?$")

def load():
    global _cache
    if _cache is None:
        with open(DATA, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache

def platforms():
    return load()["platforms"]

def _n(s):
    return re.sub(r"[^a-z0-9]", "", _BRAND.sub("", s or "").lower())

def _names(p):
    return {_n(p["name"])} | {_n(a) for a in p.get("aliases", [])}

def find(query):
    """All platforms matching a name (fuzzy) or an MTM / 4-char machine type."""
    q = (query or "").strip()
    if not q:
        return []
    u = q.upper().replace(" ", "")
    if _MTM.match(u):
        exact = [p for p in platforms() if u in p["mtms"]]
        if exact:
            return exact
        return [p for p in platforms() if u[:4] in p.get("machine_types", {}) or any(m[:4] == u[:4] for m in p["mtms"])]
    qn = _n(q)
    if not qn:
        return []
    exact = [p for p in platforms() if qn in _names(p)]
    if exact:
        return exact
    part = [p for p in platforms() if any(qn in nm for nm in _names(p))]
    if part:
        return part
    best = difflib.get_close_matches(qn, sorted({nm for p in platforms() for nm in _names(p)}), n=3, cutoff=0.7)
    rank = lambda p: min(best.index(nm) for nm in _names(p) if nm in best)
    return sorted((p for p in platforms() if any(nm in best for nm in _names(p))), key=rank)

def resolve(mtm=None, name=None):
    """One platform or None. Ambiguous (shared machine type) resolves to None."""
    for q in (mtm, name):
        if q:
            hits = find(q)
            if len(hits) == 1:
                return hits[0]
    return None

def _kv(label, val):
    return f"  {label:<12}{val}" if val not in (None, "", []) else None

def render(p):
    m, d, x, psu = p["memory"], p["drives"], p["pcie"], p["psu"]
    s = p["sockets"]
    sock = str(s["min"]) if s["min"] == s["max"] else f"{s['min']}-{s['max']}"
    ch = f"{m['channels_per_cpu']}ch x {m['dimms_per_channel']} DPC" if m.get("channels_per_cpu") else ""
    mem = f"{m['dimm_slots_total']} slots ({m['dimm_slots_per_socket']}/socket{', ' + ch if ch else ''}), up to {m['max_speed_mts']} MT/s"
    if m.get("max_capacity"): mem += f", max {m['max_capacity']}"
    bays = f"front max {d['max_front_bays_2_5']}x 2.5\", " + (f"{d['max_front_bays_3_5']}x 3.5\"" if d["supports_3_5"] else "no 3.5\" front bays")
    ocp = "unconfirmed" if x.get("ocp_slots") is None else x["ocp_slots"]
    mt = ", ".join(f"{k} ({v})" if v else k for k, v in p.get("machine_types", {}).items())
    out = [f"{p['name']}  ({p['form_factor']})  [{p['source']}, as of {p['as_of']}]",
           _kv("MTMs", " ".join(p["mtms"])), _kv("Mach types", mt),
           _kv("Sockets", sock + (f"  (HCI min {p['hci_min_cpus']} CPU)" if p.get("hci_min_cpus") else "")),
           _kv("CPU", p.get("cpu")), _kv("Memory", mem), _kv("", m.get("notes")),
           _kv("Drives", bays)]
    out += [f"  {'':<12}- {o}" for o in d.get("options", [])]
    out += [_kv("", d.get("notes")),
            _kv("PCIe", f"up to {x['slots_max']} slots + {ocp} OCP" + (f"  ({x['notes']})" if x.get("notes") else "")),
            _kv("PSU", f"{psu['bays']} bays. {psu.get('notes') or ''}".strip()),
            _kv("GPU", p.get("gpu"))]
    out += [_kv("Note", n) for n in p.get("notes", [])]
    out.append(f"  https://lenovopress.lenovo.com/{p['source']}")
    return "\n".join(l for l in out if l)

def listing():
    print(f"{'platform':<26}{'form':<28}{'CPU':>4}{'DIMM':>6}{'2.5f':>6}{'3.5f':>6}{'PCIe':>6}{'OCP':>5}  {'source':<8}{'as of'}")
    for p in platforms():
        s, d = p["sockets"], p["drives"]
        sock = str(s["min"]) if s["min"] == s["max"] else f"{s['min']}-{s['max']}"
        ocp = "?" if p["pcie"].get("ocp_slots") is None else p["pcie"]["ocp_slots"]
        print(f"{p['name']:<26}{p['form_factor'][:26]:<28}{sock:>4}{p['memory']['dimm_slots_total']:>6}"
              f"{d['max_front_bays_2_5']:>6}{d['max_front_bays_3_5']:>6}{p['pcie']['slots_max']:>6}{ocp:>5}  {p['source']:<8}{p['as_of']}")
    print(f"\n{len(platforms())} platforms; 'spec <name or MTM>' for the full record")

def main(argv):
    for s in (sys.stdout, sys.stderr):
        try: s.reconfigure(encoding="utf-8", errors="replace")
        except Exception: pass
    a = list(argv)
    if not a or a[0] in ("-h", "--help", "help") or a[0] != "spec":
        print(__doc__); return 0 if not a or a[0] in ("-h", "--help", "help") else 2
    q = a[1:]
    if q == ["--list"]:
        listing(); return 0
    if not q:
        print(__doc__); return 2
    hits = find(" ".join(q))
    if not hits:
        print(f"no platform matched: {' '.join(q)}\nknown: " + ", ".join(p["name"] for p in platforms()), file=sys.stderr)
        return 1
    if len(hits) > 1:
        print(f"{len(hits)} platforms match '{' '.join(q)}':\n")
    print("\n\n".join(render(p) for p in hits))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
