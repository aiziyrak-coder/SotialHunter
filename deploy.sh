#!/bin/bash

# SOCIAL HUNTER - Serverga Deploy Script
# Domen: yengil.cdcgroup.uz
# IP: 167.71.53.238

set -e

echo "🚀 SOCIAL HUNTER - Serverga Deploy qilish..."
echo "📍 Server: 167.71.53.238"
echo "🌐 Domen: yengil.cdcgroup.uz"
echo ""

# Server IP va parol
SERVER_IP="167.71.53.238"
SERVER_USER="root"
SERVER_PASS="Ziyrak2025Ai"
APP_DIR="/opt/instaHunter"
DOMAIN="yengil.cdcgroup.uz"

echo "📦 1. Serverga ulanish va loyiha papkasini yaratish..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
mkdir -p /opt/instaHunter
cd /opt/instaHunter
ENDSSH

echo "✅ Papka yaratildi"
echo ""

echo "📥 2. Fayllarni serverga ko'chirish..."
# Windows'dan Linux serverga fayllarni ko'chirish
sshpass -p "$SERVER_PASS" scp -r -o StrictHostKeyChecking=no \
    *.py \
    requirements.txt \
    README.md \
    .gitignore \
    "$SERVER_USER@$SERVER_IP:$APP_DIR/"

echo "✅ Fayllar ko'chirildi"
echo ""

echo "🐍 3. Python va kerakli paketlarni o'rnatish..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << ENDSSH
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx sshpass

cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python va paketlar o'rnatildi"
ENDSSH

echo ""
echo "⚙️ 4. Config faylini yaratish..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
cd /opt/instaHunter
cat > config.py << 'CONFIGEOF'
# Config fayl - Serverda .env yoki config.py orqali sozlang
# Bu fayl faqat template, haqiqiy qiymatlar .env faylida bo'lishi kerak
CONFIGEOF
echo "✅ Config fayl yaratildi (qiymatlarni keyinroq kiritasiz)"
ENDSSH

echo ""
echo "🌐 5. Nginx konfiguratsiyasini yaratish..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << ENDSSH
cat > /etc/nginx/sites-available/social_hunter << NGINXEOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/social_hunter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "✅ Nginx sozlandi"
ENDSSH

echo ""
echo "🔒 6. HTTPS sertifikatini olish (Let's Encrypt)..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << ENDSSH
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo "⚠️ Certbot xatosi (DNS tekshirib ko'ring)"
echo "✅ HTTPS sozlandi"
ENDSSH

echo ""
echo "🔧 7. Systemd service yaratish..."
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
cat > /etc/systemd/system/social_hunter.service << SERVICEEOF
[Unit]
Description=Social Hunter Bot + Webhook Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/instaHunter
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/instaHunter/venv/bin/python /opt/instaHunter/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable social_hunter.service
echo "✅ Systemd service yaratildi"
ENDSSH

echo ""
echo "📝 8. Config faylini sozlash..."
echo "⚠️  E'tibor: config.py faylida API kalitlarini kiritishingiz kerak!"
echo "   Serverga kirib, /opt/instaHunter/config.py ni tahrirlang"
echo ""

echo "🎉 Deploy yakunlandi!"
echo ""
echo "📋 Keyingi qadamlar:"
echo "1. Serverga kiring: ssh root@167.71.53.238"
echo "2. Config faylini tahrirlang: nano /opt/instaHunter/config.py"
echo "3. Serviceni ishga tushiring: systemctl start social_hunter"
echo "4. Loglarni ko'ring: journalctl -u social_hunter -f"
echo "5. Facebook Developer Console'da webhook URL ni yangilang:"
echo "   https://yengil.cdcgroup.uz/webhook"
echo ""
