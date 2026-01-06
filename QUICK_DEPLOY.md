# 🚀 Tezkor Deploy - Serverga Joylashtirish

## ✅ GitHubga Push Qilindi!

Kodlar GitHub'ga muvaffaqiyatli push qilindi: https://github.com/aiziyrak-coder/SotialHunter

---

## 📋 Serverga Deploy Qilish

### 1. Serverga Kirish

Windows PowerShell'da:

```powershell
ssh root@167.71.53.238
# Parol: Ziyrak2025Ai
```

### 2. Deploy Scriptni Ishga Tushirish

Serverga kirgandan keyin, quyidagi buyruqlarni bajaring:

```bash
# Scriptni yuklab olish
cd /opt
git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
cd instaHunter

# Deploy scriptni ishga tushirish
chmod +x DEPLOY_TO_SERVER.sh
./DEPLOY_TO_SERVER.sh
```

### Yoki Qo'lda (Agar Script Ishlamasa)

```bash
# 1. Paketlarni o'rnatish
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git

# 2. GitHubdan klonlash
cd /opt
git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
cd instaHunter

# 3. Python environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Nginx sozlash
cat > /etc/nginx/sites-available/social_hunter << 'EOF'
server {
    listen 80;
    server_name yengil.cdcgroup.uz;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/social_hunter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# 5. HTTPS sertifikat (DNS sozlangan bo'lishi kerak)
certbot --nginx -d yengil.cdcgroup.uz --non-interactive --agree-tos --email admin@yengil.cdcgroup.uz

# 6. Systemd service
cat > /etc/systemd/system/social_hunter.service << 'EOF'
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
EOF

systemctl daemon-reload
systemctl enable social_hunter.service
```

### 3. Config Faylini Sozlash

```bash
nano /opt/instaHunter/config.py
```

Yoki `.env` fayl yaratish (tavsiya etiladi):

```bash
cd /opt/instaHunter
nano .env
```

Ichiga API kalitlarini yozing (config.py dagi qiymatlar allaqachon bor, lekin tekshirib ko'ring).

### 4. Serviceni Ishga Tushirish

```bash
systemctl start social_hunter
systemctl status social_hunter
```

### 5. Tekshirish

```bash
# Loglarni ko'rish
journalctl -u social_hunter -f

# Health check
curl https://yengil.cdcgroup.uz/health
```

Brauzerda oching: `https://yengil.cdcgroup.uz/health`

`{"status":"healthy"}` chiqishi kerak.

### 6. Facebook Developer Console'da Webhook Sozlash

1. Facebook Developer Console'ga kiring
2. App Settings → Webhooks
3. Instagram webhook'ni tanlang
4. Quyidagilarni kiriting:
   - **Callback URL**: `https://yengil.cdcgroup.uz/webhook`
   - **Verify Token**: `social_hunter_verify_token`
   - **Subscription Fields**: `comments`, `messages`
5. **Verify and Save** ni bosing
6. App Mode'ni **Live** ga o'zgartiring

---

## ⚠️ Muhim Eslatmalar

1. **DNS Sozlash**: `yengil.cdcgroup.uz` → `167.71.53.238` A-record qo'shing
2. **Config Fayl**: Serverda `/opt/instaHunter/config.py` ni tekshirib ko'ring
3. **Firewall**: Port 80 va 443 ochiq bo'lishi kerak

---

## 🔧 Muammolarni Hal Qilish

### Serviceni qayta ishga tushirish:
```bash
systemctl restart social_hunter
```

### Loglarni ko'rish:
```bash
journalctl -u social_hunter -f --lines 100
```

### DNS tekshirish:
```bash
nslookup yengil.cdcgroup.uz
```

---

## ✅ Muvaffaqiyat!

Agar hammasi to'g'ri bo'lsa, bot ishga tushgan bo'lishi kerak!

Telegram botga `/start` yuborib tekshiring.
