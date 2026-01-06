"""
SOCIAL HUNTER - Instagram Graph API Integration
"""
import requests
import config
from typing import Optional, Dict, List
import re

class InstagramAPI:
    """Instagram Graph API bilan ishlash"""
    
    BASE_URL = "https://graph.facebook.com/v18.0"
    
    def __init__(self):
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.page_id = config.INSTAGRAM_PAGE_ID
        self.username = config.INSTAGRAM_USERNAME
        self.password = config.INSTAGRAM_PASSWORD
    
    def extract_media_id_from_url(self, post_url: str) -> Optional[str]:
        """
        Instagram post URL dan Media ID ni olish
        
        Formats:
        - https://www.instagram.com/p/ABC123/
        - https://www.instagram.com/reel/ABC123/
        - https://instagram.com/p/ABC123/
        - instagram.com/p/ABC123/
        
        Eslatma: Shortcode dan to'g'ridan-to'g'ri media_id olish qiyin.
        Webhook orqali media_id keladi, lekin bu funksiya shortcode ni saqlaydi.
        """
        if not post_url:
            return None
        
        # URL ni tozalash
        post_url = post_url.strip()
        
        # URL dan shortcode ni olish - turli formatlarni qo'llab-quvvatlash
        patterns = [
            r'instagram\.com/p/([A-Za-z0-9_-]+)',
            r'instagram\.com/reel/([A-Za-z0-9_-]+)',
            r'instagram\.com/tv/([A-Za-z0-9_-]+)',
            r'instagram\.com/stories/[^/]+/([0-9]+)',  # Stories uchun
        ]
        
        shortcode = None
        for pattern in patterns:
            match = re.search(pattern, post_url, re.IGNORECASE)
            if match:
                shortcode = match.group(1)
                # Qo'shimcha tekshirish - shortcode bo'sh bo'lmasligi kerak
                if shortcode and len(shortcode) > 0:
                    break
        
        if not shortcode:
            try:
                print(f"WARNING: Shortcode topilmadi. URL: {post_url}")
            except:
                pass
            return None
        
        try:
            print(f"OK: Shortcode topildi: {shortcode} (URL: {post_url})")
        except:
            pass
        
        # Shortcode ni media_id sifatida saqlaymiz
        # Webhook orqali to'g'ri media_id keladi va yangilanadi
        return shortcode
    
    def get_media_id(self, shortcode: str) -> Optional[str]:
        """Shortcode dan Media ID ga o'tish (webhook orqali keladi)"""
        # Webhook orqali media_id keladi, shuning uchun bu funksiya keyinroq to'ldiriladi
        return shortcode
    
    def get_shortcode_from_media_id(self, media_id: str) -> Optional[str]:
        """
        Instagram Graph API dan kelgan Media ID ni shortcode ga o'girish
        """
        try:
            # Instagram Graph API orqali Media ID dan shortcode olish
            url = f"{self.BASE_URL}/{media_id}"
            params = {
                "access_token": self.access_token,
                "fields": "shortcode"
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                shortcode = data.get("shortcode")
                if shortcode:
                    print(f"DEBUG: Media ID {media_id} -> Shortcode: {shortcode}")
                    return shortcode
            else:
                print(f"WARNING: Media ID dan shortcode olishda xato: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"ERROR: Media ID dan shortcode olishda xato: {e}")
        
        return None
    
    def reply_to_comment(self, comment_id: str, message: str) -> bool:
        """
        Kommentga javob yozish
        """
        url = f"{self.BASE_URL}/{comment_id}/replies"
        params = {
            "access_token": self.access_token,
            "message": message
        }
        
        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                return True
            else:
                print(f"Kommentga javob yozishda xato: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Kommentga javob yozishda xato: {e}")
            return False
    
    def send_direct_message(self, user_id: str, message: str) -> bool:
        """
        Direct xabar yuborish (Instagram Messaging API)
        """
        # Instagram Messaging API uchun to'g'ri format
        url = f"{self.BASE_URL}/{self.page_id}/messages"
        data = {
            "recipient": {"id": user_id},
            "message": {"text": message},
            "messaging_type": "RESPONSE"  # yoki "MESSAGE_TAG" kerak bo'lsa
        }
        params = {
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, json=data, params=params)
            if response.status_code == 200:
                return True
            else:
                print(f"Direct xabar yuborishda xato: {response.status_code} - {response.text}")
                # Alternative: Instagram Direct API
                return self._send_direct_alternative(user_id, message)
        except Exception as e:
            print(f"Direct xabar yuborishda xato: {e}")
            return False
    
    def _send_direct_alternative(self, user_id: str, message: str) -> bool:
        """Alternative usul - Instagram Direct API"""
        # Agar birinchi usul ishlamasa, bu usulni sinab ko'rish
        url = f"{self.BASE_URL}/me/messages"
        data = {
            "recipient": {"id": user_id},
            "message": {"text": message}
        }
        params = {
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, json=data, params=params)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Foydalanuvchi ma'lumotlarini olish"""
        url = f"{self.BASE_URL}/{user_id}"
        params = {
            "access_token": self.access_token,
            "fields": "id,username"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Foydalanuvchi ma'lumotlarini olishda xato: {response.status_code}")
                return None
        except Exception as e:
            print(f"Foydalanuvchi ma'lumotlarini olishda xato: {e}")
            return None
    
    def verify_instagram_credentials(self) -> bool:
        """
        Instagram login ma'lumotlarini tekshirish
        (Instagram Basic Display API yoki boshqa usullar uchun)
        """
        try:
            # Instagram Graph API orqali page ma'lumotlarini olish
            url = f"{self.BASE_URL}/{self.page_id}"
            params = {
                "access_token": self.access_token,
                "fields": "id,name,username"
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                try:
                    print(f"SUCCESS: Instagram ulanishi muvaffaqiyatli!")
                    print(f"Page: {data.get('name', 'N/A')} (@{data.get('username', 'N/A')})")
                except:
                    print("SUCCESS: Instagram ulanishi muvaffaqiyatli!")
                return True
            else:
                try:
                    print(f"WARNING: Instagram ulanishi xatosi: {response.status_code}")
                    print(f"Javob: {response.text}")
                except:
                    print(f"WARNING: Instagram ulanishi xatosi: {response.status_code}")
                return False
        except Exception as e:
            try:
                print(f"ERROR: Instagram ulanishi xatosi: {e}")
            except:
                print(f"ERROR: Instagram ulanishi xatosi")
            return False
    
    def refresh_access_token(self) -> Optional[str]:
        """
        Access token ni yangilash (Long-lived token exchange)
        Login ma'lumotlari kerak bo'lsa, ularni ishlatadi
        """
        try:
            # Long-lived token olish
            url = f"{self.BASE_URL}/oauth/access_token"
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": config.INSTAGRAM_APP_ID,
                "client_secret": config.INSTAGRAM_APP_SECRET,
                "fb_exchange_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                new_token = data.get("access_token")
                if new_token:
                    print("✅ Access token yangilandi!")
                    return new_token
                else:
                    print("⚠️ Yangi token topilmadi")
                    return None
            else:
                print(f"⚠️ Token yangilashda xato: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Token yangilashda xato: {e}")
            return None