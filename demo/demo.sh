#!/bin/bash
# demo.sh - runs the SCL-Toolkit demo on a virtual display (Xvfb :99)
# and records a video + screenshots. Everything happens off-screen.
set -e

export DISPLAY=:99
Xvfb :99 -screen 0 1280x800x24 &
XVFB_PID=$!
sleep 2

# Minimal window manager so windows behave normally
openbox &
sleep 1

# Record the whole session; -t makes ffmpeg exit cleanly (writes moov atom)
ffmpeg -y -f x11grab -video_size 1280x800 -framerate 10 -t 90 -i :99 \
  -c:v libx264 -preset ultrafast -pix_fmt yuv420p -movflags +faststart /out/scl-demo.mp4 &
FF_PID=$!
sleep 2

# Terminal window at a fixed position
xterm -geometry 118x40+40+40 -fa Monospace -fs 11 -e bash &
sleep 2
# Make sure the terminal actually has focus before we start typing
xdotool search --class xterm windowactivate --sync 2>/dev/null || true
sleep 1

type_and_run() {
  local txt="$1"
  xdotool type --delay 40 "$txt"
  xdotool key Return
  sleep "$2"
}

# --- demo 1: generic formatter ---
type_and_run 'echo "=== SCL-Toolkit demo ==="' 1
type_and_run 'python3 generic_formatter.py sample_contacts.csv --rename "phone:Mobile" --drop "notes" -o /tmp/formatted.xlsx' 5
type_and_run 'python3 -c "import pandas as pd; print(pd.read_excel(\"/tmp/formatted.xlsx\").to_string())"' 3

# --- demo 2: pdf merger ---
type_and_run 'python3 - <<"PY"
from pypdf import PdfWriter
for n in ["a","b","c"]:
    w = PdfWriter(); w.add_blank_page(width=300, height=400); w.write(f"/tmp/{n}.pdf")
print("made a,b,c test PDFs")
PY' 3
type_and_run 'python3 pdf_merger.py --files /tmp/c.pdf /tmp/a.pdf /tmp/b.pdf -o /tmp/merged.pdf' 3
type_and_run 'python3 -c "from pypdf import PdfReader; print(\"merged pages:\", len(PdfReader(\"/tmp/merged.pdf\").pages))"' 2

# --- demo 3: whatsapp sender dry-run ---
type_and_run 'python3 whatsapp_bulk_sender.py sample_contacts.csv --dry-run --template "Hi {name}, this is a test."' 4

# Screenshot of the final state
import -window root /out/scl-demo-final.png
type_and_run 'echo "Demo complete. Outputs: /tmp/formatted.xlsx /tmp/merged.pdf"' 2

sleep 2
# Wait for ffmpeg to finish writing (it self-terminates after -t 90)
wait $FF_PID 2>/dev/null || true
kill $XVFB_PID 2>/dev/null || true
echo "DONE"