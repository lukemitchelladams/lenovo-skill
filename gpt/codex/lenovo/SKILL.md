---
name: lenovo
description: Answer any Lenovo data center hardware question from verified evidence (DCSC exports, curated facts, Lenovo Press) instead of model memory. Use for ANY question about Lenovo ThinkSystem, ThinkAgile, ThinkEdge, DCSC, Top Choice Express or TCE, BU1E, feature codes, MTMs, drives, DIMMs, CPUs, GPUs, backplanes, RAID controllers, NICs, transceivers, PSUs, rail kits, storage arrays, HX/VX/MX/FX nodes, Nutanix or Azure Local on Lenovo, competitor-to-Lenovo BOM conversions, build validation, or reading a DCSC export.
---

# Lenovo question protocol

Run every Lenovo hardware question through this before answering. **Never answer a Lenovo feature-code, build or TCE question from model knowledge.** It is unreliable, and the catalogue rotates every few weeks.

## Source hierarchy, highest authority first

1. A live DCSC export the user provides. This is ground truth for that config on that date, so ask for it if they have one.
2. `references/facts.md` in this skill folder: curated, hand-verified facts, each marked proven, flagged or unknown, with a date.
3. The user's local KB of their own DCSC exports, if built (see below).
4. Lenovo Press product guides (`lenovopress.lenovo.com`).
5. Model knowledge, for general concepts only.

## Step 0: facts first

Search `references/facts.md` for the feature code, MTM or platform, for example with `rg -n "<term>" references/facts.md`. Read `references/hard-rules.md` before any TCE, storage or export-reading answer. If a fact answers the question, cite it and stop.

## Step 1: local KB (optional)

If the `LENOVO_KB_DIR` environment variable is set, it points at the `kb/` folder of the lenovo-skill repo:

```bash
python "$LENOVO_KB_DIR/kb.py" fact "<terms>"      # curated facts, full-text search
python "$LENOVO_KB_DIR/kb.py" part <FC>            # MTMs seen on + TCE-proven or not
python "$LENOVO_KB_DIR/kb.py" tce <MTM>            # parts proven TCE on an MTM
python "$LENOVO_KB_DIR/kb.py" find <MTM> <regex>   # search descriptions on an MTM
python "$LENOVO_KB_DIR/kb.py" errors               # DCSC gating messages, verbatim
python "$LENOVO_KB_DIR/kb.py" docs "<query>"       # local Lenovo Press index
python "$LENOVO_KB_DIR/kb.py" sql "<SELECT ...>"   # read-only ad-hoc SQL
```

If the variable is unset or the command fails, say the KB was not available and continue. `references/kb-usage.md` has the schema and the FTS5 syntax traps.

## Step 2: Lenovo Press

`references/lenovo-press-docs.md` maps each platform to its guide id. Prefer the local index. If web search is enabled, fetch `https://lenovopress.lenovo.com/lpNNNN` or `.../lpNNNN.pdf`. If you cannot read the section you need, say so rather than paraphrase it.

## Step 3: reading a DCSC export

If the user gives you an `.xlsx` export, parse it with Python (`openpyxl`, `data_only=True`):

- The `Quote` sheet has the feature code in column A, the description in C, the quantity in E and the per-unit price in F.
- BU1E present means TCE.
- The `Message History` sheet holds the warnings and criticals.
- Total Part Price reads back empty, so compute qty x unit.
- The group quantity is only in the zip's `.xml` (`<ConfigurationGroupLineItem><quantity>`).

## Step 4: competitor BOM conversions

Map line by line against the target platform's product guide. For each line:

1. Record the TCE column.
2. Check `references/facts.md` for crosswalks and traps.
3. Add the forced companions (fans, DIMM fillers, risers, cable kits, optics).
4. List what you could not map.

Only a BU1E export proves the result is TCE.

## Hard rules (full list in references/hard-rules.md)

- TCE is proven only by BU1E, and it is all-or-nothing. It rotates per MTM per date, and its lists have floors as well as ceilings.
- A rack chassis, or a tied order holding non-TCE product, voids TCE.
- U.3 NVMe blocks TCE. Tri-mode is 940-series only.
- Software-defined storage needs raw drives.
- Write TB, never TiB.
- Separate absence of evidence from proof of prohibition, and what DCSC built from what Lenovo supports.

## Output

Lead with the answer. Put the evidence in a table with sources. Mark every claim proven, flagged or unknown. End with the exact question to put to Lenovo if anything is unresolved. Say "Top Choice Express (TCE)", never "quick-ship". Never give prices from memory.
