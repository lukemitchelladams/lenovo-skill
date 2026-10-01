# Lenovo Presales Skill

An evidence-first Lenovo data center assistant for **Claude**, **ChatGPT**, **OpenAI Codex** and **any other LLM**. It answers ThinkSystem, ThinkAgile and ThinkEdge questions (Top Choice Express, feature codes, build validation, DCSC exports) and **converts competitor BOMs** from verified sources instead of model memory.

Models are confidently wrong about Lenovo feature codes, and the catalogue rotates every few weeks. This skill gives the model real evidence:

- **The DCSC configurator rules for 225 live MTMs** (crawled 2026-09-30), plus the 43 CTOs DCSC has retired:
  - every option per section, with its Top Choice Express (TCE) flag, min/max and legal quantities
  - required sections
  - 13,000+ withdraw dates
  - 111 of DCSC's own gating messages

  Prices are stripped and customer data is excluded.
- **165 verified facts:**
  - TCE floors and ceilings
  - NIC media traps
  - M.2 RAID behaviour
  - GPU forced companions
  - RAID limits
  - Dell/HPE/Cisco/Supermicro/Nutanix crosswalks
  - licensing and support rules
- **40 deterministic validators:** `check` runs them against any Lenovo BOM or DCSC export. Examples: a 230V-only PSU paired with a 120V cord, the HX single-NIC-vendor rule, an 8i controller behind 12 bays, a single M.2 boot drive, TCE all-or-nothing.
- **A competitor BOM matcher** (`match`). Give it a Dell, HPE, Cisco or Supermicro quote (txt, csv or xlsx) and it:
  - picks the Lenovo platform
  - proposes up to 3 real feature codes per line, TCE first
  - handles order-total quantities
  - lists forced companions
  - validates the result
- **Lenovo's official competitor map**, fetched live from Lenovo Press.
- **Platform specs for 16 platforms** (sockets, DIMM channels, bays, slots), plus a crawler for all ~2,200 Lenovo Press articles and a parts-table extractor for the product guides.

> **Not affiliated with or endorsed by Lenovo.** Lenovo, ThinkSystem, ThinkAgile, ThinkEdge and XClarity are trademarks of Lenovo. The DCSC rules snapshot and the facts are dated, and TCE membership and pricing change constantly. Always confirm a build in the live DCSC configurator; only an export carrying BU1E proves Top Choice Express.

## Pick your platform

