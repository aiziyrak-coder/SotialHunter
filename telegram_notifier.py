"""
SOCIAL HUNTER - Telegram Group Notification System
"""
import asyncio
from aiogram import Bot
import config

async def send_lead_notification(instagram_username: str, phone_number: str, conversation_summary: str = ""):
    """
    Yangi lid haqida Telegram guruhga xabar yuborish
    
    Args:
        instagram_username: Instagram username
        phone_number: Telefon raqami
        conversation_summary: Suhbat qisqachasi
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    message = f"🔥 **YANGI LID!**\n\n"
    message += f"👤 **Foydalanuvchi:** @{instagram_username}\n"
    message += f"📱 **Telefon:** `{phone_number}`\n"
    
    if conversation_summary:
        summary = conversation_summary[:200] + "..." if len(conversation_summary) > 200 else conversation_summary
        message += f"💬 **Suhbat:** {summary}\n"
    
    try:
        await bot.send_message(
            chat_id=config.TELEGRAM_GROUP_ID,
            text=message,
            parse_mode="Markdown"
        )
        print(f"✅ Telegram guruhga lid yuborildi: @{instagram_username}")
    except Exception as e:
        print(f"❌ Telegram guruhga xabar yuborishda xato: {e}")
    finally:
        await bot.session.close()

def send_lead_notification_sync(instagram_username: str, phone_number: str, conversation_summary: str = ""):
    """Sinxron versiya"""
    asyncio.run(send_lead_notification(instagram_username, phone_number, conversation_summary))
