"""
Ngrok tunnel holatini tekshirish va URL ni ko'rsatish
"""
import requests
import json

def check_ngrok():
    """Ngrok tunnel holatini tekshirish"""
    try:
        # Ngrok API orqali tunnel holatini olish
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get("tunnels", [])
            
            if tunnels:
                print("=" * 60)
                print("NGROK TUNNEL TOPILDI!")
                print("=" * 60)
                for tunnel in tunnels:
                    public_url = tunnel.get("public_url")
                    config = tunnel.get("config", {})
                    addr = config.get("addr", "N/A")
                    
                    print(f"Public URL: {public_url}")
                    print(f"Local Address: {addr}")
                    print(f"Protocol: {tunnel.get('proto', 'N/A')}")
                    print("-" * 60)
                    
                    if public_url:
                        webhook_url = f"{public_url}/webhook"
                        print(f"\nWebhook URL: {webhook_url}")
                        print("\nFacebook Console da quyidagi URL ni ishlating:")
                        print(f"  {webhook_url}")
                        print("\nVerify Token: social_hunter_verify_token")
                        print("=" * 60)
                        return public_url
            else:
                print("WARNING: Ngrok tunnel topilmadi!")
                print("Ngrok ni ishga tushiring: ngrok http 8000")
                return None
        else:
            print(f"ERROR: Ngrok API ga ulanib bo'lmadi (Status: {response.status_code})")
            print("Ngrok ni ishga tushiring: ngrok http 8000")
            return None
    except requests.exceptions.ConnectionError:
        print("=" * 60)
        print("ERROR: Ngrok ishlamayapti!")
        print("=" * 60)
        print("Ngrok ni ishga tushiring:")
        print("  1. Ngrok ni yuklab oling: https://ngrok.com/download")
        print("  2. Terminalda ishga tushiring: ngrok http 8000")
        print("  3. Yoki run.bat ni o'zgartiring va Ngrok ni avtomatik ishga tushiring")
        print("=" * 60)
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    check_ngrok()