| Platform | Get it | What you get |
|---|---|---|
| Claude Code / claude.ai | `lenovo-claude-skill.zip` from [Releases](https://github.com/lukemitchelladams/lenovo-skill/releases/latest) | A self-contained Agent Skill: SKILL.md, references and the bundled tools plus DCSC data |
| ChatGPT (custom GPT) | [`gpt/custom-gpt/`](gpt/custom-gpt/) plus `lenovo-kb-tools.zip` | Instructions (under 8,000 characters), 6 knowledge files, and tools that Code Interpreter runs |
| OpenAI Codex CLI | `lenovo-codex-skill.zip` from Releases | A self-contained Agent Skill tuned for Codex |
| Anything else | [`generic/`](generic/) | A compact system prompt / `AGENTS.md` plus knowledge files to attach or index |

## Install

### Claude Code

```bash
unzip lenovo-claude-skill.zip -d ~/.claude/skills/
```

On Windows, extract into `%USERPROFILE%\.claude\skills\` so you get `...\skills\lenovo\SKILL.md`.

It triggers on its own when you mention Lenovo, DCSC, TCE, a feature code, an MTM or a competitor BOM, or you can run `/lenovo`. The tools need Python 3.9+ and nothing else; `pip install openpyxl` is only required to read `.xlsx` files.

### claude.ai (web and desktop)

Upload `lenovo-claude-skill.zip` in the Skills section of claude.ai's settings.

### ChatGPT

Follow [`gpt/custom-gpt/README.md`](gpt/custom-gpt/README.md): paste the instructions, upload the 6 knowledge files, and turn on Web Search and Code Interpreter.

### OpenAI Codex CLI

```bash
unzip lenovo-codex-skill.zip -d ~/.codex/skills/
```

### Any other LLM

Use [`generic/LENOVO_PROMPT.md`](generic/LENOVO_PROMPT.md) as the system prompt or `AGENTS.md`, and attach or index the files in [`generic/knowledge/`](generic/knowledge/). If your agent can run a shell, point it at `kb/kb.py`.

### From source

```bash
git clone https://github.com/lukemitchelladams/lenovo-skill.git && cd lenovo-skill
python tools/build_references.py     # regenerates references and builds the three zips in dist/
```

## Try it

```bash
python kb/kb.py match my-dell-quote.csv            # competitor BOM -> Lenovo worksheet
python kb/kb.py check my-lenovo-bom.txt --tce       # validate a Lenovo BOM or DCSC export
python kb/kb.py rules --fc B8P0                     # where a feature code lives, TCE flag per MTM/section
python kb/kb.py dfind "SR630 V4" "Xeon" --tce       # TCE CPUs on the SR630 V4
python kb/kb.py gates "Tri-Mode"                    # DCSC's own gating messages
python kb/kb.py compete "HPE DL380 Gen12"           # Lenovo's official competitor map
python kb/kb.py fact "M.2 RAID"                     # curated verified facts
```

Every command is listed in [`shared/kb-usage.md`](shared/kb-usage.md).

## Optional: your own knowledge base

The snapshot and facts cover what one engineer proved. A local KB adds **your** quote history: every part you have configured, on which MTM, whether it carried BU1E, and every DCSC message. It also adds a full-text index of the Lenovo Press guides.

```bash
pip install -r requirements.txt
python kb/refresh.py ~/Downloads ~/Desktop/Configs   # folders holding your DCSC exports (.xlsx or .zip)
python docs/get_lenovo_docs.py                       # the 44 key product guides (~230 MB)
python docs/crawl_lenovo_press.py                    # optional: all ~2,200 Lenovo Press articles as text
python kb/build_kb_index.py                          # facts, doc index and guide part tables
```

Point the skill at it with `LENOVO_KB_DB=/path/to/kb/dcsc_kb.sqlite`.

**Your KB contains your customers' configurations and pricing.** It is `.gitignore`d. Never commit it, and never attach it to a shared GPT. The Lenovo Press documents are Lenovo's copyright: they are fetched for personal reference and not redistributed.

## Where the data comes from

| Data | Source | Notes |
|---|---|---|
| `kb/data/dcsc-rules.json.gz` | DCSC configurator rules, crawled 2026-09-30 (previous: 2026-07-28) | Sections, options, TCE flags, min/max, legal quantities and withdraw dates, plus gating messages. Prices were removed. Gating messages had configuration names stripped, and any message that could still identify a customer was dropped. It is a default-state snapshot. |
| `kb/data/platform-specs.json` | Lenovo Press product guides | Paraphrased hardware limits, with the guide id and as-of month per platform |
| `kb/kb_facts*.py` | Hand-verified against DCSC exports and Lenovo Press | Each fact is dated and marked proven, flagged or unknown. No customer names or prices. |
| Competitor map | `lenovopress.lenovo.com/compare_competitor_map.json` | Fetched live, not redistributed |

## Adding a fact

Each fact is a tuple, `(topic, scope, status, title, body, source, verified)`, in [`kb/kb_facts.py`](kb/kb_facts.py) or its sibling modules. After adding one:

```bash
python tools/build_references.py
python -m unittest discover -s kb/tests
```

PRs are welcome. Each fact needs a source (a Lenovo Press page or DCSC evidence), a verified date, and **no customer names, deal details or prices**.

## Layout

```
kb/                   the tools: kb.py (entry point), match, rules, dcsc_rules, specs, compete, press_parts
kb/data/              DCSC rules snapshot + platform specs
kb/kb_facts*.py       the fact library (single source)
kb/tests/             98 tests (python -m unittest discover -s kb/tests)
claude/lenovo/        Claude skill (SKILL.md; references/ and scripts/ are generated)
gpt/custom-gpt/       ChatGPT GPT: instructions, starters, generated knowledge/
gpt/codex/lenovo/     Codex CLI skill
generic/              prompt + knowledge files for any LLM (generated)
shared/               hand-written sources: hard rules, tool usage, generic header
docs/                 Lenovo Press downloader and full-site crawler
tools/                build_references.py
```

## License

[MIT](LICENSE).
