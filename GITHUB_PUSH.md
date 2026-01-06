# GitHubga Push Qilish

GitHubga push qilish uchun quyidagi qadamlarni bajaring:

## 1. Personal Access Token Yaratish

1. GitHub'ga kiring: https://github.com
2. O'ng yuqori burchakdagi profil rasmingizga bosing → **Settings**
3. Chap menudan **Developer settings** → **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)** ni bosing
5. **Note**: `Social Hunter Deploy` yozing
6. **Expiration**: `90 days` yoki `No expiration` tanlang
7. **Select scopes**: `repo` ni belgilang (barcha repo checkbox'lar avtomatik belgilanadi)
8. **Generate token** ni bosing
9. **Token'ni ko'chirib oling** (keyin ko'rinmaydi!)

## 2. Push Qilish

PowerShell'da quyidagi buyruqlarni bajaring:

```powershell
# Token'ni o'zgaruvchiga saqlash
$token = "YOUR_TOKEN_HERE"

# Remote URL ni o'zgartirish
git remote set-url origin https://$token@github.com/aiziyrak-coder/SotialHunter.git

# Push qilish
git push -u origin main
```

Yoki bir qatorda:

```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/aiziyrak-coder/SotialHunter.git
git push -u origin main
```

## 3. Keyin Serverga Deploy

GitHubga push qilgandan keyin, serverga deploy qilish uchun `DEPLOY.md` faylini o'qing.
