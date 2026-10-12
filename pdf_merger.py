#!/usr/bin/env python3
"""pdf_merger.py - concatenate PDFs in any order, CLI or GUI.

CLI: order = argument order, exactly as you list them:
    python pdf_merger.py --files a.pdf b.pdf c.pdf --output combined.pdf

GUI: same merge tool with Move Up / Move Down reordering and a watch
folder (drag new PDFs in), kept for mouse-driven use.
"""
import argparse
import os
import sys

try:
    from PyPDF2 import PdfMerger as _LegacyMerger  # type: ignore
except ImportError:
    _LegacyMerger = None

try:
    from pypdf import PdfReader, PdfWriter  # pypdf >= 4 (modern API)
    _MODERN = True
except ImportError:
    _MODERN = False


def merge(files: list[str], output: str) -> None:
    if not files:
        raise SystemExit("No PDFs given.")
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        raise SystemExit("Missing files: " + ", ".join(missing))

    if _MODERN:
        writer = PdfWriter()
        for f in files:
            reader = PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)
        with open(output, "wb") as out:
            writer.write(out)
        print(f"Merged {len(files)} PDFs -> {output}")
        return

    if _LegacyMerger is None:
        raise SystemExit("pip install pypdf  (or PyPDF2) first")
    merger = _LegacyMerger()
    for f in files:
        merger.append(f)
    with open(output, "wb") as out:
        merger.write(out)
    merger.close()
    print(f"Merged {len(files)} PDFs -> {output}")


def cli() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--files", nargs="+", required=True, help="PDFs in the exact merge order")
    ap.add_argument("--output", "-o", default="merged.pdf", help="Output file")
    args = ap.parse_args()
    merge(args.files, args.output)
    return 0


def gui() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class MergerApp:
        def __init__(self, root):
            self.root = root
            root.title("PDF Merger")
            self.pdf_files: list[str] = []
            self.watched_directory = None
            self.setup_ui()

        def setup_ui(self):
            frame = tk.Frame(self.root); frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            self.listbox = tk.Listbox(frame, selectmode=tk.SINGLE, height=15, width=60, bg="white")
            self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.listbox.config(yscrollcommand=scrollbar.set)
            buttons = tk.Frame(self.root); buttons.pack(pady=10)
            for text, cmd in [("Add PDFs", self.add_pdfs), ("Watch Folder", self.watch_folder),
                              ("Remove", self.remove_selected), ("Move Up", self.move_up),
                              ("Move Down", self.move_down), ("Merge", self.merge_pdfs)]:
                tk.Button(buttons, text=text, command=cmd).pack(side=tk.LEFT, padx=4)
            self.delete_var = tk.BooleanVar()
            tk.Checkbutton(self.root, text="Delete originals after merge", variable=self.delete_var).pack()

        def refresh(self):
            self.listbox.delete(0, tk.END)
            for f in self.pdf_files:
                self.listbox.insert(tk.END, os.path.basename(f))

        def add_pdfs(self):
            files = filedialog.askopenfilenames(filetypes=[("PDF", "*.pdf")])
            for f in files:
                if f not in self.pdf_files:
                    self.pdf_files.append(f)
            self.refresh()

        def watch_folder(self):
            d = filedialog.askdirectory()
            if not d:
                return
            self.watched_directory = d
            observer = Observer()
            observer.schedule(FileSystemEventHandler(), path=d, recursive=False)
            observer.start()
            for f in sorted(os.listdir(d)):
                if f.lower().endswith(".pdf"):
                    self.pdf_files.append(os.path.join(d, f))
            self.refresh()

        def remove_selected(self):
            for i in reversed(self.listbox.curselection()):
                self.pdf_files.pop(i)
            self.refresh()

        def move_up(self):
            sel = self.listbox.curselection()
            if sel and sel[0] > 0:
                i = sel[0]
                self.pdf_files[i], self.pdf_files[i - 1] = self.pdf_files[i - 1], self.pdf_files[i]
                self.refresh()
                self.listbox.select_set(i - 1)

        def move_down(self):
            sel = self.listbox.curselection()
            if sel and sel[0] < len(self.pdf_files) - 1:
                i = sel[0]
                self.pdf_files[i], self.pdf_files[i + 1] = self.pdf_files[i + 1], self.pdf_files[i]
                self.refresh()
                self.listbox.select_set(i + 1)

        def merge_pdfs(self):
            if not self.pdf_files:
                messagebox.showwarning("No PDFs", "Add PDFs first.")
                return
            out = os.path.join(self.watched_directory or os.getcwd(), "Output_Merge.pdf")
            merge(self.pdf_files, out)
            if self.delete_var.get():
                for f in self.pdf_files:
                    try:
                        os.remove(f)
                    except OSError:
                        pass
            messagebox.showinfo("Done", f"Merged to {out}")

    root = tk.Tk()
    MergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv:
        gui()
    else:
        raise SystemExit(cli())