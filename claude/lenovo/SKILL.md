---
name: lenovo
description: Answer any Lenovo data center hardware question from verified evidence (DCSC configurator rules, 160+ curated facts, Lenovo Press, the official Lenovo competitor map) instead of model memory, and convert competitor BOMs. Use for ANY question about Lenovo ThinkSystem, ThinkAgile, ThinkEdge, DCSC, Top Choice Express or TCE, BU1E, feature codes, MTMs, drives, DIMMs, CPUs, GPUs, backplanes, RAID controllers, rail kits, PSUs, NICs, transceivers, racks, JBODs, storage arrays (DM/DG/DE/DS), HX/VX/MX/FX nodes, Nutanix or Azure Local on Lenovo, competitor-to-Lenovo BOM conversions (Dell, HPE, Cisco, Supermicro, Nutanix NX), build validation, field upgrades, thermal rules, or reading a DCSC export. Triggers on "lenovo", "DCSC", "TCE", "thinksystem", "thinkagile", "feature code", "is this TCE", "will this build", "convert this BOM", or a pasted MTM/feature code.
---

# Lenovo question protocol

Run every Lenovo hardware question through this. **Never answer a Lenovo feature-code, build or TCE question from model knowledge.** It is unreliable, and the catalogue rotates every few weeks.

## Tools bundled with this skill

The folder next to this file, `scripts/kb/`, holds Python tools plus data: the DCSC rules snapshot and the platform specs. They need only Python 3.9+ and no install; `openpyxl` is required only for `.xlsx` files. In Claude Code the path is `~/.claude/skills/lenovo/scripts/kb/kb.py`. Run them with the Bash tool:

```bash
KB=~/.claude/skills/lenovo/scripts/kb/kb.py
python $KB fact "<terms>"                     # 160+ curated verified facts (run this FIRST)
python $KB rules --fc <FC>                     # every MTM/section holding a feature code, TCE flag, min/max
python $KB rules "<model|MTM>" --required      # DCSC required sections for a platform
python $KB dfind "<model|MTM>" "<regex>" [--tce]   # search the COMPLETE DCSC option list of an MTM
python $KB gates "<regex>"                     # DCSC gating messages (the configurator's own rules)
python $KB spec "<model|MTM>"                  # platform limits: sockets, DIMM slots, bays, slots, PSU
python $KB compete "<competitor model>"        # official Lenovo competitor map (live; needs internet)
python $KB match <competitor-bom file>         # competitor BOM -> Lenovo worksheet with TCE flags
python $KB check <lenovo-bom file|DCSC .xlsx> [--mtm X] [--nodes N] [--tce]   # 40 rule validators
```

On Windows PowerShell, use `$env:USERPROFILE\.claude\skills\lenovo\scripts\kb\kb.py`. If the user has built a personal KB from their own DCSC exports, the environment variable `LENOVO_KB_DB` points at it, and `part`, `tce`, `find`, `errors`, `configs`, `docs` and `sql` then answer from their quote history. If a command fails, say so and fall back to `references/`. Do not pretend it was checked.

## Source hierarchy, highest authority first

1. **A live DCSC export the user just gave you.** It is ground truth for that config on that date. If they have one, ask for it.
2. **Curated facts:** `kb.py fact`, or grep `references/facts.md`. Each fact is marked proven, flagged or unknown, and dated.
3. **The DCSC rules snapshot:** `kb.py rules`, `dfind` and `gates`. It shows what the configurator offers per MTM and section, with the TCE flag, as of the snapshot date. It is a default-state snapshot: `q=[0]` means "not selectable in the default state", not illegal.
4. **Lenovo Press:** the product guides (`references/lenovo-press-docs.md` maps platform to guide id). Fetch `https://lenovopress.lenovo.com/lpNNNN` with WebFetch, or use `kb.py docs` if the user built the local index.
5. **Model knowledge**, for general concepts only.

## Workflow

- **"Is X TCE?" / "Does X fit Y?"**
  1. Run `fact X`.
  2. Run `rules --fc X`. It shows the TCE flag per MTM and section.
  3. Check the product guide's TCE column.
  4. Answer with the date of each source and say that only BU1E in a live export proves it.
- **"Will this build?"** Save the BOM to a file and run `check`. Then explain each block and warning, and run `gates` for any related DCSC message.
- **Competitor BOM:**
  1. Save it to a file and run `match`. It picks the platform, proposes up to 3 real feature codes per line (TCE first), lists forced companions and runs the validators.
  2. Refine the worksheet: pick one code per line and justify it, using `fact`, `dfind` and `spec`.
  3. List what could not be mapped and what must be confirmed in DCSC.
  4. Never invent a feature code the tools did not return.
- **Reading a DCSC export:**
  - BU1E means TCE.
  - Price is per unit; compute qty x unit.
  - The xlsx hides the config-group quantity, which only the `.xml` in the zip carries.
  - Read Message History: Critical blocks the build, Warning does not.

Full references are in `references/`: `hard-rules.md`, `facts.md`, `platform-specs.md`, `dcsc-gates.md`, `kb-usage.md` and `lenovo-press-docs.md`.

## Hard rules

- TCE is proven only by BU1E in a DCSC export, and it is all-or-nothing.
- TCE rotates per MTM per date, and its lists have floors as well as ceilings. Never extrapolate to a bigger or smaller part.
- A rack chassis, or a tied order holding non-TCE product, voids TCE. DCSC says 10 business days order to ship.
- U.3 NVMe blocks TCE. Tri-mode is 940-series only.
- Software-defined storage needs raw drives.
- Write TB, never TiB.
- Separate absence of evidence from proof of prohibition, and what DCSC built from what Lenovo supports.

## Output

Lead with the answer. Put the evidence in a table with its sources and dates. Mark every claim **proven**, **flagged** or **unknown**. End with the exact question to put to Lenovo or the DCSC panel if anything is unresolved.

Say "Top Choice Express (TCE)", never "quick-ship". Give no prices from memory or from the snapshot, which has none; prices come only from a current export.
