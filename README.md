# SCL-Toolkit

A small, growing set of everyday utility tools that SCL Systems work spun off.
Each tool is standalone, plain-Python, and works on any Windows machine.

**Formerly `Personal-Projects`.** Renamed 2026-10-12 so the repo says what it
actually contains.

## Tools

| Tool | What it does | Run it |
|---|---|---|
| `generic_formatter.py` | Adapts **any** structured data (CSV/JSON/XLSX) to a clean, styled Excel sheet. Column renames, drops, null-token handling, numeric coercion, frozen header, auto filter. No domain assumptions. | `python generic_formatter.py contacts.csv --rename "name:Full Name" --drop "notes"` |
| `pdf_merger.py` | Concatenates PDFs in exactly the order you list them, CLI or GUI (add, reorder, watch folder, merge, optional delete-after). | `python pdf_merger.py --files a.pdf b.pdf c.pdf -o out.pdf` |
| `whatsapp_bulk_sender.py` | Sends personalized WhatsApp messages to a contact list from Excel/CSV. Persistent QR login, `{name}` template, dry-run, pacing, per-contact log, confirmation gate. | `python whatsapp_bulk_sender.py contacts.xlsx --dry-run` |
| `test_script.py` | Original PDF merger GUI (kept for reference / fallback). | `python test_script.py` |

## Install

```bash
pip install -r requirements.txt
# optional, for the WhatsApp tool:
playwright install chromium
```

## Notes

- The old repo contained only PyInstaller build artifacts for the WhatsApp
  tool; the original `WhatsappV3.py` source was never committed and is gone
  from disk (OneDrive placeholder, folder deleted). The WhatsApp tool is a
  clean rebuild with the same purpose and a safer flow (dry-run + confirm).
- Deliberately AGPL-3.0-free: license is MIT for anything new; the legacy
  GUI kept GPL-3.0 as it was published. See `LICENSE`.