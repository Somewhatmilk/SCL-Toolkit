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
