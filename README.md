# SCL-Toolkit

Small utilities I built for day-to-day work: turn messy contact lists into
clean Excel sheets, merge PDFs, and send personalized WhatsApp messages to
a list of contacts. Each tool is standalone, plain Python, and runs on any
Windows machine.

## What's inside

### Generic Formatter

Takes CSV, JSON, or XLSX input and produces a clean, styled Excel sheet.
Rename columns, drop the ones you don't need, blank out null tokens, keep
only a subset. It makes no assumptions about your data; it adapts to
whatever structure you throw at it.

```
python generic_formatter.py contacts.csv --rename "name:Full Name" --drop notes
```

### PDF Merger

Concatenates PDFs in exactly the order you list them. GUI mode lets you
add, reorder, and watch a folder; CLI mode is one line.

```
python pdf_merger.py --files a.pdf b.pdf c.pdf -o out.pdf
```

### WhatsApp Bulk Sender

Sends personalized WhatsApp messages to a contact list from Excel or CSV.
Persistent QR login, a `{name}` placeholder in your template, pacing
between sends, and a per-contact log. It always starts in dry-run so you
can review exactly what would be sent before anything goes out.

```
python whatsapp_bulk_sender.py contacts.xlsx --template "Hi {name}, ..." --dry-run
```

## Install

```
pip install -r requirements.txt
# only needed for the WhatsApp tool:
playwright install chromium
```

## GUI

Not comfortable with the command line? Run the launcher and pick a tool
from the menu; it handles file selection for you.

```
python launcher.py
```

## Docs

- [User manual](USER_MANUAL.md): step-by-step for each tool, with both GUI and CLI paths
- [Demo](demo/out/scl-demo.mp4): the tools in action

## Notes

The WhatsApp tool is a rebuild; the original source was lost, so this
version was written from scratch with a safer flow (dry-run + confirmation
gate). See `LICENSE` for licensing.

---

## Merged: SCL-Momentum (2026-10-20)

SCL-Momentum (github.com/Somewhatmilk/SCL-Momentum, commit 6a7c65c) was merged into this
repo on branch `merge-momentum` as a **copy** — the original repository is untouched. All
its tracked files live under `tools/momentum/`:

| Path | What it is |
|---|---|
| `tools/momentum/chatbot.py` | Streamlit + LangChain RAG chatbot prototype (local LLM QA over documents) |
| `tools/momentum/excel_data.py` | Junction-box dimensions → Excel (`output_data.xlsx`); renamed from `Excel Data.py` (space breaks CLI) — see `tools/momentum/PROVENANCE.md` |
| `tools/momentum/config.toml` | Streamlit theme (inert at this path — Streamlit loads `.streamlit/config.toml`) |
| `tools/momentum/README.md` | Original Momentum README, preserved verbatim |
| `tools/momentum/LICENSE` | AGPLv3 — note: this repo's own license is GPLv3; both kept alongside their code |
| `tools/momentum/requirements.txt` | Momentum's original dependency list (provenance) |
| `tools/momentum/.gitignore` | Momentum's original ignore file (provenance) |

Status notes: `chatbot.py` is a non-runnable prototype as merged — it imports
`constants.CHROMA_SETTINGS` but `constants.py` is absent, and it loads `google/flan-t5-xxl`
(~22 GB) at import time. `secrets.toml` / `.env` were **not** copied (never committed in the
source repo; both now covered by this repo's `.gitignore`).

## Tools at a glance

| Tool | File | Purpose |
|---|---|---|
| Generic Formatter | `generic_formatter.py` | CSV/JSON/XLSX → clean styled Excel |
| PDF Merger | `pdf_merger.py` | Concatenate PDFs, GUI + CLI |
| WhatsApp Bulk Sender | `whatsapp_bulk_sender.py` | Personalized WhatsApp messages, dry-run first |
| GUI Launcher | `launcher.py` | Menu UI for all tools |
| RAG Chatbot (prototype) | `tools/momentum/chatbot.py` | Document QA chatbot (LLM stack, heavy) |
| Excel Export (demo) | `tools/momentum/excel_data.py` | Hardcoded dimensions → Excel |

## Consolidated deps

`requirements.txt` = original SCL-Toolkit core + Momentum's LLM stack (comment-grouped).
The two dependency sets share no package names, so the merge is conflict-free; Momentum's
`excel_data.py` needs only pandas + openpyxl, both already in core.