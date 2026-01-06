#!/bin/bash
# Bu script SERVERDA ishga tushiriladi (serverga kirgandan keyin)

set -e

APP_DIR="/opt/instaHunter"
DOMAIN="yengil.cdcgroup.uz"

echo "🚀 SOCIAL HUNTER - Server sozlash..."
echo ""

# 1. Paketlarni yangilash va o'rnatish
echo "📦 Paketlarni o'rnatish..."
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git

# 2. Python virtual environment
echo "🐍 Python virtual environment yaratish..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Nginx konfiguratsiya
echo "🌐 Nginx sozlash..."
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

# 4. HTTPS sertifikat
echo "🔒 HTTPS sertifikat olish..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo "⚠️ Certbot xatosi"

# 5. Systemd service
echo "🔧 Systemd service yaratish..."
cat > /etc/systemd/system/social_hunter.service << SERVICEEOF
[Unit]
Description=Social Hunter Bot + Webhook Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment="PYTHONUNBUFFERED=1"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable social_hunter.service

echo ""
echo "✅ Server sozlandi!"
echo ""
echo "📝 Keyingi qadamlar:"
echo "1. Config faylini tahrirlang: nano $APP_DIR/config.py"
echo "2. Serviceni ishga tushiring: systemctl start social_hunter"
echo "3. Loglarni ko'ring: journalctl -u social_hunter -f"
echo ""
