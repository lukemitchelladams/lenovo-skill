#!/usr/bin/env python3
"""Crawl Lenovo Press articles (product guides, reference architectures, ...) to plain text.

usage: python crawl_lenovo_press.py [--limit N] [--only lp1971 [lpNNNN ...]] [--match REGEX]
                                    [--since YYYY-MM-DD] [--kinds lp,ds] [--force] [--update]
                                    [--delay SEC] [--respect-robots] [--dry-run]
  discovery : https://lenovopress.lenovo.com/sitemap.xml (falls back to sitemap_index.xml + its
              sub-sitemaps); keeps /lpNNNN-slug and /dsNNNN-slug urls (--kinds adds tips,redp,sg)
  pages     -> <docs dir>/pages/<id>.txt   article column only (id="contentcol"), tables kept as
                                           "| cell | cell |" rows so part tables stay greppable
  index     -> <docs dir>/pages/INDEX.csv  id,title,url,category,section,date,lastmod,fetched,chars,status
Docs dir defaults to <repo>/docs/lenovo-press; override with env LENOVO_DOCS_DIR.

  --limit N       fetch at most N documents this run (newest ids first)
  --only IDS      just these ids (works for ids missing from the sitemap too)
  --match REGEX   title filter (the url slug stands in for the title until a page is fetched)
  --since DATE    only documents the sitemap says changed on/after DATE
  --force         re-fetch pages already present;  --update  re-fetch only pages whose sitemap
                  lastmod is newer than the stored copy
  --delay SEC     pause between requests (default 1.0); --respect-robots raises it to the site's
                  robots.txt Crawl-delay
  --dry-run       discover and count, fetch nothing

Resumable and non-destructive: a page already on disk is skipped, a failed fetch never touches the
old copy, files are replaced atomically. Then: python kb/build_kb_index.py --docs-only
"""
import argparse, csv, gzip, html, os, re, sys, time, urllib.error, urllib.request
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kb"))
from paths import DOCS_DIR

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE = "https://lenovopress.lenovo.com/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
PAGES_DIR = os.path.join(DOCS_DIR, "pages")
PAGES_INDEX = os.path.join(PAGES_DIR, "INDEX.csv")
COLS = ["id", "title", "url", "category", "section", "date", "lastmod", "fetched", "chars", "status"]
KINDS = ("lp", "ds", "tips", "redp", "sg")
MIN_CHARS = 300  # shorter than this is an empty/redirect page, not an article


