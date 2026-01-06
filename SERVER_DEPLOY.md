# 🚀 Serverga Deploy Qilish - To'liq Qo'llanma

## Domen: yengil.cdcgroup.uz
## Server IP: 167.71.53.238
## Parol: Ziyrak2025Ai

---

## 📋 Qadam 1: Serverga Kirish

Windows PowerShell'da:

```powershell
ssh root@167.71.53.238
# Parol: Ziyrak2025Ai
```

Yoki PuTTY ishlatib:

- Host: `167.71.53.238`
- Port: `22`
- Username: `root`
- Password: `Ziyrak2025Ai`

---

## 📦 Qadam 2: Paketlarni O'rnatish

Serverga kirgandan keyin:

```bash
apt update -y
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git
```

---

## 📁 Qadam 3: Loyiha Papkasini Yaratish

```bash
mkdir -p /opt/instaHunter
cd /opt/instaHunter
```

---

## 📥 Qadam 4: Fayllarni Serverga Ko'chirish

### Variant A: GitHubdan Klonlash (Tavsiya etiladi)

Agar GitHubga push qilgan bo'lsangiz:

```bash
cd /opt
git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
cd instaHunter
```

### Variant B: Windows'dan SCP orqali

Windows PowerShell'da (loyiha papkasidan):

```powershell
# Barcha fayllarni ko'chirish
scp -r *.py requirements.txt README.md .gitignore root@167.71.53.238:/opt/instaHunter/
```

Parol so'ralganda: `Ziyrak2025Ai`

---

## 🐍 Qadam 5: Python Virtual Environment

```bash
cd /opt/instaHunter
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Qadam 6: Config Faylini Sozlash

```bash
nano /opt/instaHunter/config.py
```

Yoki `.env` fayl yaratish (tavsiya etiladi):

```bash
cd /opt/instaHunter
nano .env
```

Ichiga quyidagilarni yozing (API kalitlarini o'zgartiring):

```env
TELEGRAM_BOT_TOKEN=8574513735:AAFz2bVwtJE15XRvCO79SwOzBb_yM_i9fhU
TELEGRAM_GROUP_ID=-5195668612
INSTAGRAM_APP_ID=25401954939503877
INSTAGRAM_APP_SECRET=e9627b0fe9506318a9994d8649cb94fe
INSTAGRAM_PAGE_ID=17841478439647668
INSTAGRAM_ACCESS_TOKEN=EAFoZB8YTFBQUBQYqcjlndNc4cbnL1zgpDsAYtEMvc0BRiO5ZBVwCH7pJhBrkY0R0ijHZBfwip48bRZBZBF8R5uEvniwzlFNNSZADJguv86B4ZCnw3PZCN76liNPqTnJNNiEbXSkKMDpiVBIbAtvGfHUv9X6rhQD8rqII5A33nLeVfmIGmxlPQmwAwcpADwxZCEwSu
FACEBOOK_PAGE_ID=922675184265185
INSTAGRAM_USERNAME=aisotuvchiman
INSTAGRAM_PASSWORD=Aa.19980912
INSTAGRAM_VERIFY_TOKEN=social_hunter_verify_token
WEBHOOK_URL=https://yengil.cdcgroup.uz/webhook
GEMINI_API_KEY=AIzaSyBUrNipIDFCnSeZ5nokTqN6o75kDEpklGg
```

Saqlash: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🌐 Qadam 7: Nginx Konfiguratsiyasi

```bash
nano /etc/nginx/sites-available/social_hunter
```

Ichiga quyidagilarni yozing:

```nginx
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
```

Saqlash va faollashtirish:

```bash
ln -sf /etc/nginx/sites-available/social_hunter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

---

## 🔒 Qadam 8: HTTPS Sertifikat (Let's Encrypt)

**MUHIM**: Avval DNS sozlang! `yengil.cdcgroup.uz` → `167.71.53.238` A-record qo'shing.

```bash
certbot --nginx -d yengil.cdcgroup.uz --non-interactive --agree-tos --email admin@yengil.cdcgroup.uz
```

Agar xatolik bo'lsa, DNS tekshirib ko'ring:

```bash
nslookup yengil.cdcgroup.uz
# 167.71.53.238 chiqishi kerak
```

---

## 🔧 Qadam 9: Systemd Service

```bash
nano /etc/systemd/system/social_hunter.service
```

Ichiga quyidagilarni yozing:

```ini
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
```

Saqlash va faollashtirish:

```bash
systemctl daemon-reload
systemctl enable social_hunter.service
systemctl start social_hunter.service
```

---

## ✅ Qadam 10: Tekshirish

### Serviceni tekshirish:

```bash
systemctl status social_hunter
```

### Loglarni ko'rish:

```bash
journalctl -u social_hunter -f
```

### Health check:

Brauzerda oching: `https://yengil.cdcgroup.uz/health`

`{"status":"healthy"}` chiqishi kerak.

---

## 🌐 Qadam 11: Facebook Developer Console'da Webhook Sozlash

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

## 🔧 Muammolarni Hal Qilish

### Serviceni qayta ishga tushirish:

```bash
systemctl restart social_hunter
```

### Loglarni ko'rish:

```bash
journalctl -u social_hunter -f --lines 100
```

### Nginx loglari:

```bash
tail -f /var/log/nginx/error.log
```

### DNS tekshirish:

```bash
nslookup yengil.cdcgroup.uz
```

### Port tekshirish:

```bash
netstat -tulpn | grep 8000
```

---

## 📞 Yordam

Agar muammo bo'lsa, loglarni tekshiring va xatoliklarni yuboring.
