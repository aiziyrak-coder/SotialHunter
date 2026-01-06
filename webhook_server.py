"""
SOCIAL HUNTER - FastAPI Webhook Server for Instagram Events
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import config
from database import SessionLocal, ActivePost, Lead, Conversation
from instagram_api import InstagramAPI
from gemini_ai import ZiyrakAI
from telegram_notifier import send_lead_notification_sync
import asyncio
import json
from datetime import datetime

app = FastAPI()
instagram_api = InstagramAPI()
ziyrak_ai = ZiyrakAI()

# Foydalanuvchilar bilan suhbatlar (memory cache)
user_conversations = {}  # {user_id: {"history": [...], "media_id": "...", "username": "..."}}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification (Meta talab qiladi)
    """
    print("=" * 50)
    print("WEBHOOK VERIFICATION SO'ROVI QABUL QILINDI")
    print("=" * 50)
    
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    print(f"Mode: {mode}")
    print(f"Token: {token}")
    print(f"Expected Token: {config.INSTAGRAM_VERIFY_TOKEN}")
    print(f"Challenge: {challenge}")
    print("=" * 50)
    
    if mode == "subscribe" and token == config.INSTAGRAM_VERIFY_TOKEN:
        print("SUCCESS: Webhook tasdiqlandi!")
        print(f"Challenge qaytarilmoqda: {challenge}")
        return Response(content=challenge, media_type="text/plain")
    else:
        print("ERROR: Webhook tasdiqlanmadi!")
        if mode != "subscribe":
            print(f"  - Mode not 'subscribe': {mode}")
        if token != config.INSTAGRAM_VERIFY_TOKEN:
            print(f"  - Token mismatch!")
            print(f"    Received: {token}")
            print(f"    Expected: {config.INSTAGRAM_VERIFY_TOKEN}")
        raise HTTPException(status_code=403, detail="Forbidden")

