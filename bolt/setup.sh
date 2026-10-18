#!/usr/bin/env bash
# One-time setup for the Inspector Bolt engine (Linux, cloud workspace). Safe to re-run.
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages kokoro-onnx soundfile numpy pillow 2>/dev/null || pip install -q kokoro-onnx soundfile numpy pillow
# Blender 4.2.3 LTS (portable, headless EEVEE)
BL=/opt/bl/blender-4.2.3-linux-x64/blender
if [ ! -x "$BL" ]; then
  mkdir -p /opt/bl && curl -sSL https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz | tar xJ -C /opt/bl
fi
command -v xvfb-run >/dev/null || (apt-get install -y -qq xvfb libegl1 libgl1 >/dev/null 2>&1 || true)
# Kokoro TTS models
mkdir -p /opt/kokoro
[ -s /opt/kokoro/kokoro.onnx ] || curl -sSL -o /opt/kokoro/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s /opt/kokoro/voices.bin ] || curl -sSL -o /opt/kokoro/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
"$BL" -b --factory-startup --python-expr "import bpy;print('blender ok', bpy.app.version_string)" 2>/dev/null | grep "blender ok"
echo "setup ok"
