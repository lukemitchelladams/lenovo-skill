#!/usr/bin/env python3
'''Regenerate every platform's reference files and packages from the single sources.

Sources:  kb/kb_facts*.py, kb/data/, kb/*.py, shared/*.md, docs/get_lenovo_docs.py (DOCS)
Targets:  claude/lenovo/{references,scripts}/   gpt/codex/lenovo/{references,scripts}/
          gpt/custom-gpt/knowledge/              generic/LENOVO_PROMPT.md + generic/knowledge/
          dist/lenovo-claude-skill.zip, dist/lenovo-codex-skill.zip, dist/lenovo-kb-tools.zip

Usage: python tools/build_references.py
'''
import datetime, glob, gzip, html, importlib.util, json, os, re, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.join(ROOT, 'kb')
SHARED = os.path.join(ROOT, 'shared')
GPT_LIMIT = 8000
sys.path.insert(0, KB)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def facts_md(facts):
    today = datetime.date.today().isoformat()
    n = {s: sum(1 for f in facts if f[2] == s) for s in ('proven', 'flagged', 'unknown')}
    out = ['# Lenovo verified facts', '',
           f'{len(facts)} facts ({n["proven"]} proven, {n["flagged"]} flagged, {n["unknown"]} unknown). '
           f'Generated {today} from `kb/kb_facts*.py`.', '',
           '- **proven**: verified against DCSC exports and/or Lenovo Press on the date shown.',
           '- **flagged**: sources conflict or the evidence is thin; say so when you use it.',
           '- TCE membership **rotates** per MTM and per date. Treat any TCE claim older than a few weeks as a lead to re-check in the live DCSC panel.',
           '- "The source corpus" means the author\'s own DCSC exports, which are not published. Prices are omitted on purpose.', '']
    for topic, scope, status, title, body, source, verified in facts:
        out += [f'## {title}', '', f'`{topic}` | **{status}** | scope: {scope} | verified: {verified}', '',
                body, '', f'*Source: {source}*', '']
    return '\n'.join(out)


def docs_md(docs):
    out = ['# Lenovo Press document index', '',
           'Product guides live at `https://lenovopress.lenovo.com/<id>` (web page) and `https://lenovopress.lenovo.com/<id>.pdf` (full PDF). '
           'A few ids (RAID/HBA reference, SSD portfolio, rail kits, DM Series) are live-database web pages with no PDF. '
           '`docs/crawl_lenovo_press.py` fetches all ~2,200 Lenovo Press articles for a local index.', '',
           '| id | category | title |', '|---|---|---|']
    out += [f'| {i} | {c} | {t} |' for i, c, t in docs]
    out += ['', 'Also useful, not in the download list: `lp2279` Scale Computing on Lenovo, `lp1907` ST50 V3, `lp1994` ST45 V3, '
            '`lp1667` HX630 V3 ROBO, `lp1992` XClarity One, `lp2376` OpenShift Virtualization DRS. Thermal tables live at `pubs.lenovo.com`.', '']
    return '\n'.join(out)


def specs_md(specs):
    ps = specs.platforms()
    out = ['# Platform specs', '', f'{len(ps)} platforms, paraphrased from their Lenovo Press product guides (the `source` id). '
           'Hardware limits only: sockets, DIMM slots and channels, drive bays, PCIe/OCP slots, PSU and GPU notes. '
           'Always confirm against the named guide.', '']
    for p in ps:
        out += ['```', specs.render(p), '```', '']
    return '\n'.join(out)


