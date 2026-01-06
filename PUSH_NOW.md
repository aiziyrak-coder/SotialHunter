# 🚀 GitHubga Push Qilish - Tezkor Qo'llanma

## 1. GitHub Personal Access Token Yaratish

1. **GitHub'ga kiring**: https://github.com
2. **Profil rasmingiz** → **Settings**
3. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. **Note**: `Social Hunter` yozing
6. **Expiration**: `90 days` yoki `No expiration`
7. **Select scopes**: `repo` ni belgilang (barcha repo checkbox'lar avtomatik belgilanadi)
8. **Generate token** ni bosing
9. **Token'ni ko'chirib oling** (keyin ko'rinmaydi!)

## 2. Push Qilish

### Variant A: PowerShell Script (Oson)

```powershell
powershell -ExecutionPolicy Bypass -File push_to_github.ps1
```

Token so'ralganda, yaratgan token'ni kiriting.

### Variant B: Qo'lda Push Qilish

PowerShell'da:

```powershell
# Token'ni o'zgaruvchiga saqlash
$token = "YOUR_TOKEN_HERE"

# Remote URL ni o'zgartirish
git remote set-url origin https://$token@github.com/aiziyrak-coder/SotialHunter.git

# Push qilish
git push -u origin main
```

### Variant C: SSH Key (Uzoq muddatli)

Agar SSH key sozlagan bo'lsangiz:

```powershell
git remote set-url origin git@github.com:aiziyrak-coder/SotialHunter.git
git push -u origin main
```

## 3. Tekshirish

Push qilgandan keyin, brauzerda oching:

**https://github.com/aiziyrak-coder/SotialHunter**

Barcha fayllar ko'rinishi kerak!

## 4. Keyin Serverga Deploy

GitHubga push qilgandan keyin, serverga deploy qilish uchun:

```bash
ssh root@167.71.53.238
cd /opt
git clone https://github.com/aiziyrak-coder/SotialHunter.git instaHunter
cd instaHunter
chmod +x setup_server.sh
./setup_server.sh
```

Yoki `SERVER_DEPLOY.md` faylini o'qing.
