#!/bin/bash
# demo.sh - drives the SCL-Toolkit GUI launcher on a virtual display (Xvfb :99)
# and records a video + screenshot. Everything happens off-screen.
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

# Create sample PDFs for the merger demo (self-contained; pypdf is installed)
python3 - <<'PY'
from pypdf import PdfWriter
for n in ["sample_a", "sample_b"]:
    w = PdfWriter()
    w.add_blank_page(width=300, height=400)
    w.write(f"/work/{n}.pdf")
print("sample PDFs created")
PY
sleep 1

# Start the launcher GUI in demo mode (SCL_DEMO=1 drives the tabs itself)
SCL_DEMO=1 python3 launcher.py &
LAUNCH_PID=$!

# Wait for the demo to finish (it self-drives; the video captures everything).
# ffmpeg self-terminates after -t 90, so cap the wait there.
sleep 60

# Screenshot of the final state
import -window root /out/scl-demo-final.png

# Copy tool outputs out so the run is provable from the host side
cp -f /work/sample_contacts_formatted.xlsx /work/demo_merged.pdf /out/ 2>/dev/null || true

# Wait for ffmpeg to finish writing (it self-terminates after -t 90)
wait $FF_PID 2>/dev/null || true
kill $LAUNCH_PID 2>/dev/null || true
kill $XVFB_PID 2>/dev/null || true
echo "DONE"
