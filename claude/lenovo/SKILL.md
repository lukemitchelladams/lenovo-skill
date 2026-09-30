---
name: lenovo
description: Answer any Lenovo data center hardware question from verified evidence (DCSC exports, curated facts, Lenovo Press) instead of model memory. Use for ANY question about Lenovo ThinkSystem, ThinkAgile, ThinkEdge, DCSC, Top Choice Express or TCE, BU1E, feature codes, MTMs, part numbers, drives, DIMMs, CPUs, GPUs, backplanes, RAID controllers, rail kits, PSUs, NICs, transceivers, racks, JBODs, storage arrays (DM/DG/DE/DS), HX/VX/MX/FX nodes, Nutanix on Lenovo, Azure Local on Lenovo, competitor-to-Lenovo BOM conversions (Dell, HPE, Cisco, Supermicro), build validation, field upgrades, thermal rules, or reading a DCSC export. Triggers on "lenovo", "DCSC", "TCE", "thinksystem", "thinkagile", "feature code", "is this TCE", "will this build", or a pasted MTM/feature code.
---

# Lenovo question protocol

Run every Lenovo hardware question through this before answering. **Do not answer Lenovo part, build or TCE questions from model knowledge.** Model knowledge of Lenovo feature codes is unreliable, and the catalogue rotates every few weeks.

## Source hierarchy, highest authority first

1. **A live DCSC export the user just gave you.** This beats everything: it is ground truth for that configuration on that date. If the user has one and has not shared it, ask for it.
2. **Curated facts:** `references/facts.md` in this skill folder. These are hand-verified rules that already cost real research.
3. **The user's local KB**, if they built one (see below). It holds their own DCSC exports. Only a BU1E export proves TCE.
4. **Lenovo Press** (`lenovopress.lenovo.com`). It is authoritative for specs, DWPD, thermal rules and TCE columns in product guides. It is often silent on field upgrades and configurator gating.
5. **Model knowledge.** Use it only for general concepts, and never for feature codes, TCE status or prices.

## Step 0: check the curated facts first

Grep `references/facts.md` for the feature code, MTM or platform name before doing anything else. Each fact is marked `proven`, `flagged` or `unknown`, with a verified date. Carry that status word into your answer. If a fact answers the question, say so and stop; do not re-derive a stored rule.

Always read `references/hard-rules.md` before answering a TCE, storage or export-reading question.

## Step 1: the local KB (Claude Code only, optional)

Check whether the user has built a KB: the `LENOVO_KB_DIR` environment variable points at the `kb/` folder of the lenovo-skill repo. Test it with the Bash tool:

```bash
python "$LENOVO_KB_DIR/kb.py" fact "<terms>"
```

On Windows PowerShell use `$env:LENOVO_KB_DIR`. If the variable is unset or the command fails, skip to Step 2 and say the KB was not available. Do not pretend it was checked.

When the KB is there:

- `kb.py fact <terms>`: the curated facts, full-text searched. Run this first.
- `kb.py part <FC>`: every MTM the part was seen on, and whether it was TCE-proven there.
- `kb.py tce <MTM>`: every part proven TCE-buildable on that MTM.
- `kb.py find <MTM> <regex>`: search part descriptions on an MTM.
- `kb.py errors`: every DCSC Critical/Error gating message, verbatim.
- `kb.py docs <query> [--lp lpNNNN]` then `kb.py page <lp> <page>`: search the local Lenovo Press index.
- `kb.py sql "<SELECT ...>"`: ad-hoc read-only SQL.

`references/kb-usage.md` has the schema, the workhorse queries and the FTS5 syntax traps. Keep result sets small: always use `GROUP BY` and `LIMIT`.

## Step 2: Lenovo Press

`references/lenovo-press-docs.md` maps each platform to its product guide id (for example SR630 V4 is `lp1971`). Use the local index (`kb.py docs`) when it exists; it finds deep table rows that web fetches miss. Otherwise fetch with WebFetch:

- `https://lenovopress.lenovo.com/lpNNNN` for the web page
- `https://lenovopress.lenovo.com/lpNNNN.pdf` for the full PDF

WebFetch summarizes large guides and often misses deep sections. If it does not return the section you need, **say so** and answer from the other evidence, flagging that you could not read the passage. Thermal tables live at `pubs.lenovo.com`, not Lenovo Press.

## Step 3: reading a DCSC export the user pastes or uploads

- BU1E present means TCE. BU1E absent means not TCE, whatever the filename says.
- The price column is per unit; compute qty x unit yourself. Total Part Price reads back empty.
- The xlsx never shows the config-group quantity. If the user has the zip, read `<ConfigurationGroupLineItem><quantity>` from the `.xml` before stating a server count or order total.
- Read the Message History sheet. Criticals block the build; warnings do not.
- Check the currency.

## Step 4: competitor BOM to Lenovo conversions

Map line by line to the target platform's product guide, not from memory:

1. Pick the platform on the competitor's constraints: sockets, depth, bays, GPU and PSU voltage.
2. For each line, find the Lenovo feature code in the guide and note its TCE column.
3. Check `references/facts.md` for known crosswalks and traps (NIC media, M.2 RAID, GPU companions, 545-8i limits).
4. Add the forced companions that guides require and auto-mappers miss: fans, DIMM fillers, risers, cable kits and optics.
5. List every line you could not map, and every assumption, separately.
6. Tell the user that only a DCSC export with BU1E proves the build is TCE.

## Hard rules (full list in references/hard-rules.md)

- TCE is proven only by BU1E in a DCSC export, and it is all-or-nothing.
- TCE rotates per MTM per date, and it has floors as well as ceilings. Never extrapolate to a bigger or smaller variant.
- A rack chassis, or a tied order holding non-TCE product, voids TCE.
- U.3 NVMe blocks TCE. Tri-mode is 940-series only.
- Software-defined storage needs raw drives.
- Write TB, never TiB.
- Separate absence of evidence from proof of prohibition, and what DCSC **built** from what Lenovo **supports**.

## Output

Lead with the answer. Show the evidence as a table with sources, and config counts where you have them. Mark every claim as **proven**, **flagged** or **unknown**. End with the precise question to put to Lenovo or the DCSC panel if anything is still unresolved.

In customer-facing writing, say "Top Choice Express (TCE)" and never "quick-ship". Give no prices from memory; prices come only from a current export.
