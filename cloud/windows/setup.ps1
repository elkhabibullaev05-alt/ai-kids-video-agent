# Kanal ishchisi — Windows kompyuterda (WSL Ubuntu ichida), Claude'siz.
# PowerShell'ni ADMINISTRATOR sifatida oching va yozing:
#   irm https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/windows/setup.ps1 | iex
# Qayta ishga tushirish xavfsiz: bajarilgan qadamlar o'tkazib yuboriladi.
$ErrorActionPreference = "Continue"
$R = "elkhabibullaev05-alt/ai-kids-video-agent"
$D = "Ubuntu-24.04"
$T = Join-Path $env:USERPROFILE "Documents\kanal_tokenlar"
function Say($m, $c = "Cyan") { Write-Host "`n>> $m" -ForegroundColor $c }
function HasDistro { ((wsl.exe -l -q 2>$null) -replace "`0", "") | Where-Object { $_.Trim() -eq $D } }

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Say "Administrator oynasi ochilmoqda — chiqqan savolga 'Да / Yes' ni bosing..." Yellow
  Start-Process powershell -Verb RunAs -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-Command',"irm https://raw.githubusercontent.com/$R/main/cloud/windows/setup.ps1 | iex"
  return
}

# 1. WSL + Ubuntu
if (-not (HasDistro)) {
  Say "1/5 Ubuntu (WSL) o'rnatilmoqda..."
  wsl.exe --install -d $D --no-launch
  $u = Get-Command ubuntu2404.exe -ErrorAction SilentlyContinue
  if ($u) { & $u.Source install --root | Out-Null }
  if (-not (HasDistro)) { Say "Kompyuterni qayta yoqing (Restart), keyin shu buyruqni yana bir marta yozing." Yellow; return }
}
Say "1/5 Ubuntu tayyor" Green

# 2. Blender, ovoz, ffmpeg, kod (Ubuntu ichida) — birinchi marta 10-20 daqiqa
Say "2/5 Dasturlar o'rnatilmoqda (birinchi marta 10-20 daqiqa)..."
wsl.exe -d $D -u root -- bash -c "curl -sSL https://raw.githubusercontent.com/$R/main/cloud/install.sh | KANAL_NO_CRON=1 bash -s all"
$key = (wsl.exe -d $D -u root -- cat /root/.ssh/kanal_deploy.pub) -join ""
if (-not $key) { Say "O'rnatish xato bilan tugadi — yuqoridagi xabarni Claude'ga yuboring." Red; return }

# 3. GitHub deploy key (natijalarni repoga yozish uchun)
$ok = wsl.exe -d $D -u root -- bash -c "cd /opt/kanal/repo && GIT_TERMINAL_PROMPT=0 timeout 30 git push --dry-run -q origin HEAD:main >/dev/null 2>&1 && echo OK"
if ($ok -ne "OK") {
  Set-Clipboard -Value $key
  Say "3/5 GitHub sahifasi ochiladi. Title: kanal-pc | Key: Ctrl+V (kalit nusxalandi) | 'Allow write access' ni belgilang | Add key." Yellow
  Start-Process "https://github.com/$R/settings/keys/new"
  Read-Host "Qo'shib bo'lgach Enter bosing"
}
Say "3/5 GitHub tayyor" Green

# 4. YouTube tokenlar (har kanalga bir marta, brauzerda kanalni tanlaysiz)
New-Item -ItemType Directory -Force -Path $T | Out-Null
$max = Join-Path $env:USERPROFILE "Documents\maxtube"
if ((Test-Path "$max\token.json") -and -not (Test-Path "$T\token_maxcat.json")) { Copy-Item "$max\token.json" "$T\token_maxcat.json" }
$secret = @("$T\client_secret.json", "$max\client_secret.json") | Where-Object { Test-Path $_ } | Select-Object -First 1
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/$R/main/cloud/auth.py" -OutFile "$T\auth.py"
python -m pip install -q google-auth-oauthlib google-api-python-client 2>$null
$need = [ordered]@{
  doughbros = "Dough Bros  (akkaunt: habibullaeveldorbek57)";
  hollow    = "Hollowmere Tales  (akkaunt: habibullaeveldorbek57)";
  bolt      = "Inspector Bolt  (akkaunt: halilovelbek558)";
  grind     = "Grind_video  (akkaunt: eldorbekkhabibullaev44)"
}
foreach ($ch in $need.Keys) {
  if (Test-Path "$T\token_$ch.json") { continue }
  Say "4/5 Brauzer ochiladi -> kanal: $($need[$ch]). Shu kanalni tanlang va ruxsat bering." Yellow
  Read-Host "Tayyor bo'lsangiz Enter bosing"
  python "$T\auth.py" $secret "$T\token_$ch.json"
}
Say "4/5 Tokenlar: $((Get-ChildItem $T -Filter 'token_*.json').Name -join ', ')" Green

# 5. Har 20 daqiqada ishga tushadigan Windows vazifasi (oyna ko'rinmaydi)
$act = New-ScheduledTaskAction -Execute "conhost.exe" -Argument "--headless wsl.exe -d $D -u root -- bash /opt/kanal/repo/cloud/run_all.sh"
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 20)
$set = New-ScheduledTaskSettingsSet -MultipleInstances Parallel -ExecutionTimeLimit (New-TimeSpan -Hours 12) -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "KanalWorker" -Action $act -Trigger $trg -Settings $set -Force | Out-Null
Start-ScheduledTask -TaskName "KanalWorker"
Say "5/5 Tayyor! Ishchi har 20 daqiqada o'zi ishlaydi. Kompyuter uyquga ketmasin (Sozlamalar -> Quvvat -> Uyqu: Hech qachon)." Green
Say "Tekshirish:  wsl -d $D -u root -- bash /opt/kanal/repo/cloud/doctor.sh" Green
