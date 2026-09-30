---
name: lenovo
description: Answer any Lenovo data center hardware question from verified evidence (DCSC configurator rules, 160+ curated facts, Lenovo Press, the official Lenovo competitor map) instead of model memory, and convert competitor BOMs. Use for ANY question about Lenovo ThinkSystem, ThinkAgile, ThinkEdge, DCSC, Top Choice Express or TCE, BU1E, feature codes, MTMs, drives, DIMMs, CPUs, GPUs, controllers, NICs, PSUs, storage arrays, HX/VX/MX/FX nodes, Nutanix or Azure Local on Lenovo, competitor-to-Lenovo BOM conversions, build validation, or reading a DCSC export.
---

# Lenovo question protocol

**Never answer a Lenovo feature-code, build or TCE question from model knowledge.** It is unreliable, and the catalogue rotates every few weeks.

## Tools bundled with this skill

`scripts/kb/` next to this file needs only Python 3.9+ and no install; `openpyxl` is required only for `.xlsx` files. With Codex the path is `~/.codex/skills/lenovo/scripts/kb/kb.py`:

```bash
KB=~/.codex/skills/lenovo/scripts/kb/kb.py
python $KB fact "<terms>"                          # curated verified facts: run first
python $KB rules --fc <FC>                          # MTMs/sections holding a feature code + TCE flag
python $KB rules "<model|MTM>" --required           # DCSC required sections
python $KB dfind "<model|MTM>" "<regex>" [--tce]    # complete DCSC option list of an MTM
python $KB gates "<regex>"                          # DCSC gating messages
python $KB spec "<model|MTM>"                       # platform limits
python $KB compete "<competitor model>"             # official Lenovo competitor map (needs network)
python $KB match <competitor-bom file>              # competitor BOM -> Lenovo worksheet
python $KB check <lenovo-bom|DCSC .xlsx> [--mtm X] [--nodes N] [--tce]   # rule validators
```

If `LENOVO_KB_DB` is set, it points at the user's personal KB of their own DCSC exports, and `part`, `tce`, `find`, `errors`, `docs` and `sql` then work too. If a command fails, say so and use `references/`.

## Source hierarchy

1. A live DCSC export the user provides.
2. `kb.py fact` / `references/facts.md`.
3. The DCSC rules snapshot (`rules`, `dfind`, `gates`). It is a dated default-state snapshot: `q=[0]` means "not selectable by default", not illegal.
4. Lenovo Press guides (`references/lenovo-press-docs.md`).
5. Model knowledge, for concepts only.

## Workflow

- **"Is X TCE?"** Run `fact` + `rules --fc` + the guide's TCE column. Date every source. Only BU1E in a live export proves it.
- **"Will this build?"** Run `check` on the BOM file, then `gates` for related DCSC messages.
- **Competitor BOM:** run `match`, then refine: pick one code per line with `fact`, `dfind` and `spec`, and list what remains to confirm. Never invent a feature code the tools did not return.
- **DCSC export:**
  - BU1E means TCE.
  - Unit price is per unit.
  - The group quantity is only in the zip's `.xml`.
  - In Message History, Critical blocks the build and Warning does not.

## Hard rules (full list in references/hard-rules.md)

- TCE is proven only by BU1E, and it is all-or-nothing. It rotates per MTM per date, and its lists have floors and ceilings.
- A rack or a tied non-TCE order voids TCE.
- U.3 blocks TCE. Tri-mode is 940-series only.
- Software-defined storage needs raw drives.
- Write TB, never TiB.
- Separate absence of evidence from proof of prohibition, and what DCSC built from what Lenovo supports.

## Output

Lead with the answer. Put the evidence in a table with sources and dates. Mark every claim proven, flagged or unknown. End with the exact question to put to Lenovo if anything is unresolved. Say "Top Choice Express (TCE)", never "quick-ship". Never give prices from memory.
