"""
SOCIAL HUNTER - Gemini AI (Ziyrak AI) Integration
"""
import google.generativeai as genai
import config
import re
from typing import List, Dict, Optional

class ZiyrakAI:
    """Ziyrak AI - Gemini 1.5 Pro orqali muloqot"""
    
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config={
                'temperature': 0.7,  # Har safar biroz turlicha javoblar
                'top_p': 0.8,
                'top_k': 40,
            }
        )
        self.system_prompt = config.AI_SYSTEM_PROMPT
    
    def update_system_prompt(self, new_prompt: str):
        """AI sozlamalarini yangilash"""
        self.system_prompt = new_prompt
    
    def generate_response(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Foydalanuvchi xabariga javob yaratish
        
        Args:
            user_message: Foydalanuvchi xabari
            conversation_history: Oldingi suhbatlar ro'yxati [{"role": "user", "content": "..."}, ...]
        
        Returns:
            AI javobi
        """
        if conversation_history is None:
            conversation_history = []
        
        # Suhbat kontekstini yaratish
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Tarixni qo'shish
        for msg in conversation_history[-10:]:  # Oxirgi 10 ta xabarni olish
            messages.append(msg)
        
        # Hozirgi xabarni qo'shish
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Gemini API chaqiruvi
            response = self.model.generate_content(
                "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini AI xatosi: {e}")
            return "Kechirasiz, texnik muammo yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
    
    def extract_phone_number(self, text: str) -> Optional[str]:
        """
        Matndan telefon raqamini topish
        
        Formats: +998, 998, 9x, 8x, 3x va h.k.
        """
        # O'zbekiston telefon raqamlari uchun regex
        patterns = [
            r'\+998\d{9}',  # +998901234567
            r'998\d{9}',    # 998901234567
            r'9\d{8}',      # 901234567
            r'8\d{8}',      # 801234567
            r'3\d{8}',      # 301234567
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0)
                # Formatni birlashtirish (+998...)
                if not phone.startswith('+998'):
                    if phone.startswith('998'):
                        phone = '+' + phone
                    elif phone.startswith('9'):
                        phone = '+998' + phone
                    elif phone.startswith('8'):
                        phone = '+998' + phone[1:]
                    elif phone.startswith('3'):
                        phone = '+998' + phone
                
                # Raqam uzunligini tekshirish
                if len(phone.replace('+', '')) == 12:
                    return phone
        
        return None
