# ChatGPT custom GPT setup

You need a ChatGPT plan that can create GPTs.

1. Go to **Explore GPTs > Create > Configure**.
2. **Name:** Lenovo Presales (or whatever you like). **Description:** "Lenovo ThinkSystem/ThinkAgile builds, TCE and DCSC exports, from evidence."
3. **Instructions:** paste all of [`instructions.md`](instructions.md). It is under the 8,000-character limit; `python tools/build_references.py` checks this.
4. **Conversation starters:** one per line from [`conversation-starters.md`](conversation-starters.md).
5. **Knowledge:** upload the three files in [`knowledge/`](knowledge/):
   - `facts.md`: the curated fact library
   - `hard-rules.md`
   - `lenovo-press-docs.md`: the platform-to-guide index
6. **Capabilities:** turn on **Web Search** (for Lenovo Press) and **Code Interpreter & Data Analysis** (for parsing uploaded DCSC `.xlsx` exports). Image generation is not needed.
7. Save. Keep it **Only me** or **Anyone with the link** unless you want it in the GPT Store.

## Keeping it current

When `kb/kb_facts.py` changes, run `python tools/build_references.py` and re-upload `knowledge/facts.md`.

## Optional: your own export KB

If you built `kb/dcsc_kb.sqlite` from your own exports, you can upload it in a chat and ask the GPT to query it with Code Interpreter. **Do not** attach it as a GPT knowledge file if you will share the GPT: it contains your customers' configurations and pricing.
