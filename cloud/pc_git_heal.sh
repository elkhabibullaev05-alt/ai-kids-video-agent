#!/usr/bin/env bash
# 2026-11-08: the PC worker stopped pushing status to GitHub on 7 Nov (~09:00 UTC) while still uploading.
# Called by run_all.sh every run: un-stick git (half-done rebase/merge, lock files), keep the HTTPS-read /
# SSH-443-write remotes, push what is waiting, and write a readable report to the owner's Documents folder
# (C:\Users\<user>\Documents\kanal_holat.txt) so Claude can read it through the desktop app. No secrets printed.
cd /opt/kanal/repo || exit 0
# 2026-11-09: a hard power-off left an EMPTY object file in .git ("object file ... is empty", "bad object HEAD"),
# so every channel failed to commit/pull/push and the fixes from GitHub could not arrive. Self-heal: when HEAD is
# unreadable, re-clone from GitHub, keep the broken copy as /opt/kanal/repo.bad_<time> (nothing deleted), and put
# this PC's results + untracked/ignored files back on top.
if ! git rev-parse -q --verify HEAD >/dev/null 2>&1 || git fsck --connectivity-only 2>&1 | grep -q "is empty"; then
  ts=$(date +%Y%m%d%H%M%S); cd /opt/kanal && rm -rf repo.new
  if GIT_TERMINAL_PROMPT=0 timeout 900 git clone -q --depth 50 https://github.com/elkhabibullaev05-alt/ai-kids-video-agent.git repo.new; then
    mv repo "repo.bad_$ts" && mv repo.new repo
    cp -a "repo.bad_$ts/cloud/results/." repo/cloud/results/ 2>/dev/null
    ( cd "repo.bad_$ts" && tar --exclude=./.git -cf - . ) | ( cd repo && tar --skip-old-files -xf - ) 2>/dev/null
    cd repo && git add -A cloud/results && \
      git -c user.name=kanal-worker -c user.email=worker@kanal.local commit -qm "[pc] results after repo re-clone $ts" 2>/dev/null
    echo "repo was corrupt -> re-cloned (old copy: /opt/kanal/repo.bad_$ts)"
  fi
  cd /opt/kanal/repo || exit 0
fi
R=elkhabibullaev05-alt/ai-kids-video-agent
DOC=$(ls -d /mnt/c/Users/*/Documents 2>/dev/null | grep -v -e Public -e Default | head -1)
OUT=${DOC:+$DOC/kanal_holat.txt}
{
echo "=== kanal holati $(date -u +%F' '%H:%M) UTC, host $(hostname) ==="
# 1. stuck states
for d in .git/rebase-merge .git/rebase-apply; do [ -d "$d" ] && { echo "stuck rebase -> abort"; git rebase --abort 2>&1 | tail -2; }; done
[ -f .git/MERGE_HEAD ] && { echo "stuck merge -> abort"; git merge --abort 2>&1 | tail -2; }
find .git -maxdepth 2 -name '*.lock' -mmin +30 -print -delete 2>/dev/null | sed 's/^/old lock removed: /'
# 2. remotes (read over HTTPS, write over SSH port 443; port 22 is blocked on this network)
git remote set-url origin https://github.com/$R.git
git remote set-url --push origin ssh://git@ssh.github.com:443/$R.git
git config core.sshCommand "ssh -i /root/.ssh/kanal_deploy -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20 -o StrictHostKeyChecking=accept-new"
echo "branch: $(git status -sb | head -1)"
echo "local commits not on GitHub: $(git rev-list --count origin/main..HEAD 2>/dev/null)"
# 3. pull + push waiting commits
GIT_TERMINAL_PROMPT=0 timeout 120 git pull -q --rebase --autostash 2>&1 | tail -3 | sed 's/^/pull: /'
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ "$(git rev-list --count HEAD..origin/main 2>/dev/null)" != "0" ]; then
  # pull could not rebase (conflict): take GitHub's tree, then put this PC's newer channel results back on top
  echo "pull conflict -> GitHub tree + this PC's results"
  git rebase --abort 2>/dev/null; rm -rf /tmp/kanal_res; cp -a cloud/results /tmp/kanal_res
  git fetch -q origin && git reset -q --hard origin/main && cp -a /tmp/kanal_res/. cloud/results/ && git add -A cloud/results && \
    git -c user.name=kanal-worker -c user.email=worker@kanal.local commit -qm "[pc] results after git repair" 2>/dev/null
fi
if GIT_TERMINAL_PROMPT=0 timeout 90 git push -q origin HEAD:main 2>/tmp/kp.err; then echo "PUSH: OK"
else echo "PUSH: XATO"; sed 's/^/  /' /tmp/kp.err | head -5
  echo "deploy key exists: $([ -s /root/.ssh/kanal_deploy ] && echo yes || echo NO)"
  echo "public key: $(cat /root/.ssh/kanal_deploy.pub 2>/dev/null)"
  timeout 25 ssh -i /root/.ssh/kanal_deploy -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20 -o StrictHostKeyChecking=accept-new -p 443 -T git@ssh.github.com 2>&1 | head -2 | sed 's/^/  ssh test: /'
fi
echo "disk free: $(df -h / | awk 'NR==2{print $4}')"
for ch in maxcat doughbros hollow bolt roblox funny money ufc sleep; do
  echo "--- $ch: $(python3 -c "import json;d=json.load(open('cloud/results/$ch/status.json'));print(d.get('time'),d.get('stage'),d.get('error','')[:150])" 2>/dev/null)"
  tail -4 /root/kanal/$ch/worker.log 2>/dev/null | cut -c1-220 | sed 's/^/    /'
  [ -f /root/kanal/$ch/maker.log ] && tail -6 /root/kanal/$ch/maker.log | cut -c1-220 | sed 's/^/    maker: /'
done
} > /tmp/kanal_holat.txt 2>&1
[ -n "$OUT" ] && cp -f /tmp/kanal_holat.txt "$OUT"
exit 0
