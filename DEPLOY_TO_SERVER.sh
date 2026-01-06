#!/bin/bash
# Bu script SERVERDA ishga tushiriladi
# Serverga kirib, quyidagi buyruqlarni bajaring:

set -e

APP_DIR="/opt/instaHunter"
DOMAIN="yengil.cdcgroup.uz"

echo "SOCIAL HUNTER - Serverga Deploy qilish..."
echo ""

# 1. Paketlarni o'rnatish
echo "1. Paketlarni o'rnatish..."
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git

# 2. Loyiha papkasini yaratish va GitHubdan klonlash
echo ""
echo "2. GitHubdan klonlash..."
mkdir -p /opt
cd /opt
if [ -d "instaHunter" ]; then
    echo "Papka allaqachon mavjud. Yangilash..."
    cd instaHunter
    git pull
else
    git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
    cd instaHunter
fi

# 3. Python virtual environment
echo ""
echo "3. Python virtual environment yaratish..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Nginx konfiguratsiya
echo ""
echo "4. Nginx sozlash..."
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

# 5. HTTPS sertifikat (DNS sozlangan bo'lishi kerak)
echo ""
echo "5. HTTPS sertifikat olish..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo "Certbot xatosi - DNS tekshirib ko'ring"

# 6. Systemd service
echo ""
echo "6. Systemd service yaratish..."
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
echo "Deploy yakunlandi!"
echo ""
echo "Keyingi qadamlar:"
echo "1. Config faylini tahrirlang: nano $APP_DIR/config.py"
echo "2. Serviceni ishga tushiring: systemctl start social_hunter"
echo "3. Statusni tekshiring: systemctl status social_hunter"
echo "4. Loglarni ko'ring: journalctl -u social_hunter -f"
echo "5. Health check: curl https://$DOMAIN/health"
echo ""