# ---------------------------------------------------------------- discovery
def http(url, tries=4, timeout=90):
    """GET with retries. Returns (text, status); text is None on failure."""
    last = "error"
    for n in range(tries):
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": "text/html,application/xml,*/*", "Accept-Language": "en",
            "Accept-Encoding": "gzip"})
        wait = 2 ** (n + 1)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding", "") == "gzip":
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", errors="replace"), "OK"
        except urllib.error.HTTPError as e:
            last = "HTTP %d" % e.code
            if e.code not in (429, 500, 502, 503, 504):
                return None, last
            try:
                wait = min(int(e.headers.get("Retry-After", wait)), 120)
            except (TypeError, ValueError):
                pass
        except Exception as e:
            last = type(e).__name__
        if n < tries - 1:
            time.sleep(wait)
    return None, last


def loc_entries(xml):
    """(loc, lastmod) pairs from a sitemap or sitemap index."""
    out = []
    for blk in re.findall(r"<(?:url|sitemap)>(.*?)</(?:url|sitemap)>", xml, re.S):
        m = re.search(r"<loc>\s*([^<]+?)\s*</loc>", blk)
        if m:
            lm = re.search(r"<lastmod>\s*([^<]+?)\s*</lastmod>", blk)
            out.append((html.unescape(m.group(1)), lm.group(1)[:10] if lm else ""))
    return out


def discover(kinds):
    """{id: {url, lastmod}} for every article url in the sitemap (the refresh-corpus.mjs method)."""
    rx = re.compile(r"^https://lenovopress\.lenovo\.com/((?:%s)\d{3,}[a-z0-9-]*)$" % "|".join(kinds), re.I)
    found = {}
    for sm in ("sitemap.xml", "sitemap_index.xml"):
        xml, _ = http(BASE + sm)
        if not xml:
            continue
        ents = loc_entries(xml)
        subs = [u for u, _ in ents if re.search(r"sitemap[^/]*\.xml$", u, re.I)]
        for s in subs[:10]:
            x2, _ = http(s)
            if x2:
                ents += loc_entries(x2)
        for u, lm in ents:
            m = rx.match(u)
            if not m:
                continue
            i = re.match(r"[a-z]+\d+", m.group(1), re.I).group(0).lower()
            if i not in found or lm > found[i]["lastmod"]:
                found[i] = {"url": u, "lastmod": lm}
        if found:
            break
    return found


def robots_delay():
    txt, _ = http(BASE + "robots.txt", tries=2, timeout=30)
    star = False
    for ln in (txt or "").splitlines():
        k, _, v = ln.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            star = v == "*"
        elif k == "crawl-delay" and star:
            try:
                return float(v)
            except ValueError:
                pass
    return 0.0


def guess_section(title):
    t = title
    if re.search(r"thinkagile|nutanix|vsan|azure|\bHX\d|\bVX\d|\bMX\d|\bFX\d", t, re.I): return "ThinkAgile / SDI"
    if re.search(r"\bSE\d|edge\b", t, re.I): return "Edge"
    if re.search(r"storage|\bDM\d|\bDE\d|\bDG\d|\bD\d{4}\b|tape|\bSAN\b", t, re.I): return "Storage"
    if re.search(r"xclarity|management", t, re.I): return "Systems Management"
    if re.search(r"service|premier|warranty|truscale", t, re.I): return "Value Prop & Services"
    return "Servers"


# ---------------------------------------------------------------- article -> text
def container(h, marker):
    """Depth-balanced inner slice of the <div> whose opening tag matches `marker` (regex)."""
    m = re.search(marker, h)
    if not m:
        return None
    start = h.index(">", m.start()) + 1
    depth = 1
    for t in re.finditer(r"<div\b|</div>", h[start:]):
        depth += -1 if t.group(0) == "</div>" else 1
        if depth == 0:
            return h[start:start + t.start()]
    return h[start:]


SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "template", "iframe"}
BLOCK_TAGS = {"p", "div", "section", "article", "ul", "ol", "dl", "dt", "dd", "pre", "blockquote",
              "figure", "figcaption", "hr", "details", "summary", "address"}
VOID = {"br", "img", "hr", "input", "meta", "link", "wbr", "col", "source"}


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


class Renderer(HTMLParser):
    """HTML fragment -> text. Headings become '## ..', list items '- ..', tables '| a | b |' rows."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.cur = [], []
        self.skip_tag, self.skip_depth = None, 0
        self.tables = []  # stack of {cap, in_cap, rows, row, cell}

    # -- output helpers
    def target(self):
        t = self.tables[-1] if self.tables else None
        if t is not None:
            if t["in_cap"]:
                return t["cap"]
            if t["cell"] is not None:
                return t["cell"]["buf"]
        return self.cur

    def nl(self):
        s = clean("".join(self.cur))
        if s:
            self.lines.append(s)
        self.cur = []

    def blank(self):
        self.nl()
        if self.lines and self.lines[-1] != "":
            self.lines.append("")

    # -- parser events
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip_tag:
            if tag == self.skip_tag and tag not in VOID:
                self.skip_depth += 1
            return
        cls = a.get("class") or ""
        if tag in SKIP_TAGS or (tag == "div" and re.search(r"\bmodal\b", cls)):
            self.skip_tag, self.skip_depth = tag, 1
            return
        t = self.tables[-1] if self.tables else None
        if tag == "table":
            if not self.tables:
                self.blank()
            self.tables.append({"cap": [], "in_cap": False, "rows": [], "row": None, "cell": None})
        elif t is not None and tag == "caption":
            t["in_cap"] = True
        elif t is not None and tag == "tr":
            self.close_cell(t)
            t["row"] = []
            t["rows"].append(t["row"])
        elif t is not None and tag in ("td", "th"):
            self.close_cell(t)
            if t["row"] is None:
                t["row"] = []
                t["rows"].append(t["row"])
            try:
                cs, rs = max(1, int(a.get("colspan") or 1)), max(1, int(a.get("rowspan") or 1))
            except ValueError:
                cs, rs = 1, 1
            t["cell"] = {"buf": [], "cs": min(cs, 40), "rs": min(rs, 40)}
        elif tag == "br":
            (self.cur.append(" ") if self.tables and self.tables[-1]["cell"] is not None else self.nl())
        elif re.fullmatch(r"h[1-6]", tag):
            self.blank()
        elif tag == "li":
            if self.tables:
                self.target().append(" ")
            else:
                self.nl()
                self.cur.append("- ")
        elif tag in BLOCK_TAGS:
            (self.target().append(" ") if self.tables else self.nl())

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth == 0:
                    self.skip_tag = None
            return
        t = self.tables[-1] if self.tables else None
        if tag == "caption" and t is not None:
            t["in_cap"] = False
        elif t is not None and tag in ("td", "th"):
            self.close_cell(t)
        elif t is not None and tag == "tr":
            self.close_cell(t)
            t["row"] = None
        elif tag == "table" and t is not None:
            self.close_cell(t)
            self.tables.pop()
            self.emit_table(t)
        elif re.fullmatch(r"h[1-6]", tag):
            s = clean("".join(self.cur))
            self.cur = []
            if s:
                self.lines.append("#" * int(tag[1]) + " " + s)
            self.blank()
        elif tag in BLOCK_TAGS or tag == "li":
            (self.target().append(" ") if self.tables else self.nl())

    def handle_data(self, data):
        if not self.skip_tag:
            self.target().append(data)

    # -- tables
    def close_cell(self, t):
        c = t["cell"]
        if c is not None:
            t["row"].append({"text": clean("".join(c["buf"])).replace("|", "/"), "cs": c["cs"], "rs": c["rs"]})
            t["cell"] = None

    def emit_table(self, t):
        grid, pending = [], {}  # pending: col -> [text, rows still to fill]
        for row in t["rows"]:
            out, col = [], 0
            for c in row:
                while col in pending:
                    out.append("")
                    pending[col][1] -= 1
                    if pending[col][1] <= 0:
                        del pending[col]
                    col += 1
                out.append(c["text"])
                if c["rs"] > 1:
                    pending[col] = [c["text"], c["rs"] - 1]
                out.extend([""] * (c["cs"] - 1))
                for k in range(1, c["cs"]):
                    if c["rs"] > 1:
                        pending[col + k] = ["", c["rs"] - 1]
                col += c["cs"]
            while col in pending:
                out.append("")
                pending[col][1] -= 1
                if pending[col][1] <= 0:
                    del pending[col]
                col += 1
            while out and out[-1] == "":
                out.pop()
            if out:
                grid.append(out)
        cap = clean("".join(t["cap"]))
        block = ([cap] if cap else []) + ["| " + " | ".join(r) + " |" for r in grid]
        if self.tables:  # nested table: fold into the parent cell as one line
            self.target().append(" ; ".join(block) + " ")
            return
        self.nl()
        self.lines.extend(block)
        self.blank()

    def text(self):
        self.nl()
        return "\n".join(self.lines).strip() + "\n"


def meta_title(page):
    m = (re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', page, re.I)
         or re.search(r"<title>([^<]+)</title>", page, re.I))
    t = html.unescape(m.group(1)) if m else ""
    return clean(re.sub(r"\s*[|>—-]\s*Lenovo\s*Press.*$", "", t, flags=re.I))


MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}


def page_date(page):
    """ISO date of the 'Updated'/'Published' entry in the article sidebar, '' if absent."""
    m = re.search(r'id="meta-published">[^<]*</h5>\s*(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})', page)
    if m and m.group(2).lower() in MONTHS:
        return "%s-%02d-%02d" % (m.group(3), MONTHS[m.group(2).lower()], int(m.group(1)))
    return ""


# boilerplate sections that sit inside the article column on every page (and churn weekly)
DROP_H2 = {"lenovo financial services", "seller training courses", "trademarks"}


def drop_boilerplate(text):
    out, skip = [], False
    for ln in text.split("\n"):
        if ln.startswith("# ") or ln.startswith("## "):
            skip = ln.lstrip("# ").strip().lower() in DROP_H2
        if not skip:
            out.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def extract(page):
    """(title, category, date, text) for one article page; text is scoped to the article column."""
    title = meta_title(page)
    m = re.search(r'static-hero__title">([^<]*)</h1>\s*<h4>([^<]*)</h4>', page)
    cat = clean(html.unescape(m.group(2))) if m else ""
    body = (container(page, r'<div[^>]*id="contentcol"') or container(page, r'<div[^>]*id="content"[^c]')
            or page)
    r = Renderer()
    r.feed(body)
    r.close()
    return title, cat, page_date(page), drop_boilerplate(r.text())


# ---------------------------------------------------------------- index
def read_index():
    if not os.path.exists(PAGES_INDEX):
        return {}
    with open(PAGES_INDEX, newline="", encoding="utf-8-sig") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def write_index(rows):
    os.makedirs(PAGES_DIR, exist_ok=True)
    tmp = PAGES_INDEX + ".part"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: r["id"]))
    os.replace(tmp, PAGES_INDEX)


def save_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------- main
def num(i):
    m = re.search(r"\d+", i)
    return int(m.group(0)) if m else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Crawl Lenovo Press articles to text for the KB doc index.")
    ap.add_argument("--limit", type=int, metavar="N", help="fetch at most N documents this run")
    ap.add_argument("--only", nargs="+", metavar="ID", help="fetch only these ids, e.g. --only lp1971")
    ap.add_argument("--match", metavar="REGEX", help="only documents whose title matches (case-insensitive)")
    ap.add_argument("--since", metavar="YYYY-MM-DD", help="only documents changed on/after this date (sitemap lastmod)")
    ap.add_argument("--kinds", default="lp,ds", help="id prefixes to crawl, from %s (default lp,ds)" % ",".join(KINDS))
    ap.add_argument("--force", action="store_true", help="re-fetch pages already present")
    ap.add_argument("--update", action="store_true", help="re-fetch pages whose sitemap lastmod is newer than the stored copy")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1.0)")
    ap.add_argument("--respect-robots", action="store_true", help="wait at least the robots.txt Crawl-delay")
    ap.add_argument("--dry-run", action="store_true", help="discover and count only")
    a = ap.parse_args(argv)

    kinds = [k.strip().lower() for k in a.kinds.split(",") if k.strip()]
    bad = [k for k in kinds if k not in KINDS]
    if bad:
        sys.exit("unknown --kinds: %s (choose from %s)" % (",".join(bad), ",".join(KINDS)))
    if a.since and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.since):
        sys.exit("--since wants YYYY-MM-DD")
    rx = re.compile(a.match, re.I) if a.match else None

    found = discover(kinds)
    if not found:
        sys.exit("could not read the sitemap from %s (offline? blocked?). Nothing changed." % BASE)
    per = {}
    for i in found:
        per[re.match(r"[a-z]+", i).group(0)] = per.get(re.match(r"[a-z]+", i).group(0), 0) + 1
    print("discovered %d documents (%s)" % (len(found), ", ".join("%s %d" % kv for kv in sorted(per.items()))))

    have = read_index()
    todo = []
    want = [x.lower() for x in a.only] if a.only else None
    if want:
        for i in want:
            if not re.fullmatch(r"[a-z]+\d+", i):
                sys.exit("bad id %r (want e.g. lp1971)" % i)
            found.setdefault(i, {"url": BASE + i, "lastmod": ""})
        ids = want
    else:
        ids = sorted(found, key=num, reverse=True)
    for i in ids:
        d = found[i]
        title = (have.get(i) or {}).get("title") or re.sub(r"^[a-z]+\d+-?", "", d["url"].rsplit("/", 1)[-1]).replace("-", " ")
        if rx and not rx.search(title):
            continue
        if a.since and (d["lastmod"] or "0000") < a.since:
            continue
        path = os.path.join(PAGES_DIR, i + ".txt")
        present = os.path.exists(path) and os.path.getsize(path) > 0
        old = have.get(i) or {}
        stale = bool(a.update and present and d["lastmod"] and d["lastmod"] > (old.get("lastmod") or ""))
        if present and not (a.force or stale):
            continue
        todo.append((i, d))
    skipped = len(ids) - len(todo)
    if a.limit is not None:
        todo = todo[:max(0, a.limit)]
    print("selected %d to fetch (%d already present or filtered out)" % (len(todo), skipped))

    delay = a.delay
    rd = robots_delay()
    if rd > delay:
        if a.respect_robots:
            delay = rd
            print("robots.txt Crawl-delay: %g s - honoring it (%d docs ~ %.1f h)" % (rd, len(todo), len(todo) * rd / 3600))
        else:
            print("note: robots.txt asks for Crawl-delay %g s; using --delay %g. Add --respect-robots to honor it." % (rd, delay))
    if a.dry_run:
        for i, d in todo[:10]:
            print("  %-8s %s %s" % (i, d["lastmod"], d["url"]))
        if len(todo) > 10:
            print("  ... %d more" % (len(todo) - 10))
        return 0

    ok = fail = empty = 0
    today = time.strftime("%Y-%m-%d")
    try:
        for n, (i, d) in enumerate(todo, 1):
            t0 = time.time()
            page, st = http(d["url"])
            if page is None:
                fail += 1
                print("  %-8s FAIL %s" % (i, st))
            else:
                title, cat, date, text = extract(page)
                if len(text) < MIN_CHARS:
                    empty += 1
                    print("  %-8s EMPTY (%d chars), kept old copy if any" % (i, len(text)))
                else:
                    head = "%s\n%s\n%s\n\n" % (title, d["url"], " | ".join(x for x in (cat, ("Updated " + date) if date else "", i) if x))
                    save_text(os.path.join(PAGES_DIR, i + ".txt"), head + text)
                    have[i] = dict(id=i, title=title, url=d["url"], category=cat, section=guess_section(title),
                                   date=date, lastmod=d["lastmod"], fetched=today, chars=len(text), status="OK")
                    ok += 1
                    print("  %-8s ok  %7.1f KB  %s" % (i, len(text) / 1024, title[:70]))
            if n % 25 == 0:
                write_index(have)
            if n < len(todo):
                time.sleep(max(0.0, delay - (time.time() - t0)))
    except KeyboardInterrupt:
        print("\ninterrupted - progress is saved, rerun to resume")
    finally:
        if ok:
            write_index(have)
    print("\nFETCHED: %d ok, %d failed, %d empty   (pages on disk: %d)" % (
        ok, fail, empty, len([f for f in os.listdir(PAGES_DIR) if f.endswith(".txt")]) if os.path.isdir(PAGES_DIR) else 0))
    print("INDEX: " + PAGES_INDEX)
    print("next: python kb/build_kb_index.py --docs-only")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
