"""
SOCIAL HUNTER - Telegram Bot (Admin Panel)
"""
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import config
from database import SessionLocal, ActivePost, Lead, AISettings
from instagram_api import InstagramAPI
from gemini_ai import ZiyrakAI
import re

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
instagram_api = InstagramAPI()
ziyrak_ai = ZiyrakAI()

# Admin tekshirish
def is_admin(user_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return user_id in config.ADMIN_USER_IDS or len(config.ADMIN_USER_IDS) == 0

# FSM States
class PostMonitoring(StatesGroup):
    waiting_for_post_url = State()

class AISettingsState(StatesGroup):
    waiting_for_prompt = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Botni ishga tushirish"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda bu botdan foydalanish huquqi yo'q.")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Hunterni ishga tushirish", callback_data="start_hunter")],
        [InlineKeyboardButton(text="📊 Faol Postlar", callback_data="active_posts")],
        [InlineKeyboardButton(text="👥 Lidlar Bazasi", callback_data="leads_list")],
        [InlineKeyboardButton(text="⚙️ AI Sozlamalari", callback_data="ai_settings")]
    ])
    
    await message.answer(
        "🤖 **SOCIAL HUNTER** - Admin Panel\n\n"
        "Quyidagi funksiyalardan birini tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "start_hunter")
async def start_hunter(callback: CallbackQuery, state: FSMContext):
    """Hunter ishga tushirish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return
    
    await callback.message.answer(
        "📎 Instagram post linkini yuboring:\n\n"
        "Masalan: https://www.instagram.com/p/ABC123/"
    )
    await state.set_state(PostMonitoring.waiting_for_post_url)
    await callback.answer()

@dp.message(PostMonitoring.waiting_for_post_url)
async def process_post_url(message: Message, state: FSMContext):
    """Post URL ni qayta ishlash"""
    post_url = message.text.strip()
    
    # URL ni tekshirish
    if "instagram.com" not in post_url.lower():
        await message.answer(
            "❌ Noto'g'ri Instagram link. Iltimos, to'g'ri link yuboring.\n\n"
            "Masalan:\n"
            "• https://www.instagram.com/p/ABC123/\n"
            "• https://instagram.com/reel/ABC123/"
        )
        return
    
    # Media ID ni olish
    try:
        print(f"DEBUG: Post URL qabul qilindi: {post_url}")
        media_id = instagram_api.extract_media_id_from_url(post_url)
        print(f"DEBUG: Extracted media_id: {media_id}")
        
        if not media_id:
            # Qo'shimcha tekshirish - boshqa formatlar
            print(f"DEBUG: Media ID topilmadi, qo'shimcha tekshirish...")
            await message.answer(
                "❌ Post ID ni aniqlab bo'lmadi.\n\n"
                f"Yuborilgan link: `{post_url[:100]}`\n\n"
                "Iltimos, quyidagi formatlardan birini ishlating:\n"
                "• https://www.instagram.com/p/SHORTCODE/\n"
                "• https://instagram.com/p/SHORTCODE/\n"
                "• https://www.instagram.com/reel/SHORTCODE/\n\n"
                "Eslatma: Linkda 'p/' yoki 'reel/' bo'lishi kerak.",
                parse_mode="Markdown"
            )
            await state.clear()
            return
    except Exception as e:
        import traceback
        print(f"ERROR: Post ID aniqlashda xato: {e}")
        traceback.print_exc()
        await message.answer(
            f"❌ Post IDni aniqlashda xatolik yuz berdi.\n"
            f"Xato: {str(e)}\n\n"
            f"Linkni tekshirib, qayta yuboring.\n\n"
            f"Yuborilgan link: {post_url[:100]}"
        )
        await state.clear()
        return
    
    # Bazaga qo'shish
    db = SessionLocal()
    try:
        # Oldingi postni tekshirish
        existing = db.query(ActivePost).filter(ActivePost.media_id == media_id).first()
        if existing:
            existing.is_active = True
        else:
            active_post = ActivePost(media_id=media_id, post_url=post_url)
            db.add(active_post)
        db.commit()
        
        await message.answer(
            f"✅ **Hunter ishga tushirildi!**\n\n"
            f"📎 Post: {post_url}\n"
            f"🆔 Media ID: `{media_id}`\n\n"
            f"Endi bu postga yozilgan kommentlar avtomatik kuzatiladi.\n\n"
            f"⚠️ **MUHIM ESLATMA:**\n"
            f"Instagram Graph API webhook eventlari faqat bot akkauntining o'z postlariga keladi.\n"
            f"Agar bu boshqa odamning posti bo'lsa, webhook eventlar kelmaydi.\n\n"
            f"**Yechim:**\n"
            f"1. Bot akkaunti o'sha postga komment yozishi kerak\n"
            f"2. Yoki bot akkaunti o'sha postni o'z akkauntiga repost qilishi kerak\n"
            f"3. Shundan keyin webhook eventlar keladi",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"❌ Xato: {e}")
    finally:
        db.close()
        await state.clear()

@dp.callback_query(F.data == "active_posts")
async def show_active_posts(callback: CallbackQuery):
    """Faol postlarni ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        active_posts = db.query(ActivePost).filter(ActivePost.is_active == True).all()
        
        if not active_posts:
            await callback.message.answer("📊 Hozirda faol postlar yo'q.")
            await callback.answer()
            return
        
        text = "📊 **Faol Postlar:**\n\n"
        keyboard_buttons = []
        
        for post in active_posts:
            text += f"🆔 ID: `{post.media_id}`\n"
            text += f"🔗 Link: {post.post_url}\n"
            text += f"📅 {post.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
            
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=f"⏹️ To'xtatish: {post.media_id[:10]}...",
                    callback_data=f"stop_post_{post.id}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    finally:
        db.close()
    
    await callback.answer()

@dp.callback_query(F.data.startswith("stop_post_"))
async def stop_post(callback: CallbackQuery):
    """Postni to'xtatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return
    
    post_id = int(callback.data.split("_")[-1])
    db = SessionLocal()
    try:
        post = db.query(ActivePost).filter(ActivePost.id == post_id).first()
        if post:
            post.is_active = False
            db.commit()
            await callback.message.answer(f"✅ Post to'xtatildi: {post.media_id}")
        else:
            await callback.message.answer("❌ Post topilmadi.")
    finally:
        db.close()
    
    await callback.answer()

@dp.callback_query(F.data == "leads_list")
async def show_leads(callback: CallbackQuery):
    """Lidlar ro'yxatini ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        leads = db.query(Lead).order_by(Lead.created_at.desc()).limit(50).all()
        
        if not leads:
            await callback.message.answer("👥 Hozirda lidlar yo'q.")
            await callback.answer()
            return
        
        text = f"👥 **Lidlar Bazasi** (Jami: {len(leads)})\n\n"
        
        for lead in leads[:20]:  # Birinchi 20 tasini ko'rsatish
            text += f"👤 @{lead.instagram_username}\n"
            text += f"📱 {lead.phone_number}\n"
            if lead.conversation_summary:
                summary = lead.conversation_summary[:50] + "..." if len(lead.conversation_summary) > 50 else lead.conversation_summary
                text += f"💬 {summary}\n"
            text += f"📅 {lead.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if len(leads) > 20:
            text += f"\n... va yana {len(leads) - 20} ta lid"
        
        await callback.message.answer(text, parse_mode="Markdown")
    finally:
        db.close()
    
    await callback.answer()

@dp.callback_query(F.data == "ai_settings")
async def show_ai_settings(callback: CallbackQuery, state: FSMContext):
    """AI sozlamalarini ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return
    
    db = SessionLocal()
    try:
        ai_settings = db.query(AISettings).first()
        if ai_settings:
            current_prompt = ai_settings.system_prompt
            await callback.message.answer(
                f"⚙️ **Hozirgi AI Sozlamalari:**\n\n"
                f"`{current_prompt[:200]}...`\n\n"
                f"Yangi prompt yuboring yoki /cancel buyrug'i bilan bekor qiling.",
                parse_mode="Markdown"
            )
            await state.set_state(AISettingsState.waiting_for_prompt)
        else:
            await callback.message.answer("❌ AI sozlamalari topilmadi.")
    finally:
        db.close()
    
    await callback.answer()

@dp.message(AISettingsState.waiting_for_prompt)
async def update_ai_prompt(message: Message, state: FSMContext):
    """AI prompt ni yangilash"""
    new_prompt = message.text.strip()
    
    db = SessionLocal()
    try:
        ai_settings = db.query(AISettings).first()
        if ai_settings:
            ai_settings.system_prompt = new_prompt
            ziyrak_ai.update_system_prompt(new_prompt)
            db.commit()
            await message.answer("✅ AI sozlamalari yangilandi!")
        else:
            from database import AISettings
            ai_settings = AISettings(system_prompt=new_prompt)
            db.add(ai_settings)
            db.commit()
            ziyrak_ai.update_system_prompt(new_prompt)
            await message.answer("✅ AI sozlamalari yaratildi!")
    except Exception as e:
        await message.answer(f"❌ Xato: {e}")
    finally:
        db.close()
        await state.clear()

@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Jarayonni bekor qilish"""
    await state.clear()
    await message.answer("❌ Jarayon bekor qilindi.")

async def main():
    """Botni ishga tushirish"""
    print("🤖 Telegram Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
