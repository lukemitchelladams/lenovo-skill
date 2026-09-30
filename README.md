# Lenovo Presales Skill

An evidence-first Lenovo data center assistant for **Claude**, **ChatGPT**, **OpenAI Codex** and **any other LLM**. It answers ThinkSystem, ThinkAgile and ThinkEdge questions (Top Choice Express, feature codes, build validation, DCSC exports, competitor BOM conversions) from verified sources instead of model memory.

Models are confidently wrong about Lenovo feature codes, and the catalogue rotates every few weeks. This skill makes the model:

- **check a curated library of 48 verified facts first**: TCE floors and ceilings, NIC media traps, M.2 RAID behaviour, GPU forced companions, RAID controller limits, Dell/HPE crosswalks, and more
- **apply hard rules that override inference**, such as "only BU1E proves TCE" and "TCE is all-or-nothing"
- **read DCSC exports correctly**: per-unit prices, the hidden config-group quantity, and BU1E detection
- **separate proof from absence of evidence**, and what DCSC *built* from what Lenovo *supports*
- **optionally query your own local KB** built from your DCSC exports plus the public Lenovo Press guides

> **Not affiliated with or endorsed by Lenovo.** Lenovo, ThinkSystem, ThinkAgile, ThinkEdge and XClarity are trademarks of Lenovo. Facts were verified on the dates shown, but TCE membership and pricing change constantly. Always confirm in the live DCSC configurator before quoting.

## Pick your platform

| Platform | Folder | What you get |
|---|---|---|
| Claude Code / claude.ai | [`claude/lenovo/`](claude/lenovo/) | Agent Skill (`SKILL.md` + references), with optional KB queries via Bash |
| ChatGPT (custom GPT) | [`gpt/custom-gpt/`](gpt/custom-gpt/) | Instructions (under 8,000 characters) + 3 knowledge files + conversation starters |
| OpenAI Codex CLI | [`gpt/codex/lenovo/`](gpt/codex/lenovo/) | Agent Skill tuned for Codex |
| Anything else | [`generic/LENOVO_PROMPT.md`](generic/LENOVO_PROMPT.md) | One self-contained file (~16k tokens) to use as a system prompt, `AGENTS.md`, `GEMINI.md`, `.cursorrules` or Copilot instructions |

## Install

### Claude Code

```bash
git clone https://github.com/lukemitchelladams/lenovo-skill.git
cp -r lenovo-skill/claude/lenovo ~/.claude/skills/lenovo
```

On Windows PowerShell: `Copy-Item -Recurse lenovo-skill\claude\lenovo $HOME\.claude\skills\lenovo`.

The skill then triggers on its own when you mention Lenovo, DCSC, TCE, a feature code or an MTM, or you can run `/lenovo`.

### claude.ai (web and desktop)

1. Download `lenovo-claude-skill.zip` from the [latest release](https://github.com/lukemitchelladams/lenovo-skill/releases/latest), or run `python tools/build_references.py` to build it into `dist/`.
2. Upload it in the Skills section of claude.ai's settings.

The local-KB step is skipped there; everything else works.

### ChatGPT

Follow [`gpt/custom-gpt/README.md`](gpt/custom-gpt/README.md). It takes about 3 minutes: paste the instructions, upload 3 knowledge files, and turn on Web Search and Code Interpreter so the GPT can parse the DCSC `.xlsx` exports you upload.

### OpenAI Codex CLI

```bash
cp -r lenovo-skill/gpt/codex/lenovo ~/.codex/skills/lenovo
```

On Windows, the folder is `%USERPROFILE%\.codex\skills\lenovo`.

### Any other LLM

Use [`generic/LENOVO_PROMPT.md`](generic/LENOVO_PROMPT.md) as the system prompt, or drop it into your project as `AGENTS.md`. If your model's context is small, trim the facts section to the platforms you sell.

## Optional: build your own knowledge base

The facts cover what one engineer proved. A local KB lets the skill answer from **your** quote history as well: every part you have ever configured, on which MTM, whether it carried BU1E, and every DCSC gating message verbatim.

```bash
pip install -r requirements.txt
python kb/refresh.py ~/Downloads ~/Desktop/Configs   # folders holding your DCSC exports (.xlsx or .zip)
python docs/get_lenovo_docs.py                       # public Lenovo Press guides, ~230 MB
python kb/build_kb_index.py --docs-only              # page-level full-text index of the guides
```

Then point the skill at it by setting `LENOVO_KB_DIR` to the absolute path of this repo's `kb/` folder:

```bash
export LENOVO_KB_DIR="$HOME/lenovo-skill/kb"
```

On Windows: `setx LENOVO_KB_DIR "%USERPROFILE%\lenovo-skill\kb"`.

Try it:

```bash
python kb/kb.py fact "M.2 RAID"      # curated facts (works even without a database)
python kb/kb.py part BU1E            # which MTMs you have TCE-validated builds on
python kb/kb.py tce 7DG9CTO1WW       # every part proven TCE on an SR630 V4
python kb/kb.py docs '"10GBASE-T"' --lp lp1971
```

See [`shared/kb-usage.md`](shared/kb-usage.md) for every command, the schema and the SQL recipes.

**Your KB contains your customers' configurations and pricing.** It is `.gitignore`d. Never commit it, and never attach it to a shared GPT. The Lenovo Press PDFs are Lenovo's copyright and are downloaded for personal reference, not redistributed.

## Adding a fact

Each fact in [`kb/kb_facts.py`](kb/kb_facts.py) is a tuple: `(topic, scope, status, title, body, source, verified)`, where `status` is `proven`, `flagged` or `unknown`. After adding one:

```bash
python tools/build_references.py         # regenerates every platform's reference files
python kb/build_kb_index.py --facts-only # refreshes your local KB, if you have one
```

PRs with new facts are welcome. Each needs a source (a Lenovo Press page, or evidence from a DCSC export), a verified date, and **no customer names, deal details or prices**.

## Layout

```
claude/lenovo/        Claude skill (SKILL.md + generated references/)
gpt/custom-gpt/       ChatGPT GPT: instructions, starters, generated knowledge/
gpt/codex/lenovo/     Codex CLI skill
generic/              single-file prompt for any LLM (generated)
shared/               hand-written sources: hard rules, KB usage, generic header
kb/                   fact library + DCSC export KB tooling
docs/                 Lenovo Press downloader
tools/                build_references.py
```

Files under `references/`, `knowledge/`, `generic/` and `dist/` are generated, so edit `kb/kb_facts.py` or `shared/` instead.

## License

[MIT](LICENSE).
