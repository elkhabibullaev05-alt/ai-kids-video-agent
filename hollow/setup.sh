#!/usr/bin/env bash
# One-time setup for the Hollowmere engine (Linux). Safe to re-run.
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages cairosvg kokoro-onnx soundfile numpy pillow 2>/dev/null || pip install -q cairosvg kokoro-onnx soundfile numpy pillow
if [ ! -e models ]; then
  if [ -s ../doughbros/models/kokoro.onnx ]; then ln -s ../doughbros/models models; else mkdir -p models; fi
fi
[ -s models/kokoro.onnx ] || curl -sSL -o models/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s models/voices.bin ] || curl -sSL -o models/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
mkdir -p ~/.fonts && cp assets/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
echo "setup ok"
