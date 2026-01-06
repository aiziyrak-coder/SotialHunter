@echo off
echo SOCIAL HUNTER - Ishga tushirish...
echo.

REM Eski jarayonlarni to'xtatish
echo Eski jarayonlarni to'xtatish...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Jarayon to'xtatilmoqda: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Python jarayonlarini to'xtatish (ixtiyoriy)
echo Python jarayonlarini tekshirish...
timeout /t 2 >nul

REM Botni ishga tushirish
echo.
echo Botni ishga tushirish...
python main.py

pause
