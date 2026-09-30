#!/usr/bin/env python3
'''Lenovo's official competitor map: which Lenovo product answers which Dell / HPE / Supermicro / ... box.

Source: https://lenovopress.lenovo.com/compare_competitor_map.json (public, no login; Lenovo Press keeps it
current). Cached in <docs dir>/compete_map.json for 24 h; offline runs fall back to the cache.

usage:
  python compete.py <competitor text>          competitor -> Lenovo products:  'Dell R760', 'PowerEdge R760xs',
                                               'HPE DL380 Gen11', 'NX-8170', 'Supermicro SYS-221H'
  python compete.py --lenovo <text> [--vs MFR] Lenovo -> its competitors, grouped by maker:  'SR630 V4', 'HX650'
  python compete.py --list [manufacturer]      makers with product counts, or every product of one maker
  add --refresh to any of them to re-download the map now
Matching is token based and forgiving: vendor words (dell, hp, hpe, smc, ...) filter the maker, model tokens
match exactly or as a prefix (R760 finds R760, R760xs, R760xa), 'dl 380' and 'dl380' are the same.
The map is Lenovo's marketing pairing, not a feature-parity guarantee: compare the specs before you quote.
'''
import argparse, gzip, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from paths import DOCS_DIR

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

URL = 'https://lenovopress.lenovo.com/compare_competitor_map.json'
CACHE = os.path.join(DOCS_DIR, 'compete_map.json')
TTL = 24 * 3600
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/124.0.0.0 Safari/537.36')
ALIAS = {'hp': 'hpe', 'hewlett': 'hpe', 'packard': 'hpe', 'smc': 'supermicro', 'pure': 'everpure',
         'purestorage': 'everpure', 'ieit': 'inspur', 'atos': 'atos', 'eviden': 'atos', 'ucs': 'cisco'}


# ---------------------------------------------------------------- data
def cl(s):
    '''display form: NBSP / zero-width junk out, one space between words'''
    return re.sub(r'\s+', ' ', re.sub('[​-‍﻿�]', '', (s or '').replace('\xa0', ' '))).strip()


def fetch():
    req = urllib.request.Request(URL, headers={'User-Agent': UA, 'Accept': 'application/json',
                                               'Accept-Encoding': 'gzip'})
    last = None
    for n in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                if r.headers.get('Content-Encoding', '') == 'gzip':
                    raw = gzip.decompress(raw)
            data = json.loads(raw.decode('utf-8'))
            if not (isinstance(data, list) and data and 'product_name' in data[0]):
                raise ValueError('unexpected JSON shape')
            return raw
        except Exception as e:
            last = e
            time.sleep(2 * (n + 1))
    raise last


def load(refresh=False):
    '''(map, note). Fresh cache > download > stale cache.'''
    age = time.time() - os.path.getmtime(CACHE) if os.path.exists(CACHE) else None
    if age is not None and age < TTL and not refresh:
        return json.load(open(CACHE, encoding='utf-8')), None
    try:
        raw = fetch()
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        tmp = CACHE + '.part'
        with open(tmp, 'wb') as f:
            f.write(raw)
        os.replace(tmp, CACHE)
        return json.loads(raw.decode('utf-8')), None
    except Exception as e:
        if age is None:
            sys.exit('cannot download %s (%s) and there is no cached copy at %s' % (URL, e, CACHE))
        return json.load(open(CACHE, encoding='utf-8')), \
            'offline (%s): using the cached map from %s' % (type(e).__name__, time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(CACHE))))


def index(data):
    '''competitors: {guid: {maker, name, lenovo: [(lenovo product, class label, type)]}}, lenovo: [entries]'''
    comp = {}
    for x in data:
        for c in x.get('competitors') or []:
            for p in c.get('competing_products') or []:
                e = comp.setdefault(p['guid'], dict(maker=cl(p['manufacturer']), name=cl(p['product_name']), lenovo=[]))
                item = (cl(x['product_name']), cl(c.get('class_label')), cl(x.get('product_type')))
                if item not in e['lenovo']:
                    e['lenovo'].append(item)
    return comp


# ---------------------------------------------------------------- matching
def toks(s):
    return re.findall(r'[a-z0-9]+', cl(s).lower())


def split_query(q, makers):
    '''(vendor filters, model tokens). A vendor word is any word of a maker name or a known alias.'''
    vwords = {t for m in makers for t in toks(m)} | set(ALIAS)
    ven, mod = [], []
    for t in toks(q):
        (ven if t in vwords else mod).append(ALIAS.get(t, t))
    return ven, mod


def score(mod, name):
    '''0 = no match. exact token 3, prefix 2, squashed substring 1 (summed); None-safe.'''
    ct = toks(name)
    sq, tot = ''.join(ct), 0
    for t in mod:
        if t in ct:
            tot += 3
        elif any(c.startswith(t) for c in ct):
            tot += 2
        elif len(t) >= 3 and t in sq:
            tot += 1
        else:
            return 0
    if len(mod) > 1 and ''.join(mod) in sq:
        tot += 2  # 'dl 380' vs 'DL380'
    return tot


def near(mod, name):
    '''fallback: the query is a variant of a shorter model in the map (R760xs asked, R760 exists)'''
    ct = toks(name)
    return bool(mod) and all(any(len(c) >= 3 and re.search(r'\d', c) and t.startswith(c) and t != c for c in ct)
                             or t in ct for t in mod) and any(t not in ct for t in mod)


