# 🚀 SOCIAL HUNTER - Deploy Qo'llanmasi

## Domen: yengil.cdcgroup.uz
## Server IP: 167.71.53.238

---

## 📋 1. GitHubga Push Qilish

GitHubga push qilish uchun quyidagilardan birini qiling:

### Variant A: Personal Access Token (Tavsiya etiladi)

1. GitHub'da Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "repo" scope'ni tanlang
3. Token yaratib oling
4. Quyidagi buyruqni ishga tushiring:

```bash
git remote set-url origin https://YOUR_TOKEN@github.com/aiziyrak-coder/SotialHunter.git
git push -u origin main
```

### Variant B: SSH Key

```bash
# SSH key yaratish (agar yo'q bo'lsa)
ssh-keygen -t ed25519 -C "your_email@example.com"

# GitHub'ga SSH key qo'shish
# GitHub → Settings → SSH and GPG keys → New SSH key
# Key'ni ko'chirib qo'shing

# Remote URL ni o'zgartirish
git remote set-url origin git@github.com:aiziyrak-coder/SotialHunter.git
git push -u origin main
```

---

## 📦 2. Serverga Deploy Qilish

### Windows'dan (PowerShell):

```powershell
# 1. Posh-SSH modulini o'rnatish (agar yo'q bo'lsa)
Install-Module -Name Posh-SSH -Force -Scope CurrentUser

# 2. Deploy scriptni ishga tushirish
.\deploy.ps1
```

### Linux/Mac'dan:

```bash
# 1. sshpass o'rnatish (agar yo'q bo'lsa)
# Ubuntu/Debian:
sudo apt install sshpass

# 2. Deploy scriptni ishga tushirish
chmod +x deploy.sh
./deploy.sh
```

### Yoki Serverda To'g'ridan-to'g'ri:

```bash
# 1. Serverga kirish
ssh root@167.71.53.238
# parol: Ziyrak2025Ai

# 2. GitHubdan klonlash
cd /opt
git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
cd instaHunter

# 3. Setup scriptni ishga tushirish
chmod +x setup_server.sh
./setup_server.sh
```

---

## ⚙️ 3. Config Faylini Sozlash

Serverga kirib, config.py faylini tahrirlang:

```bash
ssh root@167.71.53.238
nano /opt/instaHunter/config.py
```

Yoki `.env` fayl yaratish (tavsiya etiladi):

```bash
cd /opt/instaHunter
nano .env
```

Ichiga quyidagilarni yozing:

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

---

## 🚀 4. Serviceni Ishga Tushirish

```bash
# Serviceni ishga tushirish
systemctl start social_hunter

# Statusni tekshirish
systemctl status social_hunter

# Loglarni ko'rish
journalctl -u social_hunter -f
```

---

## 🌐 5. Facebook Developer Console'da Webhook Sozlash

1. Facebook Developer Console'ga kiring
2. App Settings → Webhooks
3. Instagram webhook'ni tanlang
4. Quyidagilarni kiriting:
   - **Callback URL**: `https://yengil.cdcgroup.uz/webhook`
   - **Verify Token**: `social_hunter_verify_token`
   - **Subscription Fields**: `comments`, `messages`
5. "Verify and Save" ni bosing
6. App Mode'ni **Live** ga o'zgartiring

---

## ✅ 6. Tekshirish

1. **Health Check**: `https://yengil.cdcgroup.uz/health` → `{"status":"healthy"}` chiqishi kerak
2. **Webhook Test**: Facebook Developer Console'da "Test" tugmasini bosing
3. **Bot Test**: Telegram botga `/start` yuboring
4. **Instagram Test**: Bot'ga Instagram post linkini yuboring va komment yozing

---

## 🔧 7. Muammolarni Hal Qilish

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
# 167.71.53.238 chiqishi kerak
```

---

## 📞 Yordam

Agar muammo bo'lsa, loglarni tekshiring va xatoliklarni yuboring.
