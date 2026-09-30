#!/usr/bin/env python3
"""Fetch the Lenovo Press documents the KB indexes, from lenovopress.lenovo.com.

usage: python get_lenovo_docs.py [--force] [--only lp2165 [lpNNNN ...]]
  PDFs   -> <docs dir>/pdf/<id>.pdf
  pages  -> <docs dir>/html/<id>.html   (live-database refs that have no PDF)
  index  -> <docs dir>/INDEX.csv        (id,category,title,url,bytes,status)
Docs dir defaults to <repo>/docs/lenovo-press; override with env LENOVO_DOCS_DIR.
Files already present are skipped unless --force. Then: python kb/build_kb_index.py --docs-only
"""
import argparse, csv, os, sys, time, urllib.request
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kb"))
from paths import DOCS_DIR, PDF_DIR, HTML_DIR, INDEX_CSV

BASE = "https://lenovopress.lenovo.com/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")

# (id, category, title)
DOCS = [
    # --- V4 Intel servers ---
    ("lp1971", "Server V4", "ThinkSystem SR630 V4 Server Product Guide"),
    ("lp2127", "Server V4", "ThinkSystem SR650 V4 Server Product Guide"),
    ("lp2128", "Server V4", "ThinkSystem SR650a V4 Server Product Guide"),
    ("lp2231", "Server V4", "ThinkSystem SR860 V4 Server Product Guide"),
    ("lp2165", "Server V4", "Introducing the ThinkSystem V4 Servers with Intel Xeon 6"),
    # --- V3 AMD servers ---
    ("lp1607", "Server V3 AMD", "ThinkSystem SR645 V3 Server Product Guide"),
    ("lp1608", "Server V3 AMD", "ThinkSystem SR665 V3 Server Product Guide"),
    ("lp1609", "Server V3 AMD", "ThinkSystem SR635 V3 Server Product Guide"),
    ("lp1610", "Server V3 AMD", "ThinkSystem SR655 V3 Server Product Guide"),
    ("lp1665", "Server V3 AMD", "ThinkSystem V3 Servers with 4th Gen AMD EPYC"),
    ("lp1729", "Server V3", "ThinkSystem SR950 V3 Server Product Guide"),
    # --- Entry servers ---
    ("lp1802", "Server entry", "ThinkSystem SR250 V3 Server Product Guide"),
    ("lp1803", "Server entry", "ThinkSystem ST250 V3 Server Product Guide"),
    # --- ThinkAgile SDI ---
    ("lp2132", "ThinkAgile", "ThinkAgile HX630 V4 Hyperconverged System Product Guide"),
    ("lp2133", "ThinkAgile", "ThinkAgile HX650 V4 Hyperconverged System Product Guide"),
    ("lp2134", "ThinkAgile", "ThinkAgile VX630 V4 Hyperconverged System Product Guide"),
    ("lp2136", "ThinkAgile", "ThinkAgile MX630 V4 Hyperconverged System Product Guide"),
    ("lp2137", "ThinkAgile", "ThinkAgile MX650 V4 Hyperconverged System Product Guide"),
    ("lp2337", "ThinkAgile", "ThinkAgile FX630 V4 Hyperconverged System Product Guide"),
    ("lp1649", "ThinkAgile", "ThinkAgile HX665 V3 IS/CN and HX665 V3 Storage IS/CN"),
    ("lp0665", "ThinkAgile", "Reference Architecture for Workloads using Lenovo ThinkAgile HX and FX Series"),
    # --- Storage ---
    ("lp1793", "Storage", "ThinkSystem DM3010H Product Guide"),
    ("lp1681", "Storage", "ThinkSystem D4390 Direct Attached Storage Enclosure"),
    ("lp2071", "Storage", "ThinkSystem DE4200H Hybrid Storage Array Product Guide"),
    ("lp2075", "Storage", "ThinkSystem DM3200F, DM5200F, DM7200F Unified Storage"),
    ("lp0941", "Storage", "ThinkSystem DM Series Unified Storage Arrays"),
    # --- Drives / SSD ---
    ("lp1261", "Drives", "Lenovo ThinkSystem SSD Portfolio"),
    ("lp2257", "Drives", "Vendor Agnostic Mixed Use NVMe SSDs (3 DWPD)"),
    ("lp2256", "Drives", "Vendor Agnostic Read Intensive NVMe SSDs (1 DWPD)"),
    ("lp2191", "Drives", "Vendor Agnostic Read Intensive 6Gb SATA SSDs"),
    ("lp1905", "Drives", "CD8P Mixed Use NVMe PCIe 5.0 SSDs"),
    ("lp1904", "Drives", "CD8P Read Intensive NVMe PCIe 5.0 SSDs"),
    ("lp1712", "Drives", "PM1743 Read Intensive NVMe PCIe 5.0 SSDs"),
    ("lp2367", "Drives", "SN861 Read Intensive NVMe PCIe 5.0 SSDs"),
    ("lp2160", "Drives", "PS1010 Read Intensive NVMe PCIe 5.0 x4 SSDs"),
    ("lp1590", "Drives", "7450 PRO Read Intensive NVMe PCIe 4.0 SSDs"),
    ("lp2078", "Drives", "Solidigm P5620 Mixed Use NVMe PCIe 4.0 SSDs"),
    # --- Controllers / options ---
    ("lp1288", "Controllers", "ThinkSystem RAID Adapter and HBA Reference"),
    ("lp1282", "Controllers", "ThinkSystem RAID 940 Series Internal RAID Adapters"),
    ("lp1552", "Controllers", "ThinkSystem RAID 540/545 PCIe Gen4 12Gb Adapters"),
    ("lp1838", "Options", "ThinkSystem and ThinkEdge Rail Kit Reference"),
    # --- Solutions / trust ---
    ("lp2421", "Solutions", "Nutanix Cloud Infrastructure on ThinkSystem"),
    ("lp1434", "Trust", "Intel Transparent Supply Chain"),
    ("lp1116", "Trust", "Lenovo Security by Design"),
]

