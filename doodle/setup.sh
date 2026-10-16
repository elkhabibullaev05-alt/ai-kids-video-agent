#!/usr/bin/env bash
# One-time setup for the Doodle Desk engine (Linux). Safe to re-run.
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages cairocffi kokoro-onnx soundfile numpy pillow fonttools brotli 2>/dev/null || pip install -q cairocffi kokoro-onnx soundfile numpy pillow fonttools brotli
mkdir -p models
[ -s models/kokoro.onnx ] || curl -sSL -o models/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s models/voices.bin ] || curl -sSL -o models/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
# handwriting fonts (Kalam, Patrick Hand) from npm @fontsource, converted to TTF
if ! fc-list | grep -qi kalam; then
  T=$(mktemp -d); (cd "$T" && npm pack -s @fontsource/kalam@5.3.0 @fontsource/patrick-hand@5.3.0 >/dev/null && for f in *.tgz; do tar xzf "$f"; mv package "p_${f%.tgz}"; done)
  python3 - "$T" <<'PY'
import sys, glob, os
from fontTools.ttLib import TTFont
T = sys.argv[1]; d = os.path.expanduser("~/.fonts"); os.makedirs(d, exist_ok=True)
for pat, name in [("*kalam*/files/kalam-latin-700-normal.woff", "Kalam-Bold.ttf"), ("*kalam*/files/kalam-latin-400-normal.woff", "Kalam-Regular.ttf"),
                  ("*patrick*/files/patrick-hand-latin-400-normal.woff", "PatrickHand-Regular.ttf")]:
    f = TTFont(glob.glob(os.path.join(T, pat))[0]); f.flavor = None; f.save(os.path.join(d, name))
PY
  fc-cache -f >/dev/null 2>&1 || true
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
echo "setup ok"
