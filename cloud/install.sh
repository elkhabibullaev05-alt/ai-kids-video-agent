#!/usr/bin/env bash
# One server = one channel.  On a fresh Ubuntu 22.04/24.04 server, as root:
#   curl -sSL https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/install.sh | bash -s doughbros
# Channels: bolt | doughbros | hollow | maxcat
set -e
CH=${1:?usage: install.sh CHANNEL}
REPO=elkhabibullaev05-alt/ai-kids-video-agent
DIR=/opt/kanal/repo
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git curl ffmpeg python3 python3-pip xz-utils xvfb libegl1 libgl1 libxi6 libxxf86vm1 libxfixes3 \
  libxrender1 libxkbcommon0 libsm6 libice6 fonts-dejavu-core cron util-linux >/dev/null
pip3 install -q --break-system-packages google-api-python-client google-auth kokoro-onnx soundfile numpy scipy pillow 2>/dev/null \
  || pip3 install -q google-api-python-client google-auth kokoro-onnx soundfile numpy scipy pillow

# code (shallow, main only — the repo is large)
if [ ! -d $DIR/.git ]; then
  mkdir -p /opt/kanal && git clone -q --depth 1 --single-branch https://github.com/$REPO $DIR
fi
# push access: a deploy key that only works for this one repository
KEY=/root/.ssh/kanal_deploy
if [ ! -f $KEY ]; then
  mkdir -p /root/.ssh && ssh-keygen -q -t ed25519 -N "" -C "kanal-$CH@$(hostname)" -f $KEY
fi
ssh-keyscan -q github.com >> /root/.ssh/known_hosts 2>/dev/null || true
git -C $DIR remote set-url origin git@github.com:$REPO.git
git -C $DIR config core.sshCommand "ssh -i $KEY -o IdentitiesOnly=yes"

bash $DIR/bolt/setup.sh            # Blender 4.2.3 + Kokoro voices
mkdir -p /root/kanal/$CH

# every 20 minutes; flock = never two copies at once
LINE="*/20 * * * * cd $DIR && flock -n /tmp/kanal-$CH.lock python3 cloud/worker.py $CH >> /root/kanal/$CH/worker.log 2>&1"
( crontab -l 2>/dev/null | grep -v "cloud/worker.py $CH" ; echo "$LINE" ) | crontab -
systemctl enable --now cron >/dev/null 2>&1 || service cron start || true

echo
echo "================ DONE: $CH ================"
echo "1) GitHub → repo Settings → Deploy keys → Add deploy key, tick 'Allow write access', paste:"
cat $KEY.pub
echo "2) Put the YouTube token here:  /root/kanal/$CH/token.json   (made with cloud/auth.py on your PC)"
echo "3) Test:  cd $DIR && python3 cloud/worker.py $CH   — log: /root/kanal/$CH/worker.log"
