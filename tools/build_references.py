#!/usr/bin/env python3
'''Regenerate every platform's reference files from the single sources.

Sources:  kb/kb_facts.py, shared/*.md, docs/get_lenovo_docs.py (DOCS)
Targets:  claude/lenovo/references/, gpt/codex/lenovo/references/,
          gpt/custom-gpt/knowledge/, generic/LENOVO_PROMPT.md,
          dist/lenovo-claude-skill.zip, dist/lenovo-codex-skill.zip

Usage: python tools/build_references.py
'''
import datetime, importlib.util, os, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(ROOT, 'shared')
GPT_LIMIT = 8000


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
           f'Generated {today} from `kb/kb_facts.py`.', '',
           '- **proven**: verified against DCSC exports and/or Lenovo Press on the date shown.',
           '- **flagged**: sources conflict or the evidence is thin; say so when you use it.',
           '- TCE membership **rotates** per MTM and per date. Treat any TCE claim older than a few weeks as a lead to re-check in the live DCSC panel.',
           '- "The source corpus" means the author\'s own DCSC exports, which are not published. Prices are omitted on purpose.', '']
    for topic, scope, status, title, body, source, verified in facts:
        out += [f'## {title}', '',
                f'`{topic}` | **{status}** | scope: {scope} | verified: {verified}', '',
                body, '', f'*Source: {source}*', '']
    return '\n'.join(out)


def docs_md(docs):
    out = ['# Lenovo Press document index', '',
           'Product guides live at `https://lenovopress.lenovo.com/<id>` (web page) and `https://lenovopress.lenovo.com/<id>.pdf` (full PDF). '
           'A few ids (RAID/HBA reference, SSD portfolio, rail kits, DM Series) are live-database web pages with no PDF.', '',
           '| id | category | title |', '|---|---|---|']
    out += [f'| {i} | {c} | {t} |' for i, c, t in docs]
    out += ['', 'Also useful, not in the download list: `lp2279` Scale Computing on Lenovo, `lp1907` ST50 V3, `lp1994` ST45 V3, '
            '`lp1667` HX630 V3 ROBO, `lp1992` XClarity One, `lp2376` OpenShift Virtualization DRS. Thermal tables live at `pubs.lenovo.com`.', '']
    return '\n'.join(out)


def zip_dir(src, dest, arc_root):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, _, files in os.walk(src):
            for fn in sorted(files):
                p = os.path.join(dp, fn)
                z.write(p, os.path.join(arc_root, os.path.relpath(p, src)))


def main():
    facts = load(os.path.join(ROOT, 'kb', 'kb_facts.py'), 'kb_facts').FACTS
    docs = load(os.path.join(ROOT, 'docs', 'get_lenovo_docs.py'), 'get_lenovo_docs').DOCS
    bad = [f[0] for f in facts if len(f) != 7 or f[2] not in ('proven', 'flagged', 'unknown')]
    if bad:
        sys.exit('malformed facts: ' + ', '.join(bad))

    ref = {
        'facts.md': facts_md(facts),
        'lenovo-press-docs.md': docs_md(docs),
        'hard-rules.md': read(os.path.join(SHARED, 'hard-rules.md')),
        'kb-usage.md': read(os.path.join(SHARED, 'kb-usage.md')),
    }
    for skill in ('claude/lenovo', 'gpt/codex/lenovo'):
        d = os.path.join(ROOT, skill, 'references')
        shutil.rmtree(d, ignore_errors=True)
        for name, text in ref.items():
            write(os.path.join(d, name), text)

    kn = os.path.join(ROOT, 'gpt', 'custom-gpt', 'knowledge')
    shutil.rmtree(kn, ignore_errors=True)
    for name in ('facts.md', 'hard-rules.md', 'lenovo-press-docs.md'):
        write(os.path.join(kn, name), ref[name])

    prompt = '\n\n---\n\n'.join([read(os.path.join(SHARED, 'generic-header.md')).rstrip(),
                                   ref['hard-rules.md'].rstrip(), ref['lenovo-press-docs.md'].rstrip(),
                                   ref['facts.md'].rstrip()]) + '\n'
    write(os.path.join(ROOT, 'generic', 'LENOVO_PROMPT.md'), prompt)

    zip_dir(os.path.join(ROOT, 'claude', 'lenovo'), os.path.join(ROOT, 'dist', 'lenovo-claude-skill.zip'), 'lenovo')
    zip_dir(os.path.join(ROOT, 'gpt', 'codex', 'lenovo'), os.path.join(ROOT, 'dist', 'lenovo-codex-skill.zip'), 'lenovo')

    n_instr = len(read(os.path.join(ROOT, 'gpt', 'custom-gpt', 'instructions.md')))
    print(f'facts: {len(facts)}   docs: {len(docs)}')
    print(f'generic/LENOVO_PROMPT.md: {len(prompt):,} chars (~{len(prompt) // 4:,} tokens)')
    print(f'gpt/custom-gpt/instructions.md: {n_instr:,} / {GPT_LIMIT:,} chars')
    print('dist/: lenovo-claude-skill.zip, lenovo-codex-skill.zip')
    if n_instr > GPT_LIMIT:
        sys.exit('instructions.md is over the custom GPT limit')


if __name__ == '__main__':
    main()
