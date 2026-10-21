# SCL-Toolkit

Small utilities for day-to-day work: turn messy contact lists into clean
Excel sheets, merge PDFs, and send personalized WhatsApp messages to a list
of contacts. Each tool is standalone, plain Python, and runs on any Windows
machine.

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

### RAG Chatbot

A Streamlit + LangChain document-QA chatbot that answers questions over a
local document store using an LLM. Runs fully local; see
`tools/momentum/` for the source.

### Excel Export

Exports junction-box dimensions to a styled Excel sheet (`output_data.xlsx`)
from hardcoded measurement data.

## Tools at a glance

| Tool | File | Purpose |
|---|---|---|
| Generic Formatter | `generic_formatter.py` | CSV/JSON/XLSX → clean styled Excel |
| PDF Merger | `pdf_merger.py` | Concatenate PDFs, GUI + CLI |
| WhatsApp Bulk Sender | `whatsapp_bulk_sender.py` | Personalized WhatsApp messages, dry-run first |
| GUI Launcher | `launcher.py` | Menu UI for all tools |
| RAG Chatbot (prototype) | `tools/momentum/chatbot.py` | Document QA chatbot (LLM stack) |
| Excel Export | `tools/momentum/excel_data.py` | Junction-box dimensions → Excel |

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

## License

See [LICENSE](LICENSE).