def strip_html(s):
    s = re.sub(r'<br\s*/?>|<LF>', ' ', s, flags=re.I)
    s = re.sub(r'<a [^>]*href="?([^" >]+)"?[^>]*>(.*?)</a>', r'\2 (\1)', s, flags=re.I | re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def gates_md(db):
    gs = db['gates']
    out = ['# DCSC gating messages', '', f'{len(gs)} distinct messages DCSC emitted in real configurations (configuration names stripped; '
           f'DCSC rules snapshot {db["meta"]["crawled"]}). Critical blocks a build; Warning and Normal do not. They are the '
           'configurator\'s own rules, verbatim.', '']
    for sev in ('Critical', 'Error', 'Warning', 'Normal', 'Info'):
        sub = [g for g in gs if g['sev'] == sev]
        if not sub:
            continue
        out += [f'## {sev} ({len(sub)})', '']
        for g in sub:
            m = ', '.join(g['mtms'][:8]) + (' ...' if len(g['mtms']) > 8 else '')
            out.append(f'- {strip_html(g["text"])}  _(seen {g["n"]}x; {m or "MTM not recorded"})_')
        out.append('')
    return '\n'.join(out)


TOOL_FILES = ['paths.py', 'kb.py', 'kb_facts.py', 'kb_facts_rules.py', 'kb_facts_field.py', 'dcsc_rules.py', 'rules.py',
              'specs.py', 'match.py', 'compete.py', 'press_parts.py', 'build_kb_index.py']


def copy_tools(dest):
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(os.path.join(dest, 'data'))
    for f in TOOL_FILES:
        shutil.copy2(os.path.join(KB, f), os.path.join(dest, f))
    for f in glob.glob(os.path.join(KB, 'data', '*')):
        shutil.copy2(f, os.path.join(dest, 'data', os.path.basename(f)))


def zip_dir(src, dest, arc_root):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for fn in sorted(files):
                p = os.path.join(dp, fn)
                z.write(p, os.path.join(arc_root, os.path.relpath(p, src)))


def main():
    facts = load(os.path.join(KB, 'kb_facts.py'), 'kb_facts').FACTS
    docs = load(os.path.join(ROOT, 'docs', 'get_lenovo_docs.py'), 'get_lenovo_docs').DOCS
    specs = load(os.path.join(KB, 'specs.py'), 'specs')
    db = json.load(gzip.open(os.path.join(KB, 'data', 'dcsc-rules.json.gz'), 'rt', encoding='utf-8'))
    bad = [f[0] for f in facts if len(f) != 7 or f[2] not in ('proven', 'flagged', 'unknown')]
    dup = sorted({f[0] for f in facts if [g[0] for g in facts].count(f[0]) > 1})
    if bad or dup:
        sys.exit('malformed facts: ' + ', '.join(bad) + ' duplicate topics: ' + ', '.join(dup))

    ref = {'facts.md': facts_md(facts), 'lenovo-press-docs.md': docs_md(docs), 'platform-specs.md': specs_md(specs),
           'dcsc-gates.md': gates_md(db), 'hard-rules.md': read(os.path.join(SHARED, 'hard-rules.md')),
           'kb-usage.md': read(os.path.join(SHARED, 'kb-usage.md'))}

    for skill in ('claude/lenovo', 'gpt/codex/lenovo'):
        d = os.path.join(ROOT, skill, 'references')
        shutil.rmtree(d, ignore_errors=True)
        for name, text in ref.items():
            write(os.path.join(d, name), text)
        copy_tools(os.path.join(ROOT, skill, 'scripts', 'kb'))

    tools = os.path.join(ROOT, 'dist', '_tools', 'kb')
    copy_tools(tools)
    zip_dir(tools, os.path.join(ROOT, 'dist', 'lenovo-kb-tools.zip'), 'kb')
    shutil.rmtree(os.path.join(ROOT, 'dist', '_tools'), ignore_errors=True)

    kn = os.path.join(ROOT, 'gpt', 'custom-gpt', 'knowledge')
    shutil.rmtree(kn, ignore_errors=True)
    for name in ('facts.md', 'hard-rules.md', 'lenovo-press-docs.md', 'platform-specs.md', 'dcsc-gates.md'):
        write(os.path.join(kn, name), ref[name])
    shutil.copy2(os.path.join(ROOT, 'dist', 'lenovo-kb-tools.zip'), os.path.join(kn, 'lenovo-kb-tools.zip'))

    gk = os.path.join(ROOT, 'generic', 'knowledge')
    shutil.rmtree(gk, ignore_errors=True)
    for name in ('facts.md', 'platform-specs.md', 'dcsc-gates.md'):
        write(os.path.join(gk, name), ref[name])
    prompt = '\n\n---\n\n'.join([read(os.path.join(SHARED, 'generic-header.md')).rstrip(), ref['hard-rules.md'].rstrip(),
                                   ref['lenovo-press-docs.md'].rstrip()]) + '\n'
    write(os.path.join(ROOT, 'generic', 'LENOVO_PROMPT.md'), prompt)

    zip_dir(os.path.join(ROOT, 'claude', 'lenovo'), os.path.join(ROOT, 'dist', 'lenovo-claude-skill.zip'), 'lenovo')
    zip_dir(os.path.join(ROOT, 'gpt', 'codex', 'lenovo'), os.path.join(ROOT, 'dist', 'lenovo-codex-skill.zip'), 'lenovo')

    n_instr = len(read(os.path.join(ROOT, 'gpt', 'custom-gpt', 'instructions.md')))
    sz = lambda p: os.path.getsize(os.path.join(ROOT, 'dist', p)) / 1e6
    print(f'facts: {len(facts)}   docs: {len(docs)}   platforms: {len(specs.platforms())}   gates: {len(db["gates"])}   '
          f'dcsc models: {len(db["models"])}')
    print(f'generic/LENOVO_PROMPT.md: {len(prompt):,} chars; generic/knowledge/facts.md: {len(ref["facts.md"]):,} chars')
    print(f'gpt/custom-gpt/instructions.md: {n_instr:,} / {GPT_LIMIT:,} chars')
    print(f'dist/: lenovo-claude-skill.zip {sz("lenovo-claude-skill.zip"):.1f} MB, lenovo-codex-skill.zip '
          f'{sz("lenovo-codex-skill.zip"):.1f} MB, lenovo-kb-tools.zip {sz("lenovo-kb-tools.zip"):.1f} MB')
    if n_instr > GPT_LIMIT:
        sys.exit('instructions.md is over the custom GPT limit')


if __name__ == '__main__':
    main()
