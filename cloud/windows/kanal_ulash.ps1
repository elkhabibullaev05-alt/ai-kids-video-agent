# Bitta kanalni avtomatik yuklashga ulash (bir marta). Ishlatish (PowerShell):
#   irm https://raw.githubusercontent.com/elkhabibullaev05-alt/ai-kids-video-agent/main/cloud/windows/kanal_ulash.ps1 | iex
# Standart: Grind_video. Boshqa kanal uchun avval:  $KANAL="sleep"
if (-not $KANAL) { $KANAL = "grind" }
$R = "elkhabibullaev05-alt/ai-kids-video-agent"
$T = "$env:USERPROFILE\Documents\kanal_tokenlar"
New-Item -ItemType Directory -Force -Path $T | Out-Null
$secret = @("$T\client_secret.json", "$env:USERPROFILE\Documents\maxtube\client_secret.json") + (Get-ChildItem "$env:USERPROFILE\Documents" -Recurse -Depth 2 -Filter "client_secret*.json" -ErrorAction SilentlyContinue | ForEach-Object FullName) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $secret) { Write-Host "client_secret.json topilmadi" -ForegroundColor Red; return }
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/$R/main/cloud/auth.py" -OutFile "$T\auth.py"
python -m pip install -q google-auth-oauthlib google-api-python-client 2>$null
Write-Host "Brauzer ochiladi: kanal $KANAL ni tanlang -> Continue / Allow" -ForegroundColor Yellow
python "$T\auth.py" $secret "$T\token_$KANAL.json"
if (Test-Path "$T\token_$KANAL.json") { Write-Host "Tayyor! $KANAL endi o'zi yuklanadi." -ForegroundColor Green }
