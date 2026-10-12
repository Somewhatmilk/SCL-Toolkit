FROM python:3.11-slim

# Virtual display + input simulation + recording, all inside the container
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11-utils x11-apps xdotool xterm xfonts-base openbox ffmpeg imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas openpyxl pypdf

ENV DISPLAY=:99
WORKDIR /work
COPY . /work
CMD ["bash", "/work/demo/demo.sh"]