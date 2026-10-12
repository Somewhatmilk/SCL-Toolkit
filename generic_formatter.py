#!/usr/bin/env python3
"""Generic data formatter: adapts any structured input to a clean Excel/CSV output.

Reads CSV, JSON (list of objects, array of arrays, or {rows: [...]}),
or existing XLSX; normalizes columns, types, missing values; and writes
a styled .xlsx with header row, frozen pane, and auto column widths.

Usage:
  python generic_formatter.py source.csv
  python generic_formatter.py source.csv --output cleaned.xlsx
  python generic_formatter.py source.json --rename "old name:New Name" --drop "colA,colB"
  python generic_formatter.py source.xlsx --sheet "Data" --null "N.A,N/A,-"

Design goal: no hardcoded domain assumptions. Column mapping, filters,
and formatting come from CLI flags or a YAML config. Swap in any file
with any columns and it adapts.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    import pandas as pd
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False


NULL_TOKENS = {"", "n.a", "n/a", "na", "-", "none", "null", "nan"}


def load_frame(path: Path, sheet: str | None = None) -> "pd.DataFrame":
    """Read any supported input into a DataFrame."""
    if not HAVE_PANDAS:
        raise SystemExit("Requires pandas + openpyxl:  pip install pandas openpyxl")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "rows" in data:
            data = data["rows"]
        return pd.DataFrame(data).astype(str)
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=sheet or 0, dtype=str, keep_default_na=False)
    raise SystemExit(f"Unsupported input type: {suffix}")


def normalize(df: "pd.DataFrame", nulls: list[str]) -> "pd.DataFrame":
    """Trim whitespace, blank out null tokens, coerce obvious numerics."""
    df = df.apply(lambda col: col.astype(str).str.strip())
    for token in nulls:
        df = df.replace(token.strip(), "")
    for col in df.columns:
        cleaned = df[col].replace("", pd.NA)
        numeric = pd.to_numeric(cleaned, errors="coerce")
        if numeric.notna().mean() > 0.9 and numeric.notna().any():
            df[col] = numeric
    return df.fillna("")


def apply_renames(df: "pd.DataFrame", renames: list[str]) -> "pd.DataFrame":
    mapping = {}
    for spec in renames:
        if ":" in spec:
            old, new = spec.split(":", 1)
            mapping[old.strip()] = new.strip()
    return df.rename(columns=mapping)


def get_column_letter_or_name(df: "pd.DataFrame", col) -> str:
    idx = list(df.columns).index(col)
    return get_column_letter(idx + 1)


def save_styled_xlsx(df: "pd.DataFrame", out: Path, title: str) -> None:
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=title)
        ws = writer.sheets[title]
        header_fill = PatternFill("solid", fgColor="1F4E78")
        header_font = Font(bold=True, color="FFFFFF")
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
        ws.freeze_panes = "A2"
        for col in ws.columns:
            widths = [len(str(c.value)) if c.value is not None else 10 for c in col]
            ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(widths) + 2, 60)
        ws.auto_filter.ref = ws.dimensions


def write_csv(df: "pd.DataFrame", out: Path) -> None:
    df.to_csv(out, index=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="Input file: .csv, .json, .xlsx, .xls")
    ap.add_argument("--output", "-o", default=None, help="Output file (default: <source>_formatted.xlsx)")
    ap.add_argument("--sheet", default=None, help="Sheet name for xlsx input (default: first)")
    ap.add_argument("--out-sheet", default="Formatted", help="Output sheet name")
    ap.add_argument("--rename", action="append", default=[], help="'old:new' column rename, repeatable")
    ap.add_argument("--drop", default="", help="Comma-separated columns to drop")
    ap.add_argument("--null", default="N.A,N/A,-", help="Comma-separated null tokens to blank out")
    ap.add_argument("--keep", default="", help="Comma-separated subset of columns to keep (overrides --drop)")
    ap.add_argument("--csv-out", action="store_true", help="Write CSV instead of styled XLSX")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"Input not found: {src}", file=sys.stderr)
        return 1

    df = load_frame(src, args.sheet)
    df = apply_renames(df, args.rename)
    if args.keep:
        keep = [c.strip() for c in args.keep.split(",") if c.strip() in df.columns]
        df = df[keep]
    elif args.drop:
        drop = {c.strip() for c in args.drop.split(",") if c.strip()}
        df = df[[c for c in df.columns if c not in drop]]
    df = normalize(df, [t.strip() for t in args.null.split(",")])

    out = Path(args.output) if args.output else src.with_name(f"{src.stem}_formatted.xlsx")
    if args.csv_out:
        write_csv(df, out)
    else:
        save_styled_xlsx(df, out, args.out_sheet)

    print(f"Wrote {out}  ({len(df):,} rows x {len(df.columns)} cols)")
    print(f"Columns: {', '.join(map(str, df.columns))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())