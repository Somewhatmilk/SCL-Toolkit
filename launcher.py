#!/usr/bin/env python3
"""SCL-Toolkit launcher: a friendly GUI wrapper around the three tools.

Pick a tool from the tabs, choose your files, press Run. Output from the
underlying script appears in the log pane.

Requires only the standard library (tkinter). The tools themselves need
their dependencies from requirements.txt.
"""

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))


def python_exe():
    """Prefer a project venv if present, else the current interpreter."""
    for venv in (".venv", ".venv-test", "venv"):
        cand = os.path.join(TOOL_DIR, venv, "Scripts", "python.exe")
        if os.path.exists(cand):
            return cand
    return sys.executable


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SCL-Toolkit")
        self.geometry("760x560")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)
        self._build_formatter_tab()
        self._build_merger_tab()
        self._build_whatsapp_tab()
        self.log = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.log.pack(fill="x", padx=8, pady=(0, 8))
        tk.Button(self, text="Run", command=self._run_selected).pack(pady=(0, 8))

    # ---------- tabs ----------

    def _build_formatter_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Format data")
        self.fmt_source = tk.StringVar()
        self.fmt_rename = tk.StringVar()
        self.fmt_drop = tk.StringVar()
        ttk.Label(tab, text="Input file (CSV / JSON / XLSX)").grid(row=0, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.fmt_source, width=50).grid(row=1, column=0, sticky="we")
        ttk.Button(tab, text="Browse", command=self._pick_fmt_source).grid(row=1, column=1)
        ttk.Label(tab, text="Rename columns (old:new, comma-separated)").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(tab, textvariable=self.fmt_rename, width=50).grid(row=3, column=0, sticky="we")
        ttk.Label(tab, text="Drop columns (comma-separated)").grid(row=4, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(tab, textvariable=self.fmt_drop, width=50).grid(row=5, column=0, sticky="we")
        tab.columnconfigure(0, weight=1)

    def _build_merger_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Merge PDFs")
        self.merger_files = []
        self.merger_out = tk.StringVar()
        self.merger_list = tk.Listbox(tab, height=8)
        self.merger_list.grid(row=0, column=0, rowspan=4, sticky="nsew")
        btns = ttk.Frame(tab)
        btns.grid(row=0, column=1, sticky="n", padx=(8, 0))
        ttk.Button(btns, text="Add PDFs", command=self._add_pdfs).pack(fill="x", pady=2)
        ttk.Button(btns, text="Move up", command=lambda: self._move_merger(-1)).pack(fill="x", pady=2)
        ttk.Button(btns, text="Move down", command=lambda: self._move_merger(1)).pack(fill="x", pady=2)
        ttk.Button(btns, text="Remove", command=self._remove_merger).pack(fill="x", pady=2)
        ttk.Label(tab, text="Output file").grid(row=4, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(tab, textvariable=self.merger_out, width=50).grid(row=5, column=0, sticky="we")
        ttk.Button(tab, text="Browse", command=self._pick_merger_out).grid(row=5, column=1)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _build_whatsapp_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="WhatsApp sender")
        self.wa_contacts = tk.StringVar()
        self.wa_template = tk.StringVar()
        self.wa_dryrun = tk.BooleanVar(value=True)
        self.wa_limit = tk.StringVar(value="0")
        ttk.Label(tab, text="Contacts file (Excel / CSV)").grid(row=0, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.wa_contacts, width=50).grid(row=1, column=0, sticky="we")
        ttk.Button(tab, text="Browse", command=self._pick_wa_contacts).grid(row=1, column=1)
        ttk.Label(tab, text="Message template ({name} is replaced)").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(tab, textvariable=self.wa_template, width=50).grid(row=3, column=0, sticky="we")
        ttk.Label(tab, text="Limit (0 = all contacts)").grid(row=4, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(tab, textvariable=self.wa_limit, width=10).grid(row=5, column=0, sticky="w")
        ttk.Checkbutton(tab, text="Dry run (preview only, send nothing)", variable=self.wa_dryrun).grid(
            row=6, column=0, sticky="w", pady=(8, 0)
        )
        tab.columnconfigure(0, weight=1)

    # ---------- file pickers ----------

    def _pick_fmt_source(self):
        path = filedialog.askopenfilename(
            title="Choose data file",
            filetypes=[("Data files", "*.csv *.json *.xlsx *.xls"), ("All files", "*.*")],
        )
        if path:
            self.fmt_source.set(path)

    def _add_pdfs(self):
        paths = filedialog.askopenfilenames(
            title="Choose PDFs in merge order", filetypes=[("PDF", "*.pdf")]
        )
        for p in paths:
            self.merger_files.append(p)
            self.merger_list.insert(tk.END, os.path.basename(p))

    def _move_merger(self, delta):
        sel = self.merger_list.curselection()
        if not sel:
            return
        i = sel[0]
        j = i + delta
        if 0 <= j < len(self.merger_files):
            self.merger_files[i], self.merger_files[j] = self.merger_files[j], self.merger_files[i]
            self.merger_list.delete(i)
            self.merger_list.insert(i, os.path.basename(self.merger_files[i]))
            self.merger_list.selection_set(j)

    def _remove_merger(self):
        for i in reversed(self.merger_list.curselection()):
            del self.merger_files[i]
            self.merger_list.delete(i)

    def _pick_merger_out(self):
        path = filedialog.asksaveasfilename(
            title="Output PDF", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if path:
            self.merger_out.set(path)

    def _pick_wa_contacts(self):
        path = filedialog.askopenfilename(
            title="Choose contacts file",
            filetypes=[("Contacts", "*.xlsx *.xls *.csv"), ("All files", "*.*")],
        )
        if path:
            self.wa_contacts.set(path)

    # ---------- run ----------

    def _run_selected(self):
        tab = self.notebook.index(self.notebook.select())
        if tab == 0:
            cmd = self._formatter_cmd()
        elif tab == 1:
            cmd = self._merger_cmd()
        else:
            cmd = self._whatsapp_cmd()
        if cmd is None:
            return
        self._log("$ " + " ".join(cmd) + "\n")
        threading.Thread(target=self._run_cmd, args=(cmd,), daemon=True).start()

    def _formatter_cmd(self):
        src = self.fmt_source.get().strip()
        if not src:
            messagebox.showwarning("Missing input", "Pick an input file first.")
            return None
        cmd = [python_exe(), os.path.join(TOOL_DIR, "generic_formatter.py"), src]
        if self.fmt_rename.get().strip():
            for pair in self.fmt_rename.get().split(","):
                pair = pair.strip()
                if ":" in pair:
                    cmd += ["--rename", pair]
        if self.fmt_drop.get().strip():
            cmd += ["--drop", self.fmt_drop.get().strip()]
        return cmd

    def _merger_cmd(self):
        if not self.merger_files:
            messagebox.showwarning("No files", "Add at least one PDF.")
            return None
        cmd = [python_exe(), os.path.join(TOOL_DIR, "pdf_merger.py"), "--files"]
        cmd += list(self.merger_files)
        cmd += ["-o", self.merger_out.get().strip() or "merged.pdf"]
        return cmd

    def _whatsapp_cmd(self):
        contacts = self.wa_contacts.get().strip()
        if not contacts:
            messagebox.showwarning("Missing input", "Pick a contacts file first.")
            return None
        cmd = [python_exe(), os.path.join(TOOL_DIR, "whatsapp_bulk_sender.py"), contacts]
        if self.wa_template.get().strip():
            cmd += ["--template", self.wa_template.get().strip()]
        if self.wa_dryrun.get():
            cmd.append("--dry-run")
        limit = self.wa_limit.get().strip()
        if limit and limit != "0":
            cmd += ["--limit", limit]
        return cmd

    def _run_cmd(self, cmd):
        try:
            proc = subprocess.run(
                cmd, cwd=TOOL_DIR, capture_output=True, text=True, timeout=3600
            )
            out = (proc.stdout or "") + (proc.stderr or "")
        except Exception as exc:
            out = f"Error: {exc}\n"
        self.log.config(state="normal")
        self.log.insert(tk.END, out.rstrip() + "\n\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")

    def _log(self, text):
        self.log.config(state="normal")
        self.log.insert(tk.END, text)
        self.log.see(tk.END)
        self.log.config(state="disabled")


if __name__ == "__main__":
    Launcher().mainloop()
