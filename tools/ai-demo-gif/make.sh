#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
DEMO=${1:-login}
set -a; . ~/.config/shadebrowse/env; set +a
export DISPLAY=:99
Xvfb :99 -screen 0 900x700x24 & XVFB=$!
sleep 1
ffmpeg -loglevel error -y -f x11grab -framerate 10 -video_size 900x700 -i :99 -vf crop=900:580:0:95 screen.mp4 & FFMPEG=$!
~/venv/bin/python record.py $DEMO
kill -INT $FFMPEG; wait $FFMPEG || true
kill $XVFB
~/venv/bin/python panels.py $DEMO
SKIP=$(~/venv/bin/python -c "import json; print(max(json.load(open('timeline.json'))[0]['at'] - 1, 0))")
ffmpeg -loglevel error -y -ss $SKIP -f concat -i panels.txt -ss $SKIP -i screen.mp4 -filter_complex \
  "[0:v]fps=10,format=rgb24,scale=-1:580[c];[1:v]format=rgb24[s];[c][s]hstack=inputs=2:shortest=1,scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" \
  $DEMO.gif
