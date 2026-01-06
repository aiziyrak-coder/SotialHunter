@echo off
echo ========================================
echo NGROK TUNNEL ISHGA TUSHIRILMOQDA...
echo ========================================
echo.

REM Ngrok ni topish
where ngrok >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ngrok topilmadi!
    echo.
    echo Ngrok ni yuklab oling: https://ngrok.com/download
    echo Yoki quyidagi buyruqni ishga tushiring:
    echo   choco install ngrok
    echo   yoki
    echo   scoop install ngrok
    echo.
    pause
    exit /b 1
)

REM Eski Ngrok jarayonlarini to'xtatish
echo Eski Ngrok jarayonlarini to'xtatish...
taskkill /F /IM ngrok.exe >nul 2>&1
timeout /t 2 >nul

REM Ngrok ni ishga tushirish
echo Ngrok tunnel ishga tushirilmoqda...
echo Port: 8000
echo.
start "Ngrok Tunnel" ngrok http 8000

REM Kichik kutish
timeout /t 3 >nul

REM Ngrok URL ni tekshirish
echo.
echo Ngrok URL ni tekshirish...
python check_ngrok.py

echo.
echo ========================================
echo NGROK TUNNEL ISHGA TUSHIRILDI!
echo ========================================
echo.
echo Keyingi qadamlar:
echo 1. Yuqorida ko'rsatilgan Webhook URL ni ko'chirib oling
echo 2. Facebook Console > Instagram > Webhooks ga kiring
echo 3. Callback URL ni yangilang va "Verify and Save" tugmasini bosing
echo 4. "comments" va "messages" fieldlarni Subscribe qiling
echo.
pause
