# SCL-Toolkit User Manual

Step-by-step instructions for all three tools. Two ways to use each one:
the **GUI** (the `launcher.py` menu, best for non-technical users) or the
**command line** (best for scripts and automation).

---

## 1. Install (once)

1. Make sure Python 3.9+ is installed: open a terminal and run `python --version`.
2. In this folder, run:
   ```
   pip install -r requirements.txt
   ```
3. Only for the WhatsApp tool, install a browser driver:
   ```
   playwright install chromium
   ```

You can skip step 3 if you will only use the formatter and the PDF merger.

---

## 2. Generic Formatter

**What it does:** converts CSV, JSON, or XLSX data into a clean, styled
Excel sheet. You can rename columns, drop columns, and blank out null
tokens like `N.A` or `-`.

### GUI path

1. Run `python launcher.py`.
2. Go to the **Format data** tab.
3. Click **Browse** and pick your input file.
4. Optional: enter renames as `old:new, old2:new2` and drops as
   `col1,col2`.
5. Click **Run**. The output file is written next to your input as
   `<input>_formatted.xlsx`.

### CLI path

```
python generic_formatter.py contacts.csv
python generic_formatter.py contacts.csv --rename "name:Full Name" --drop notes
python generic_formatter.py data.json --keep name,phone,email -o clean.xlsx
python generic_formatter.py data.csv --csv-out
```

| Option | Meaning |
|---|---|
| `--rename old:new` | Rename a column (repeatable) |
| `--drop a,b` | Drop these columns |
| `--keep a,b` | Keep only these columns (overrides `--drop`) |
| `--null a,b` | Tokens to treat as empty (default `N.A,N/A,-`) |
| `--sheet NAME` | Sheet name for XLSX input |
| `-o out.xlsx` | Output path (default `<input>_formatted.xlsx`) |
| `--csv-out` | Write CSV instead of styled Excel |

---

## 3. PDF Merger

**What it does:** joins PDFs into one file, in the order you choose.

### GUI path

1. Run `python launcher.py`.
2. Go to the **Merge PDFs** tab.
3. Click **Add PDFs** and select the files in the order you want them.
4. Use **Move up / Move down** to fix the order, **Remove** to drop one.
5. Set an output file name (or keep `merged.pdf`).
6. Click **Run**. The merged file appears in this folder.

### CLI path

```
python pdf_merger.py --files a.pdf b.pdf c.pdf -o out.pdf
```

Files are merged in the exact order you list them, left to right.

---

## 4. WhatsApp Bulk Sender

**What it does:** sends a personalized message to each contact in an Excel
or CSV list. The template can contain `{name}`, which is replaced with each
contact's name.

**Safety first:** the tool always starts in dry-run. Nothing is sent until
you confirm and run it for real.

### Contact file format

| name | phone |
|---|---|
| Alice | +1234567890 |
| Bob | +1987654321 |

The tool looks for columns named `name` and `phone` (case-insensitive).
A `message` column, if present, is used as the template for that row.

### GUI path

1. Run `python launcher.py`.
2. Go to the **WhatsApp sender** tab.
3. Pick your contacts file.
4. Enter a template, e.g. `Hi {name}, quick reminder about tomorrow.`
5. Leave **Dry run** checked for a preview. Click **Run**.
6. When the preview looks right, uncheck **Dry run** and click **Run**
   again. A confirmation prompt appears before anything is sent.

### CLI path

```
# preview only:
python whatsapp_bulk_sender.py contacts.xlsx --template "Hi {name}, ..." --dry-run

# send for real (you will be asked to confirm):
python whatsapp_bulk_sender.py contacts.xlsx --template "Hi {name}, ..."
```

| Option | Meaning |
|---|---|
| `--template TEXT` | Message template; `{name}` is replaced per contact |
| `--dry-run` | Print what would be sent, send nothing |
| `--min-delay S` / `--max-delay S` | Random wait between sends (default 4-9 s) |
| `--limit N` | Send to at most N contacts (0 = all) |

### First-time login

On the first real run, a QR code appears in the terminal (or a browser
window opens if you are on the GUI). Scan it with WhatsApp on your phone
(Menu > Linked devices > Link a device). The login is saved, so later runs
skip the QR step.

---

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| WhatsApp: `playwright` missing | Run `playwright install chromium` |
| QR code does not appear | Make sure you are running from a terminal, not double-clicking the script |
| Formatter output looks wrong | Try `--null ""` if your data uses other placeholder tokens |
| PDFs merged in wrong order | Order of `--files` IS the output order; check the GUI list |

## 6. What the output looks like

Demo video: `demo/out/scl-demo.mp4` (open it in any video player).
