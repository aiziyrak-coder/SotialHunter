# 🎯 SOCIAL HUNTER - Liderlarni Avtomatik Qidirish Tizimi

**Baaztrucks** kompaniyasi uchun mo'ljallangan Instagram lead generation tizimi.

Instagramda reklama qilinayotgan postlarga qiziqish bildirgan foydalanuvchilarni aniqlash, ular bilan sun'iy intellekt orqali muloqot qilish va ularni haqiqiy mijozga aylantirish (lead generation) uchun mo'ljallangan.

## 🏢 Kompaniya: Baaztrucks

**Baaztrucks** — Farg'onada joylashgan, butun O'zbekiston va qo'shni davlatlar uchun foodtruck (ko'chma furgon-biznes) ishlab chiqaradigan zavod.

### Mahsulotlar va Xizmatlar:
- 🚚 **Foodtrucklar**: 3,5 ming dollardan 20 ming dollargacha
- 🎨 **Dizayn va rejalashtirish**: Biznes konsepsiyaga mos dizayn
- 🔧 **Jihozlar**: Turkiya va Xitoy uskunalari
- 📦 **Tayyor biznes paketlari**: Menyu, o'qitish, nazorat
- ✅ **1 yillik kafolat** va servis xizmati

### Mijozlar:
Evos, Perfetto, La Esmeralda, Olot Somsa va boshqa yirik brendlar

## 🏗️ Tizim Arxitekturasi

- **Telegram Bot** - Admin boshqaruv paneli
- **Instagram Graph API** - Postlarni kuzatish va xabar almashish
- **Ziyrak AI (Gemini 1.5 Pro)** - Mijoz bilan insondek muloqot qiluvchi AI
- **PostgreSQL** - Lidlar va suhbatlar tarixini saqlash
- **FastAPI Webhook** - Instagram eventlarini qabul qilish

## 📋 Talablar

- Python 3.11+
- PostgreSQL
- Instagram Business Account
- Telegram Bot Token
- Gemini API Key

## 🚀 O'rnatish

### 1. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 2. Ma'lumotlar bazasini yaratish

```bash
python -c "from database import init_db; init_db()"
```

Database avtomatik yaratiladi (SQLite).

### 3. Sozlamalar

Barcha sozlamalar `config.py` faylida. Agar `.env` fayl yaratilsa, u ishlatiladi.

## 🎮 Ishlatish

### Botni ishga tushirish

```bash
python main.py
```

Bu komanda:
- Telegram botni ishga tushiradi
- Webhook serverni 8000-portda ishga tushiradi

### Webhook ni Meta ga ulash

1. Facebook Developer Console ga kiring
2. App Settings > Webhooks bo'limiga o'ting
3. Instagram bo'limida "Subscribe" tugmasini bosing
4. Webhook URL: `https://your-domain.com/webhook`
5. Verify Token: `social_hunter_verify_token`
6. Subscribe to fields: `comments`, `messages`

## 📱 Telegram Bot Buyruqlari

- `/start` - Asosiy menyuni ko'rish
- `🚀 Hunterni ishga tushirish` - Yangi postni kuzatishga qo'shish
- `📊 Faol Postlar` - Hozirda kuzatilayotgan postlarni ko'rish
- `👥 Lidlar Bazasi` - Topilgan lidlar ro'yxati
- `⚙️ AI Sozlamalari` - AI prompt ni o'zgartirish

## 🔄 Ishlash Jarayoni

1. **Admin post linkini yuboradi** → Bot postni kuzatishga qo'shadi
2. **Foydalanuvchi komment yozadi** → Bot kommentga javob yozadi va Directga o'tadi
3. **AI muloqot** → Gemini AI foydalanuvchi bilan suhbatlashadi (Baaztrucks foodtrucklar haqida)
4. **Telefon raqami topiladi** → Lid bazaga yoziladi va Telegram guruhga xabar ketadi
5. **Suhbat yakunlanadi** → Foydalanuvchiga yakuniy xabar yuboriladi

## 🔒 Xavfsizlik

- Instagram 24 soatlik xabar yuborish oynasiga ega
- Bot faqat foydalanuvchi birinchi bo'lib yozganida javob beradi
- AI xabarlari har safar biroz turlicha yoziladi (temperature=0.7)
- Access token ni har 60 kunda yangilash kerak

## 📊 Ma'lumotlar Bazasi

### Jadvalar:

- `active_posts` - Kuzatilayotgan postlar
- `leads` - Topilgan lidlar
- `conversations` - Suhbatlar tarixi
- `ai_settings` - AI sozlamalari

## 🛠️ Texnik Stack

- **Python 3.11**
- **aiogram 3.x** - Telegram bot
- **FastAPI** - Webhook server
- **google-generativeai** - Gemini AI
- **PostgreSQL** - Ma'lumotlar bazasi
- **SQLAlchemy** - ORM

## 📝 Eslatmalar

- Webhook uchun HTTPS va public domain kerak
- Instagram Business Account va Graph API ruxsati kerak
- Access token ni muntazam yangilash kerak
- Spam filtrlardan qochish uchun AI temperature parametri ishlatiladi

## 🐛 Muammolarni hal qilish

### Webhook tasdiqlanmayapti
- Verify token to'g'ri ekanligini tekshiring
- URL HTTPS bo'lishi kerak
- Port 443 yoki 80 bo'lishi kerak

### Bot javob bermayapti
- Access token amal qilish muddati tugagan bo'lishi mumkin
- Instagram 24 soatlik oyna cheklovini tekshiring
- Database ulanishini tekshiring

## 📞 Aloqa

Muammo yoki savol bo'lsa, Telegram guruhga murojaat qiling: https://t.me/+ApU_hwOxuVE0OGJi

## 📄 Litsenziya

Bu loyiha Baaztrucks kompaniyasi uchun maxsus yaratilgan.
