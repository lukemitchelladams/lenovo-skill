# Using the local knowledge base

The KB is optional. It is a SQLite file built from **your own** DCSC exports plus the public Lenovo Press guides. Nothing in it ships with this repo. Build it once:

```bash
pip install -r requirements.txt
python kb/refresh.py ~/Downloads ~/Desktop/Configs     # folders that hold your DCSC exports
python docs/get_lenovo_docs.py                         # ~230 MB of public product guides
python kb/build_kb_index.py --docs-only                # page-level full-text index
```

The KB lives at `kb/dcsc_kb.sqlite` (override with `LENOVO_KB_DB`).

## Commands (`python kb/kb.py ...`)

| Command | What it answers |
|---|---|
| `fact <terms>` | Curated verified facts. **Run this first, every time.** Works even with no database built. |
| `fact --titles <terms>` | Just the titles, which is cheap. |
| `part <FC>` | Every MTM a feature code was seen on, whether it was TCE-proven there, and its price history. |
| `tce <MTM>` | Every part proven TCE-buildable on that MTM, by category. |
| `find <MTM> <regex>` | Search part descriptions seen on an MTM. |
| `errors` | Every Critical/Error gating message DCSC ever emitted. These are the real configurator rules, verbatim. |
| `configs [regex]` | List configs. |
| `cmp <idA> <idB>` | Diff two configs. |
| `docs <query> [--lp lpNNNN]` | Which Lenovo Press guide and page holds something. |
| `page <lp> <page>` | One full page of a guide. |
| `sql "<SELECT ...>"` | Read-only ad-hoc query, capped at 200 rows. |

## Schema

- `config(id, file, name, mtime, mtm, model, nodes, tce, criticals, total, sig)`: `tce=1` means the export carried **BU1E**.
- `part(cfg, fc, descr, qty, unit, cat)`: `unit` is the per-unit price; `qty` is the total across all nodes.
- `msg(cfg, severity, text)`: DCSC warnings and criticals.
- `fact` / `fact_fts`: curated rules.
- `doc_fts(lp, title, page, text)`: the Lenovo Press corpus, one row per page.

## Workhorse queries

Keep result sets small: always `GROUP BY` and `LIMIT`, and use `substr(descr,1,60)`.

```sql
-- Is this part TCE, and on which platforms?
SELECT c.model, c.tce, COUNT(DISTINCT c.id) cfgs
FROM part p JOIN config c ON c.id=p.cfg WHERE p.fc='<FC>' GROUP BY c.model, c.tce;

-- TCE-eligible options in a category on a platform
SELECT p.fc, substr(p.descr,1,60) descr, COUNT(DISTINCT c.id) cfgs,
       SUM(CASE WHEN c.tce=1 THEN 1 ELSE 0 END) tce_cfgs
FROM part p JOIN config c ON c.id=p.cfg
WHERE p.descr LIKE '%<keyword>%' AND c.model LIKE '%<model>%'
GROUP BY p.fc, p.descr ORDER BY tce_cfgs DESC;

-- What else is in configs that use this part? (finds required companions)
SELECT p.fc, substr(p.descr,1,60), COUNT(*) n FROM part p
WHERE p.cfg IN (SELECT cfg FROM part WHERE fc='<FC>') GROUP BY p.fc ORDER BY n DESC LIMIT 40;

-- Does part A ever coexist with part B? (evidence for or against compatibility)
SELECT COUNT(DISTINCT p1.cfg) FROM part p1 JOIN part p2 ON p1.cfg=p2.cfg
WHERE p1.fc='<A>' AND p2.fc='<B>';
```

## FTS5 syntax that bites

- Quote any hyphenated or punctuated term: `'"10GBASE-T"'`, not `10GBASE-T`, which is a syntax error.
- Quote multi-word phrases: `'"failover is not supported"'`.
- The column filter is `lp:lp1971`, and `NEAR("term a" "term b", 10)` works for proximity.
- Boolean operators are `AND`, `OR` and `NOT`, in uppercase.

## Why a local index beats fetching

Web fetch tools summarize large product guides and routinely miss deep sections. In one case a fetch of the SR650a V4 guide reported it could not find a field-upgrade section that a local search of the same PDF found at once. Before concluding Lenovo Press is silent on something, search the local copy.
