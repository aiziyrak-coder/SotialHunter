# SOCIAL HUNTER - Windows PowerShell Deploy Script
# Domen: yengil.cdcgroup.uz
# IP: 167.71.53.238

$ErrorActionPreference = "Stop"

Write-Host "🚀 SOCIAL HUNTER - Serverga Deploy qilish..." -ForegroundColor Green
Write-Host "📍 Server: 167.71.53.238" -ForegroundColor Cyan
Write-Host "🌐 Domen: yengil.cdcgroup.uz" -ForegroundColor Cyan
Write-Host ""

# Server ma'lumotlari
$SERVER_IP = "167.71.53.238"
$SERVER_USER = "root"
$SERVER_PASS = "Ziyrak2025Ai"
$APP_DIR = "/opt/instaHunter"
$DOMAIN = "yengil.cdcgroup.uz"

# sshpass o'rniga Posh-SSH ishlatamiz
if (-not (Get-Module -ListAvailable -Name Posh-SSH)) {
    Write-Host "📦 Posh-SSH modulini o'rnatish..." -ForegroundColor Yellow
    Install-Module -Name Posh-SSH -Force -Scope CurrentUser
}

Import-Module Posh-SSH

# SSH credential yaratish
$securePassword = ConvertTo-SecureString $SERVER_PASS -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($SERVER_USER, $securePassword)

Write-Host "📦 1. Serverga ulanish va loyiha papkasini yaratish..." -ForegroundColor Yellow
$session = New-SSHSession -ComputerName $SERVER_IP -Credential $credential -AcceptKey
if (-not $session) {
    Write-Host "❌ Serverga ulana olmadi!" -ForegroundColor Red
    exit 1
}

Invoke-SSHCommand -SessionId $session.SessionId -Command "mkdir -p $APP_DIR"
Write-Host "✅ Papka yaratildi" -ForegroundColor Green
Write-Host ""

Write-Host "📥 2. Fayllarni serverga ko'chirish..." -ForegroundColor Yellow
$filesToCopy = @("*.py", "requirements.txt", "README.md", ".gitignore")
foreach ($file in $filesToCopy) {
    $localFiles = Get-ChildItem -Path $file -ErrorAction SilentlyContinue
    foreach ($localFile in $localFiles) {
        Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile $localFile.FullName -RemotePath "$APP_DIR/"
    }
}
Write-Host "✅ Fayllar ko'chirildi" -ForegroundColor Green
Write-Host ""

Write-Host "🐍 3. Python va kerakli paketlarni o'rnatish..." -ForegroundColor Yellow
$installCommands = @"
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
"@

Invoke-SSHCommand -SessionId $session.SessionId -Command $installCommands
Write-Host "✅ Python va paketlar o'rnatildi" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 4. Nginx konfiguratsiyasini yaratish..." -ForegroundColor Yellow
$nginxConfig = @"
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }
}
"@

$nginxConfig | Out-File -FilePath "nginx_config_temp.txt" -Encoding UTF8
Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile "nginx_config_temp.txt" -RemotePath "/tmp/nginx_config.txt"
Remove-Item "nginx_config_temp.txt"

$nginxSetup = @"
cat /tmp/nginx_config.txt > /etc/nginx/sites-available/social_hunter
ln -sf /etc/nginx/sites-available/social_hunter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
"@

Invoke-SSHCommand -SessionId $session.SessionId -Command $nginxSetup
Write-Host "✅ Nginx sozlandi" -ForegroundColor Green
Write-Host ""

Write-Host "🔒 5. HTTPS sertifikatini olish..." -ForegroundColor Yellow
$certbotCommand = "certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo '⚠️ Certbot xatosi (DNS tekshirib ko''ring)'"
Invoke-SSHCommand -SessionId $session.SessionId -Command $certbotCommand
Write-Host "✅ HTTPS sozlandi" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 6. Systemd service yaratish..." -ForegroundColor Yellow
$serviceConfig = @"
[Unit]
Description=Social Hunter Bot + Webhook Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment=`"PYTHONUNBUFFERED=1`"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

$serviceConfig | Out-File -FilePath "service_config_temp.txt" -Encoding UTF8
Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile "service_config_temp.txt" -RemotePath "/tmp/service_config.txt"
Remove-Item "service_config_temp.txt"

$serviceSetup = @"
cat /tmp/service_config.txt > /etc/systemd/system/social_hunter.service
systemctl daemon-reload
systemctl enable social_hunter.service
"@

Invoke-SSHCommand -SessionId $session.SessionId -Command $serviceSetup
Write-Host "✅ Systemd service yaratildi" -ForegroundColor Green
Write-Host ""

Remove-SSHSession -SessionId $session.SessionId

Write-Host "🎉 Deploy yakunlandi!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Keyingi qadamlar:" -ForegroundColor Cyan
Write-Host "1. Serverga kiring: ssh root@167.71.53.238" -ForegroundColor White
Write-Host "2. Config faylini tahrirlang: nano $APP_DIR/config.py" -ForegroundColor White
Write-Host "3. Serviceni ishga tushiring: systemctl start social_hunter" -ForegroundColor White
Write-Host "4. Loglarni ko'ring: journalctl -u social_hunter -f" -ForegroundColor White
Write-Host "5. Facebook Developer Console'da webhook URL ni yangilang:" -ForegroundColor White
Write-Host "   https://$DOMAIN/webhook" -ForegroundColor Yellow
Write-Host ""
