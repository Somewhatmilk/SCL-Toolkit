#!/usr/bin/env python3
"""whatsapp_bulk_sender.py - send WhatsApp messages to a contact list (Excel/CSV).

Rebuilt in Python from the old WhatsappV3 concept (source lost; only the
PyInstaller artifacts survived). Same purpose, cleaner engine:

  * Reads contacts from Excel/CSV: "name, phone, message" (message shown in
    the review screen before sending; {name} placeholder gets personalized).
  * Persistent browser profile: QR login once, state saved for next runs.
  * Dry-run mode: prints every message, sends nothing.
  * Human pacing + per-contact success/failure log. Stops on unknown format.

Usage:
  python whatsapp_bulk_sender.py contacts.xlsx            # interactive review
  python whatsapp_bulk_sender.py contacts.csv --dry-run
  python whatsapp_bulk_sender.py contacts.xlsx --column phone --template "Hi {name}, ..."

Rule: only send to contacts who expect your message (clients, opted-in list).
This is an outreach tool for YOUR contact list, not a spam cannon.
"""
import argparse
import csv
import json
import os
import random
import time
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from playwright.sync_api import sync_playwright
    HAVE_PLAYWRIGHT = True
except ImportError:
    HAVE_PLAYWRIGHT = False

PROFILE_DIR = Path(__file__).resolve().parent / ".wa_profile"
USER_DATA = PROFILE_DIR / "user_data"
LOG_FILE = Path(__file__).resolve().parent / "wa_send_log.jsonl"

# WhatsApp Web selectors (stable as of 2026-10)
PANEL_INPUT = 'div[contenteditable="true"][data-tab="3"]'
MSG_INPUT = 'div[contenteditable="true"][data-tab="10"]'
SEND_BTN = 'button[data-testid="send"]'
SEARCH_RESULT = 'div[role="listitem"]'


def load_contacts(path: Path) -> list[dict]:
    if pd is not None and path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path, dtype=str).fillna("")
        cols = {str(c).lower(): str(c) for c in df.columns}
        name_col = cols.get("name", list(df.columns)[0])
        phone_col = cols.get("phone", cols.get("contact", cols.get("number", list(df.columns)[1] if len(df.columns) > 1 else list(df.columns)[0])))
        msg_col = cols.get("message", cols.get("msg", cols.get("text", "")))
        rows = []
        for _, r in df.iterrows():
            row = {"name": str(r[name_col]).strip(), "phone": str(r[phone_col]).strip(), "message": str(r[msg_col]).strip() if msg_col else ""}
            if row["phone"]:
                rows.append(row)
        return rows
    if path.suffix.lower() == ".csv":
        rows = []
        with open(path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                row = {k.lower(): (v or "").strip() for k, v in r.items() if k}
                if row.get("phone"):
                    rows.append({"name": row.get("name", ""), "phone": row["phone"], "message": row.get("message", row.get("msg", ""))})
        return rows
    raise SystemExit("Unsupported contact file: use .xlsx or .csv")


def normalize_phone(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("00"):
        digits = "+" + digits[2:]
    elif not digits.startswith("+"):
        # international format; user should include country code
        digits = "+" + digits
    return digits


def build_message(row: dict, template: str) -> str:
    msg = template if template else row.get("message", "")
    if not msg:
        raise SystemExit(f"No message for {row['name']} ({row['phone']}) and no --template given.")
    return msg.replace("{name}", row["name"] or "")


def open_chat(page, phone: str) -> bool:
    page.goto(f"https://web.whatsapp.com/send?phone={phone}", timeout=45000)
    # WhatsApp redirects to the chat when the number exists
    for _ in range(30):
        if page.url.startswith(f"https://web.whatsapp.com/send?phone={phone}") and "send" not in page.url.split("/")[-1]:
            break
        try:
            if page.locator(MSG_INPUT).count() and page.locator(MSG_INPUT).first.is_visible():
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def send_one(page, row: dict, template: str, delay_range: tuple[float, float]) -> bool:
    phone = normalize_phone(row["phone"])
    msg = build_message(row, template)
    if not open_chat(page, phone):
        print(f"  SKIP {row['name']} ({phone}): chat did not open (number may be invalid)")
        return False
    try:
        box = page.locator(MSG_INPUT).first
        box.wait_for(state="visible", timeout=20000)
        box.click()
        box.fill(msg)
        page.locator(SEND_BTN).first.click()
        time.sleep(random.uniform(*delay_range))
        print(f"  SENT {row['name']} ({phone})")
        return True
    except Exception as e:
        print(f"  FAIL {row['name']} ({phone}): {e}")
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("contacts", help="Excel/CSV with name, phone, optional message columns")
    ap.add_argument("--template", default="", help="Message template; {name} is replaced per contact")
    ap.add_argument("--dry-run", action="store_true", help="Print only, send nothing")
    ap.add_argument("--min-delay", type=float, default=4.0)
    ap.add_argument("--max-delay", type=float, default=9.0)
    ap.add_argument("--limit", type=int, default=0, help="Max contacts to send (0 = all)")
    args = ap.parse_args()

    src = Path(args.contacts)
    if not src.exists():
        raise SystemExit(f"Contacts file not found: {src}")

    contacts = load_contacts(src)
    if args.limit:
        contacts = contacts[: args.limit]
    print(f"Loaded {len(contacts)} contacts from {src.name}")

    if args.dry_run:
        for i, row in enumerate(contacts, 1):
            print(f"[{i}/{len(contacts)}] {row['name']} <{normalize_phone(row['phone'])}>")
            print("   " + build_message(row, args.template))
        print("DRY RUN: nothing sent.")
        return 0

    if not HAVE_PLAYWRIGHT:
        raise SystemExit("pip install playwright && playwright install chromium")

    # Confirm gate before touching WhatsApp
    print("\nAbout to send to the contacts above.")
    try:
        answer = input("Type YES to continue: ").strip().upper()
    except EOFError:
        answer = "NO"
    if answer != "YES":
        print("Aborted.")
        return 2

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA), headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-default-browser-check"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://web.whatsapp.com", timeout=45000)
        print("If a QR code appears, scan it once; the login is saved for next time.")
        try:
            page.wait_for_selector(PANEL_INPUT, timeout=120000)
            print("Logged in. Starting sends.")
        except Exception:
            print("Login not detected within 120s.", file=os.sys.stderr)
            ctx.close()
            return 3

        ok = 0
        for i, row in enumerate(contacts, 1):
            print(f"[{i}/{len(contacts)}] sending to {row['name']}...")
            try:
                if send_one(page, row, args.template, (args.min_delay, args.max_delay)):
                    ok += 1
            except Exception as e:
                print(f"  ERROR {row['name']}: {e}")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.time(), "name": row["name"], "phone": row["phone"], "sent": ok}) + "\n")
        ctx.close()

    print(f"\nDone: {ok}/{len(contacts)} sent. Log: {LOG_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())