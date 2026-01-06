"""
SOCIAL HUNTER - Asosiy dastur
Bot va Webhook serverni birga ishga tushirish
"""
import asyncio
import threading
from telegram_bot import main as bot_main
from webhook_server import app
import uvicorn

def run_webhook():
    """Webhook serverni alohida thread da ishga tushirish"""
    try:
        print("📡 Webhook server ishga tushmoqda...")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print(f"❌ Webhook server xatosi: {e}")
        import traceback
        traceback.print_exc()

def run_bot():
    """Telegram botni ishga tushirish"""
    asyncio.run(bot_main())

if __name__ == "__main__":
    print("🚀 SOCIAL HUNTER tizimi ishga tushmoqda...")
    print("📡 Webhook server: http://0.0.0.0:8000")
    print("🤖 Telegram bot: ishga tushirilmoqda...")
    
    # Webhook serverni alohida thread da ishga tushirish
    webhook_thread = threading.Thread(target=run_webhook, daemon=True)
    webhook_thread.start()
    
    # Telegram botni asosiy thread da ishga tushirish
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n⏹️ Tizim to'xtatildi.")
