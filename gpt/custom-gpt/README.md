# ChatGPT custom GPT setup

You need a ChatGPT plan that can create GPTs.

1. Go to **Explore GPTs > Create > Configure**.
2. **Name:** Lenovo Presales (or whatever you like). **Description:** "Lenovo ThinkSystem/ThinkAgile builds, TCE and DCSC exports, from evidence."
3. **Instructions:** paste all of [`instructions.md`](instructions.md). It is under the 8,000-character limit; `python tools/build_references.py` checks this.
4. **Conversation starters:** one per line from [`conversation-starters.md`](conversation-starters.md).
5. **Knowledge:** upload the six files in [`knowledge/`](knowledge/):
   - `facts.md`: the curated fact library (160+ facts)
   - `hard-rules.md`
   - `platform-specs.md`: platform limits
   - `dcsc-gates.md`: DCSC gating messages
   - `lenovo-press-docs.md`: the platform-to-guide index
   - `lenovo-kb-tools.zip`: the Python tools plus the DCSC rules snapshot (265 MTMs, no prices)

   The zip comes from the [latest release](https://github.com/lukemitchelladams/lenovo-skill/releases/latest), or from `python tools/build_references.py`.
6. **Capabilities:** turn on **Web Search** (for Lenovo Press and the competitor map) and **Code Interpreter & Data Analysis**. Code Interpreter runs the tools, including matching competitor BOMs and validating BOMs and DCSC `.xlsx` exports. Image generation is not needed.
7. Save. Keep it **Only me** or **Anyone with the link** unless you want it in the GPT Store.

## Keeping it current

When `kb/kb_facts.py` changes, run `python tools/build_references.py` and re-upload `knowledge/facts.md`.

## Optional: your own export KB

If you built `kb/dcsc_kb.sqlite` from your own exports, you can upload it in a chat and ask the GPT to query it with Code Interpreter. **Do not** attach it as a GPT knowledge file if you will share the GPT: it contains your customers' configurations and pricing.
