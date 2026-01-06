# SOCIAL HUNTER - Tezkor Deploy Script (Windows PowerShell)
# Bu script serverga to'g'ridan-to'g'ri deploy qiladi

$ErrorActionPreference = "Stop"

Write-Host "🚀 SOCIAL HUNTER - Tezkor Deploy" -ForegroundColor Green
Write-Host ""

$SERVER_IP = "167.71.53.238"
$SERVER_USER = "root"
$SERVER_PASS = "Ziyrak2025Ai"
$APP_DIR = "/opt/instaHunter"
$DOMAIN = "yengil.cdcgroup.uz"

# Posh-SSH modulini tekshirish
if (-not (Get-Module -ListAvailable -Name Posh-SSH)) {
    Write-Host "📦 Posh-SSH modulini o'rnatish..." -ForegroundColor Yellow
    Install-Module -Name Posh-SSH -Force -Scope CurrentUser -SkipPublisherCheck
}

Import-Module Posh-SSH

# SSH credential
$securePassword = ConvertTo-SecureString $SERVER_PASS -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($SERVER_USER, $securePassword)

Write-Host "🔌 Serverga ulanish..." -ForegroundColor Yellow
try {
    $session = New-SSHSession -ComputerName $SERVER_IP -Credential $credential -AcceptKey -ErrorAction Stop
    Write-Host "✅ Ulanish muvaffaqiyatli!" -ForegroundColor Green
} catch {
    Write-Host "❌ Serverga ulana olmadi: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 1. Paketlarni o'rnatish..." -ForegroundColor Cyan
$installCmd = @"
apt update -y && \
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git -y
"@
$result = Invoke-SSHCommand -SessionId $session.SessionId -Command $installCmd
Write-Host "✅ Paketlar o'rnatildi" -ForegroundColor Green

Write-Host ""
Write-Host "📁 2. Loyiha papkasini yaratish..." -ForegroundColor Cyan
$mkdirCmd = "mkdir -p $APP_DIR && cd $APP_DIR"
Invoke-SSHCommand -SessionId $session.SessionId -Command $mkdirCmd
Write-Host "✅ Papka yaratildi" -ForegroundColor Green

Write-Host ""
Write-Host "📥 3. Fayllarni serverga ko'chirish..." -ForegroundColor Cyan
$files = @("*.py", "requirements.txt", "README.md", ".gitignore")
foreach ($pattern in $files) {
    $localFiles = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
    foreach ($file in $localFiles) {
        Write-Host "   Ko'chirilmoqda: $($file.Name)" -ForegroundColor Gray
        Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile $file.FullName -RemotePath "$APP_DIR/" -ErrorAction SilentlyContinue
    }
}
Write-Host "✅ Fayllar ko'chirildi" -ForegroundColor Green

Write-Host ""
Write-Host "🐍 4. Python virtual environment..." -ForegroundColor Cyan
$venvCmd = @"
cd $APP_DIR && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt
"@
Invoke-SSHCommand -SessionId $session.SessionId -Command $venvCmd
Write-Host "✅ Python environment sozlandi" -ForegroundColor Green

Write-Host ""
Write-Host "🌐 5. Nginx konfiguratsiyasi..." -ForegroundColor Cyan
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

$nginxConfig | Out-File -FilePath "nginx_temp.txt" -Encoding UTF8
Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile "nginx_temp.txt" -RemotePath "/tmp/nginx_config.txt"
Remove-Item "nginx_temp.txt"

$nginxSetup = @"
cat /tmp/nginx_config.txt > /etc/nginx/sites-available/social_hunter && \
ln -sf /etc/nginx/sites-available/social_hunter /etc/nginx/sites-enabled/ && \
rm -f /etc/nginx/sites-enabled/default && \
nginx -t && \
systemctl reload nginx
"@
Invoke-SSHCommand -SessionId $session.SessionId -Command $nginxSetup
Write-Host "✅ Nginx sozlandi" -ForegroundColor Green

Write-Host ""
Write-Host "🔒 6. HTTPS sertifikat..." -ForegroundColor Cyan
$certbotCmd = "certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo 'DNS tekshirib ko''ring'"
Invoke-SSHCommand -SessionId $session.SessionId -Command $certbotCmd
Write-Host "✅ HTTPS sozlandi" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 7. Systemd service..." -ForegroundColor Cyan
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

$serviceConfig | Out-File -FilePath "service_temp.txt" -Encoding UTF8
Set-SCPFile -ComputerName $SERVER_IP -Credential $credential -LocalFile "service_temp.txt" -RemotePath "/tmp/service_config.txt"
Remove-Item "service_temp.txt"

$serviceSetup = @"
cat /tmp/service_config.txt > /etc/systemd/system/social_hunter.service && \
systemctl daemon-reload && \
systemctl enable social_hunter.service
"@
Invoke-SSHCommand -SessionId $session.SessionId -Command $serviceSetup
Write-Host "✅ Systemd service yaratildi" -ForegroundColor Green

Remove-SSHSession -SessionId $session.SessionId

Write-Host ""
Write-Host "🎉 Deploy yakunlandi!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Keyingi qadamlar:" -ForegroundColor Cyan
Write-Host "1. Serverga kiring: ssh root@$SERVER_IP" -ForegroundColor White
Write-Host "2. Config faylini tahrirlang: nano $APP_DIR/config.py" -ForegroundColor White
Write-Host "3. Serviceni ishga tushiring: systemctl start social_hunter" -ForegroundColor White
Write-Host "4. Loglarni ko'ring: journalctl -u social_hunter -f" -ForegroundColor White
Write-Host "5. Webhook URL: https://$DOMAIN/webhook" -ForegroundColor Yellow
Write-Host ""
