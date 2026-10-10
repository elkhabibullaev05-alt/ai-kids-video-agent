#!/usr/bin/env bash
# One-time setup for the Dough Bros engine (Linux/macOS). Safe to re-run.
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages cairosvg kokoro-onnx soundfile numpy 2>/dev/null || pip install -q cairosvg kokoro-onnx soundfile numpy
mkdir -p models
[ -s models/kokoro.onnx ] || curl -sSL -o models/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s models/voices.bin ] || curl -sSL -o models/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
echo "setup ok"