def search_comp(comp, q):
    makers = sorted({e['maker'] for e in comp.values()})
    ven, mod = split_query(q, makers)
    if not ven and not mod:
        return [], False
    def maker_ok(e):
        return all(v in e['maker'].lower() or v in ''.join(toks(e['maker'])) for v in ven)
    hits = []
    for e in comp.values():
        if not maker_ok(e):
            continue
        s = score(mod, e['name']) if mod else 1
        if s:
            hits.append((s, e))
    if hits:
        hits.sort(key=lambda h: (-h[0], len(toks(h[1]['name'])), h[1]['maker'], h[1]['name']))
        return [e for _, e in hits], False
    nh = [e for e in comp.values() if maker_ok(e) and near(mod, e['name'])]
    nh.sort(key=lambda e: (e['maker'], e['name']))
    return nh, True


def search_lenovo(data, q):
    toks_q = [t for t in toks(q) if t != 'lenovo']
    hits = []
    for x in data:
        s = score(toks_q, x['product_name'])
        if s:
            hits.append((s, x))
    hits.sort(key=lambda h: (-h[0], len(toks(h[1]['product_name'])), h[1]['product_name']))
    return [x for _, x in hits]


# ---------------------------------------------------------------- commands
def fmt_lenovo(items):
    out = []
    for name, cls, typ in items:
        extra = [x for x in (('class ' + cls) if cls and cls != name else '', typ) if x]
        out.append(name + (' (' + '; '.join(extra) + ')' if extra else ''))
    return out


def cmd_comp(comp, q, limit=30):
    hits, is_near = search_comp(comp, q)
    if not hits:
        print('no competitor product matches "%s". Try fewer words (e.g. the model number), or --list <maker>.' % q)
        return
    if is_near:
        print('no exact match for "%s"; closest shorter models in the map (check the suffix):\n' % q)
    else:
        print('%d competitor product%s match "%s"\n' % (len(hits), '' if len(hits) == 1 else 's', q))
    for e in hits[:limit]:
        print('%s %s' % (e['maker'], e['name']))
        for l in fmt_lenovo(e['lenovo']):
            print('    -> Lenovo %s' % l)
    if len(hits) > limit:
        print('... %d more, add words to narrow' % (len(hits) - limit))


def cmd_lenovo(data, q, vs=None, limit=12):
    hits = search_lenovo(data, q)
    if not hits:
        print('no Lenovo product matches "%s" in the map (--list lenovo shows them all)' % q)
        return
    vk = toks(vs)[0] if vs and toks(vs) else None
    vk = ALIAS.get(vk, vk)
    for x in hits[:limit]:
        by = {}
        for c in x.get('competitors') or []:
            for p in c.get('competing_products') or []:
                m = cl(p['manufacturer'])
                if vk and vk not in m.lower():
                    continue
                by.setdefault(m, [])
                if cl(p['product_name']) not in by[m]:
                    by[m].append(cl(p['product_name']))
        head = cl(x['product_name']) + ('  (%s)' % cl(x.get('product_type')) if x.get('product_type') else '')
        print(head)
        if not by:
            print('    (no %scompetitors listed)' % (vs + ' ' if vs else ''))
        for m in sorted(by):
            print('    %s: %s' % (m, ', '.join(by[m])))
        print()
    if len(hits) > limit:
        print('... %d more Lenovo products match, add words to narrow' % (len(hits) - limit))


def cmd_list(data, comp, q):
    if not q:
        n = {}
        for e in comp.values():
            n[e['maker']] = n.get(e['maker'], 0) + 1
        print('%d Lenovo products, %d competitor products from %d makers\n' % (len(data), len(comp), len(n)))
        for m, c in sorted(n.items(), key=lambda kv: (-kv[1], kv[0])):
            print('%-36s%4d' % (m, c))
        return
    if toks(q) and toks(q)[0] == 'lenovo':
        by = {}
        for x in data:
            by.setdefault(cl(x.get('product_type')) or '-', []).append(cl(x['product_name']))
        for t in sorted(by):
            print('%s (%d): %s\n' % (t, len(by[t]), ', '.join(sorted(by[t]))))
        return
    k = ALIAS.get(toks(q)[0], toks(q)[0]) if toks(q) else ''
    rows = sorted((e for e in comp.values() if k in e['maker'].lower() or k in ''.join(toks(e['maker']))),
                  key=lambda e: e['name'])
    if not rows:
        print('no maker matches "%s" (run --list for the makers)' % q)
        return
    print('%d %s products\n' % (len(rows), rows[0]['maker']))
    for e in rows:
        print('%-46s-> %s' % (e['name'][:45], '; '.join(l[0] for l in e['lenovo'])))


def suggest(q, limit=5):
    '''Lines like "Dell R760 -> Lenovo ThinkSystem SR650 V4" for other modules; [] if the map is unavailable.'''
    try:
        data, _ = load()
    except (SystemExit, Exception):
        return []
    hits, is_near = search_comp(index(data), q)
    return ['%s %s -> Lenovo %s%s' % (e['maker'], e['name'], ', '.join(fmt_lenovo(e['lenovo'])),
                                     ' (closest shorter model in the map)' if is_near else '') for e in hits[:limit]]


def main(argv):
    argv = list(argv)
    if argv and argv[0] == 'compete':  # called through kb.py
        argv = argv[1:]
    ap = argparse.ArgumentParser(prog='compete', add_help=False)
    ap.add_argument('text', nargs='*')
    ap.add_argument('--lenovo', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--vs', default=None)
    ap.add_argument('--refresh', action='store_true')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args(list(argv))
    q = ' '.join(a.text).strip()
    if a.help or (not q and not a.list):
        print(__doc__)
        return
    data, note = load(a.refresh)
    if note:
        print('(' + note + ')', file=sys.stderr)
    comp = index(data)
    if a.list:
        cmd_list(data, comp, q)
    elif a.lenovo:
        cmd_lenovo(data, q, a.vs)
    else:
        cmd_comp(comp, q)


if __name__ == '__main__':
    main(sys.argv[1:])