COLS = ["id", "category", "title", "url", "bytes", "status"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def get_doc(doc_id, force):
    pdf = os.path.join(PDF_DIR, doc_id + ".pdf")
    html = os.path.join(HTML_DIR, doc_id + ".html")
    if not force:
        for path, status in ((pdf, "OK"), (html, "OK-HTML")):
            if os.path.exists(path):
                return os.path.getsize(path), status, True
    body, err = None, None
    for attempt in (1, 2):
        try:
            body = fetch(BASE + doc_id + ".pdf")
            break
        except Exception as e:
            err = e
            time.sleep(2)
    if body is None:
        raise err
    if body[:4] == b"%PDF":
        path, status = pdf, "OK"
    else:
        # live-database reference: no PDF exists, keep the web page itself
        body, path, status = fetch(BASE + doc_id), html, "OK-HTML"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(body)
    os.replace(tmp, path)
    return len(body), status, False


def main():
    ap = argparse.ArgumentParser(description="Download Lenovo Press docs for the KB doc index.")
    ap.add_argument("--force", action="store_true", help="re-download files already present")
    ap.add_argument("--only", nargs="+", metavar="ID", help="fetch only these ids, e.g. --only lp2165")
    a = ap.parse_args()

    docs = DOCS
    if a.only:
        want = [x.lower() for x in a.only]
        bad = [x for x in want if x not in {d[0] for d in DOCS}]
        if bad:
            sys.exit("unknown doc id(s): " + ", ".join(bad))
        docs = [d for d in DOCS if d[0] in want]

    results = {}
    if a.only and os.path.exists(INDEX_CSV):  # partial run: keep the rest of the index
        with open(INDEX_CSV, newline="", encoding="utf-8-sig") as f:
            results = {r["id"]: r for r in csv.DictReader(f)}
    fresh = {}
    for doc_id, cat, title in docs:
        url = BASE + doc_id
        try:
            size, status, skipped = get_doc(doc_id, a.force)
            print(f"  {doc_id}  {status}  {size/1048576:6.1f} MB{'  (already present)' if skipped else ''}")
        except Exception as e:
            size, status = 0, "FAIL: " + str(e)[:60]
            print(f"  {doc_id}  {status}")
        fresh[doc_id] = dict(id=doc_id, category=cat, title=title, url=url, bytes=size, status=status)
    results.update(fresh)

    os.makedirs(DOCS_DIR, exist_ok=True)
    rows = sorted(results.values(), key=lambda r: (r["category"], r["id"]))
    with open(INDEX_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in fresh.values() if r["status"].startswith("OK")]
    bad = [r for r in fresh.values() if not r["status"].startswith("OK")]
    print(f"\nDOWNLOADED : {len(ok)} of {len(docs)}")
    print(f"TOTAL SIZE : {sum(int(r['bytes']) for r in ok)/1048576:.1f} MB\n")
    if bad:
        print("FAILED:")
        for r in bad:
            print(f"   {r['id']}  {r['title']}  -> {r['status']}")
        print()
    print(f"INDEX: {INDEX_CSV}")
    for cat, n in sorted(Counter(r["category"] for r in ok).items()):
        print(f"   {cat:<14} {n}")
    print("\nnext: python kb/build_kb_index.py --docs-only")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
