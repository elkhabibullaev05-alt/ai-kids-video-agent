#!/usr/bin/env bash
# Server tekshiruvi. Ishlatish (root bo'lib):
#   curl -sSL https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/doctor.sh | bash
# Natijani to'liq nusxalab Claude'ga yuboring. Parol yoki token chiqarilmaydi.
DIR=/opt/kanal/repo
ok(){ echo "  [OK]  $*"; }; bad(){ echo "  [XATO] $*"; }
echo "=== kanal server tekshiruvi $(date -u +%F' '%H:%M) UTC, host $(hostname) ==="
echo "CPU $(nproc) | RAM $(free -g | awk '/Mem/{print $2}') GB | disk bo'sh $(df -h / | awk 'NR==2{print $4}')"
[ -d $DIR/.git ] && ok "repo bor" || { bad "repo yo'q → install.sh ishlamagan. Qayta: curl -sSL https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/install.sh | bash -s KANAL"; exit; }
CH=$(crontab -l 2>/dev/null | grep -o 'worker.py [a-z]*' | awk '{print $2}' | head -1)
[ -n "$CH" ] && ok "cron bor, kanal: $CH" || bad "cron yo'q → install.sh oxirigacha ishlamagan"
[ -x /opt/bl/blender-4.2.3-linux-x64/blender ] && ok "Blender bor" || bad "Blender yo'q"
[ -s /opt/kokoro/kokoro.onnx ] && ok "Kokoro ovoz bor" || bad "Kokoro yo'q"
command -v ffmpeg >/dev/null && ok "ffmpeg bor" || bad "ffmpeg yo'q"
python3 -c "import googleapiclient, google.oauth2" 2>/dev/null && ok "Google kutubxona bor" || bad "Google kutubxona yo'q"
cd $DIR
if GIT_TERMINAL_PROMPT=0 timeout 30 git push --dry-run -q origin HEAD:main 2>/tmp/kp.err; then ok "GitHub'ga yozish ishlaydi (deploy key)"
else bad "GitHub'ga yozib bo'lmadi → deploy key qo'shilmagan yoki 'Allow write access' belgilanmagan. Kalit:"; cat /root/.ssh/kanal_deploy.pub 2>/dev/null; sed 's/^/        /' /tmp/kp.err | head -3; fi
if [ -n "$CH" ]; then
  T=/root/kanal/$CH/token.json
  if [ -s $T ]; then
    python3 - "$T" <<'EOF' && ok "YouTube token ishlaydi" || bad "token ishlamadi (yuqoridagi xabar)"
import sys; sys.path.insert(0, "cloud"); import youtube_up as y
c = y.client(sys.argv[1]); r = c.channels().list(part="snippet", mine=True).execute()["items"][0]
print("        kanal:", r["snippet"]["title"], r["id"])
EOF
  else bad "token yo'q: $T  → kompyuterda cloud/auth.py bilan oling va shu joyga ko'chiring"; fi
  echo "--- worker.log oxiri ---"; tail -15 /root/kanal/$CH/worker.log 2>/dev/null || echo "  (log yo'q — worker hali ishlamagan)"
fi
