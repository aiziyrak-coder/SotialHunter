"""
SOCIAL HUNTER - Configuration Module
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8574513735:AAFz2bVwtJE15XRvCO79SwOzBb_yM_i9fhU")
TELEGRAM_GROUP_ID = int(os.getenv("TELEGRAM_GROUP_ID", "-5195668612"))
TELEGRAM_GROUP_LINK = os.getenv("TELEGRAM_GROUP_LINK", "https://t.me/+ApU_hwOxuVE0OGJi")

# Instagram Graph API Configuration
INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID", "25401954939503877")
INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET", "e9627b0fe9506318a9994d8649cb94fe")
INSTAGRAM_PAGE_ID = os.getenv("INSTAGRAM_PAGE_ID", "17841478439647668")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "EAFoZB8YTFBQUBQYqcjlndNc4cbnL1zgpDsAYtEMvc0BRiO5ZBVwCH7pJhBrkY0R0ijHZBfwip48bRZBZBF8R5uEvniwzlFNNSZADJguv86B4ZCnw3PZCN76liNPqTnJNNiEbXSkKMDpiVBIbAtvGfHUv9X6rhQD8rqII5A33nLeVfmIGmxlPQmwAwcpADwxZCEwSu")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "922675184265185")

# Instagram Login Credentials (Instagram Basic Display API yoki boshqa operatsiyalar uchun)
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "aisotuvchiman")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "Aa.19980912")

# Webhook Configuration
INSTAGRAM_VERIFY_TOKEN = os.getenv("INSTAGRAM_VERIFY_TOKEN", "social_hunter_verify_token")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-domain.com/webhook")

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBUrNipIDFCnSeZ5nokTqN6o75kDEpklGg")

# Database Configuration
# Agar PostgreSQL ulanmagan bo'lsa, SQLite ishlatiladi
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL or DATABASE_URL == "postgresql://user:password@localhost:5432/social_hunter":
    # SQLite fallback (PostgreSQL sozlanmagan bo'lsa)
    import os
    db_path = os.path.join(os.path.dirname(__file__), "social_hunter.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    try:
        print(f"SQLite ishlatilmoqda: {db_path}")
    except:
        pass

# Admin Configuration
ADMIN_USER_IDS = [int(uid) for uid in os.getenv("ADMIN_USER_IDS", "").split(",") if uid.strip()]

# AI System Prompt - Baaztrucks uchun
AI_SYSTEM_PROMPT = """Sening isming Ziyrak AI. Sen Baaztrucks kompaniyasining aqlli sotuvchisisan. Baaztrucks — Farg'onada joylashgan, butun O'zbekiston va qo'shni davlatlar uchun foodtruck (ko'chma furgon-biznes) ishlab chiqaradigan zavod.

KOMPANIYA HAQIDA:
- Foodtrucklar narxi: 3,5 ming dollardan 20 ming dollargacha
- Modellar: T1, T2 va boshqa modellar (2-8 metr uzunlik, 2 metr eni)
- Xizmatlar: Furgon dizayni, ichki reja, jihozlar yetkazib berish va o'rnatish, tayyor biznes paketlari
- Mijozlar: Evos, Perfetto, La Esmeralda, Olot Somsa va boshqa yirik brendlar
- Kafolat: 1 yillik kafolat, servis xizmati
- To'lov: 50% oldindan, 50% furgon tayyor bo'lganda

SENING VAZIFANG:
Foydalanuvchi bilan do'stona muloqot qilish, uning biznes ehtiyojini aniqla (qanday turdagi foodtruck kerak: pitsa, kofe, fast-food, desertlar, telefon aksessuarlari va hokazo). Suhbat orasida unga juda samimiy munosabatda bo'l. Asosiy maqsading — mutaxassisimiz bog'lanishi uchun uning telefon raqamini olish. Raqamni olmaguningcha suhbatni to'xtatma, lekin mijozni bezovta ham qilma.

Til: O'zbek tilida (kirill va lotin) erkin muloqot."""
