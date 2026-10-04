#!/bin/sh
# encode45.sh <frames_dir> <out.mp4>  — 60fps frames + music45.wav -> 30fps with 2-frame motion blur
ffmpeg -v error -y -framerate 60 -i "$1/f%05d.png" -i music45.wav -filter_complex "[0:v]tmix=frames=2:weights='1 1',fps=30,format=yuv420p[v]" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 17 -movflags +faststart -c:a aac -b:a 192k -shortest "$2"