@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    Instagram webhook eventlarini qabul qilish
    """
    try:
        # Request headers ni tekshirish
        print("=" * 50)
        print("WEBHOOK REQUEST QABUL QILINDI")
        print("=" * 50)
        print(f"Headers: {dict(request.headers)}")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        print("=" * 50)
        
        # Request ni olish
        raw_body = await request.body()
        print("=" * 50)
        print("WEBHOOK XABARI QABUL QILINDI")
        print("=" * 50)
        print(f"Raw body length: {len(raw_body)} bytes")
        
        # JSON ni parse qilish
        try:
            body = json.loads(raw_body)
        except:
            body = await request.json()
        
        print(f"Body keys: {list(body.keys()) if isinstance(body, dict) else 'Not a dict'}")
        print(f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        print("=" * 50)
        
        # Webhook verification (POST request uchun ham)
        if "hub" in body:
            challenge = body.get("hub", {}).get("challenge")
            if challenge:
                print("Webhook verification challenge qabul qilindi")
                return Response(content=challenge, media_type="text/plain")
        
        # Entry larni qayta ishlash
        entries = body.get("entry", [])
        
        if not entries:
            print("WARNING: Entry topilmadi")
            print("Eslatma: App Development mode da bo'lsa, faqat test webhooks ishlaydi!")
            print("Production webhooks uchun app ni publish qilish kerak.")
            print("")
            print("MUAMMO HAL QILISH:")
            print("1. Facebook Console > Instagram > Webhooks ga kiring")
            print("2. 'comments' field ni tekshiring (Subscribe yoqilgan bo'lishi kerak)")
            print("3. App Mode ni 'Live' ga o'zgartiring (Settings > Basic)")
            print("4. Ngrok URL ni tekshiring va yangilang")
            print("5. Haqiqiy komment yuborib, bot terminalini tekshiring")
            print("")
            print("INFO: Agar haqiqiy kommentlar kelmayapti, quyidagilarni tekshiring:")
            print("- App Mode 'Live' bo'lishi kerak")
            print("- Webhook 'comments' field Subscribe qilingan bo'lishi kerak")
            print("- Ngrok URL Facebook Console da yangilangan bo'lishi kerak")
            print("- Bot akkauntining o'z postiga komment yozilgan bo'lishi kerak")
            return JSONResponse(content={"status": "ok", "message": "No entries"})
        
        print(f"Entrylar soni: {len(entries)}")
        
        for entry in entries:
            print(f"Entry keys: {list(entry.keys())}")
            print(f"Entry: {json.dumps(entry, indent=2, ensure_ascii=False)}")
            
            # Instagram eventlarini qayta ishlash (comments)
            if "changes" in entry:
                changes = entry.get("changes", [])
                print(f"✅ Changes topildi: {len(changes)} ta")
                for change in changes:
                    print(f"Change field: {change.get('field')}")
                    print(f"Change value keys: {list(change.get('value', {}).keys())}")
                    print(f"Change qayta ishlanmoqda: {json.dumps(change, indent=2, ensure_ascii=False)}")
                    await process_instagram_event(change)
            else:
                print("⚠️ WARNING: Entry da 'changes' topilmadi")
                print("Bu degani comments event subscribe qilinmagan yoki event to'g'ri formatda emas!")
                print("")
                print("YECHIM:")
                print("1. Facebook Console > Instagram > Webhooks ga kiring")
                print("2. 'comments' field ni toping")
                print("3. 'Test' tugmasini bosing (Subscribe tugmasi emas!)")
                print("4. Test webhook 'comments' event yuborishi kerak")
                print("")
                print("Eslatma: Hozir kelayotgan eventlar 'messaging' eventlar (message_edit, reaction va hokazo)")
                print("Bizga 'comments' event kerak!")
            
            # Facebook/Instagram Messaging eventlarini qayta ishlash
            if "messaging" in entry:
                messaging_list = entry.get("messaging", [])
                print(f"Messaging topildi: {len(messaging_list)} ta")
                for messaging in messaging_list:
                    if "sender" in messaging:
                        print(f"Messaging qayta ishlanmoqda: {json.dumps(messaging, indent=2, ensure_ascii=False)}")
                        await process_messaging_event(messaging)
            else:
                print("INFO: Entry da 'messaging' topilmadi (bu normal)")
        
        return JSONResponse(content={"status": "ok"})
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON xatosi: {e}")
        return JSONResponse(
            content={"status": "error", "message": "Invalid JSON"},
            status_code=400
        )
    except Exception as e:
        print(f"❌ Webhook xatosi: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

async def process_instagram_event(change: dict):
    """
    Instagram eventlarini qayta ishlash (kommentlar)
    """
    try:
        print("=" * 50)
        print("PROCESS_INSTAGRAM_EVENT CHAQIRILDI")
        print(f"Change: {json.dumps(change, indent=2, ensure_ascii=False)}")
        print("=" * 50)
        
        value = change.get("value", {})
        event_type = change.get("field")
        
        print(f"Event type: {event_type}")
        
        if event_type == "comments":
            # Yangi komment
            comment_id = value.get("id")
            media_id = value.get("media", {}).get("id")
            text = value.get("text", "")
            from_user = value.get("from", {})
            user_id = from_user.get("id")
            username = from_user.get("username", "unknown")
            
            print("=" * 50)
            print("INFO: Yangi komment qabul qilindi!")
            print(f"  - Text: {text}")
            print(f"  - User: @{username} (ID: {user_id})")
            print(f"  - Media ID: {media_id}")
            print(f"  - Comment ID: {comment_id}")
            print("=" * 50)
            
            if not media_id:
                print("WARNING: Media ID topilmadi")
                return
            
            # Post faol ekanligini tekshirish
            db = SessionLocal()
            try:
                # Media ID ni tekshirish - shortcode yoki to'g'ri media_id
                print(f"DEBUG: Media ID tekshirilmoqda: {media_id}")
                
                # Avval to'g'ri media_id bilan tekshirish
                active_post = db.query(ActivePost).filter(
                    ActivePost.media_id == media_id,
                    ActivePost.is_active == True
                ).first()
                
                # Agar topilmasa, shortcode bilan tekshirish (chunki biz shortcode ni saqlaymiz)
                if not active_post:
                    # Instagram Graph API dan kelgan Media ID ni shortcode ga o'girish
                    shortcode = instagram_api.get_shortcode_from_media_id(media_id)
                    if shortcode:
                        # Shortcode bilan tekshirish
                        active_post = db.query(ActivePost).filter(
                            ActivePost.media_id == shortcode,
                            ActivePost.is_active == True
                        ).first()
                        if active_post:
                            print(f"DEBUG: Post topildi shortcode orqali: {shortcode}")
                    
                    # Agar hali topilmasa, barcha faol postlarni ko'rish
                    if not active_post:
                        all_active = db.query(ActivePost).filter(ActivePost.is_active == True).all()
                        print(f"DEBUG: Barcha faol postlar: {[p.media_id for p in all_active]}")
                        
                        # Shortcode ni URL dan olish va solishtirish
                        for post in all_active:
                            # Post URL dan shortcode ni olish
                            import re
                            url_shortcode_match = re.search(r'instagram\.com/p/([A-Za-z0-9_-]+)', post.post_url, re.IGNORECASE)
                            if url_shortcode_match:
                                url_shortcode = url_shortcode_match.group(1)
                                print(f"DEBUG: Post {post.media_id} shortcode: {url_shortcode}")
                                # Agar media_id shortcode ga mos kelsa
                                if str(media_id) == str(url_shortcode) or str(media_id) == str(post.media_id) or (shortcode and str(shortcode) == str(url_shortcode)):
                                    active_post = post
                                    print(f"DEBUG: Post topildi: {post.media_id}")
                                    break
                
                if not active_post:
                    print(f"WARNING: Post faol emas yoki topilmadi. Media ID: {media_id}")
                    print(f"DEBUG: Barcha postlar: {[p.media_id for p in db.query(ActivePost).all()]}")
                    print(f"DEBUG: Barcha postlar URL: {[p.post_url for p in db.query(ActivePost).all()]}")
                    print(f"INFO: Bu test webhook bo'lishi mumkin yoki boshqa odamning posti.")
                    print(f"ESLATMA: Instagram Graph API webhook eventlari faqat bot akkauntining o'z postlariga keladi.")
                    print(f"Boshqa odamning postlariga komment yozilganda webhook event kelmaydi.")
                    print("")
                    print("MUAMMO HAL QILISH:")
                    print("1. Bot akkauntining o'z postini qo'shing (boshqa odamning posti emas!)")
                    print("2. Post URL ni to'g'ri yuboring (masalan: https://www.instagram.com/p/SHORTCODE/)")
                    print("3. Haqiqiy komment yuborib, bot terminalini tekshiring")
                    print("4. Agar Media ID mos kelmasa, shortcode ni tekshiring")
                    print("")
                    print("INFO: Haqiqiy kommentlar uchun Media ID Instagram Graph API dan keladi va shortcode ga o'giriladi.")
                    print("Agar Media ID mos kelmasa, Instagram Graph API dan kelgan Media ID ni tekshiring.")
                    # Test webhook uchun e'tiborsiz qoldiramiz
                    if media_id in ["123123123", "test", "0"]:
                        print("INFO: Test webhook - e'tiborsiz qoldirilmoqda")
                        return
                    # Haqiqiy kommentlar uchun ham e'tiborsiz qoldiramiz (chunki Media ID mos kelmayapti)
                    print("INFO: Haqiqiy komment - Media ID mos kelmayapti, e'tiborsiz qoldirilmoqda")
                    print("YECHIM: Instagram Graph API dan kelgan Media ID ni to'g'ri solishtirish kerak.")
                    return
                
                # Kommentga javob yozish
                comment_reply = "Assalomu alaykum! Baaztrucks foodtrucklar haqida qiziqishingiz uchun rahmat! Batafsil ma'lumotni Directingizga yubordim. 📱"
                instagram_api.reply_to_comment(comment_id, comment_reply)
                
                # Direct xabar yuborish
                first_message = "Assalomu alaykum! 👋\n\nBaaztrucks — professional foodtruck (ko'chma furgon) ishlab chiqaruvchi zavod. Bizning furgonlarimiz haqida qiziqdingizmi?\n\nQanday turdagi biznes uchun foodtruck kerak? (pitsa, kofe, fast-food, desertlar va hokazo)\n\nQanday yordam bera olaman? 😊"
                instagram_api.send_direct_message(user_id, first_message)
                
                # Suhbatni boshlash
                user_conversations[user_id] = {
                    "history": [
                        {"role": "assistant", "content": first_message}
                    ],
                    "media_id": media_id,
                    "username": username
                }
                
                # Suhbatni bazaga yozish
                conversation = Conversation(
                    instagram_user_id=user_id,
                    instagram_username=username,
                    message_text=first_message,
                    is_from_user=False,
                    media_id=media_id
                )
                db.add(conversation)
                db.commit()
                
            finally:
                db.close()
        
    except Exception as e:
        print(f"❌ Event qayta ishlashda xato: {e}")
        import traceback
        traceback.print_exc()

async def process_messaging_event(messaging: dict):
    """
    Direct messaging eventlarini qayta ishlash
    """
    try:
        sender = messaging.get("sender", {})
        recipient = messaging.get("recipient", {})
        
        user_id = sender.get("id")
        
        # Faqat yangi xabarlarni qayta ishlash
        # message_edit, message_reaction va boshqa eventlarni e'tiborsiz qoldirish
        if "message_edit" in messaging:
            print("INFO: message_edit event - e'tiborsiz qoldirilmoqda")
            return
        
        if "message_reaction" in messaging:
            print("INFO: message_reaction event - e'tiborsiz qoldirilmoqda")
            return
        
        message = messaging.get("message", {})
        text = message.get("text", "")
        
        if not text:
            print("INFO: Text topilmadi yoki bo'sh xabar - e'tiborsiz qoldirilmoqda")
            return
        
        print(f"📨 Direct xabar: {text} (User: {user_id})")
        
        # Foydalanuvchi suhbatini olish
        if user_id not in user_conversations:
            # Yangi suhbat
            user_info = instagram_api.get_user_info(user_id)
            username = user_info.get("username", "unknown") if user_info else "unknown"
            
            user_conversations[user_id] = {
                "history": [],
                "media_id": None,
                "username": username
            }
        
        conversation_data = user_conversations[user_id]
        
        # Foydalanuvchi xabarini tarixga qo'shish
        conversation_data["history"].append({"role": "user", "content": text})
        
        # Suhbatni bazaga yozish
        db = SessionLocal()
        try:
            conversation = Conversation(
                instagram_user_id=user_id,
                instagram_username=conversation_data["username"],
                message_text=text,
                is_from_user=True,
                media_id=conversation_data.get("media_id")
            )
            db.add(conversation)
            db.commit()
            
            # Telefon raqamini tekshirish
            phone_number = ziyrak_ai.extract_phone_number(text)
            
            if phone_number:
                # Raqam topildi - Lid yaratish
                print(f"✅ Telefon raqami topildi: {phone_number}")
                
                # Suhbat qisqachasini yaratish
                conversation_summary = " | ".join([
                    msg["content"][:50] for msg in conversation_data["history"][-5:]
                ])
                
                # Lidni bazaga yozish
                lead = Lead(
                    instagram_username=conversation_data["username"],
                    phone_number=phone_number,
                    conversation_summary=conversation_summary,
                    media_id=conversation_data.get("media_id")
                )
                db.add(lead)
                db.commit()
                
                # Telegram guruhga xabar yuborish
                send_lead_notification_sync(
                    conversation_data["username"],
                    phone_number,
                    conversation_summary
                )
                
                # Foydalanuvchiga yakuniy xabar
                final_message = "Rahmat! 🎉\n\nBaaztrucks mutaxassisi tez orada siz bilan bog'lanib, foodtruck haqida batafsil ma'lumot beradi.\n\nBizning furgonlarimiz: Evos, Perfetto, La Esmeralda kabi yirik brendlar tomonidan ishlatilmoqda! 🚚✨"
                instagram_api.send_direct_message(user_id, final_message)
                
                # Suhbatni to'xtatish
                del user_conversations[user_id]
                
                return
            
            # AI javob yaratish
            ai_response = ziyrak_ai.generate_response(
                text,
                conversation_data["history"]
            )
            
            # AI javobini yuborish
            instagram_api.send_direct_message(user_id, ai_response)
            
            # AI javobini tarixga qo'shish
            conversation_data["history"].append({"role": "assistant", "content": ai_response})
            
            # Suhbatni bazaga yozish
            conversation = Conversation(
                instagram_user_id=user_id,
                instagram_username=conversation_data["username"],
                message_text=ai_response,
                is_from_user=False,
                media_id=conversation_data.get("media_id")
            )
            db.add(conversation)
            db.commit()
            
        finally:
            db.close()
        
    except Exception as e:
        print(f"❌ Messaging event qayta ishlashda xato: {e}")

@app.get("/")
async def root():
    """Asosiy sahifa"""
    return {
        "status": "ok",
        "service": "Social Hunter Webhook",
        "version": "1.0.0",
        "webhook_url": "/webhook",
        "verify_token": config.INSTAGRAM_VERIFY_TOKEN
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Webhook server ishga tushmoqda...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
