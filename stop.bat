@echo off
echo SOCIAL HUNTER - Jarayonlarni to'xtatish...
echo.

REM Port 8000 dagi jarayonlarni topish va to'xtatish
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Jarayon to'xtatilmoqda: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Barcha Python jarayonlarini to'xtatish (ixtiyoriy)
echo.
echo Barcha Python jarayonlarini to'xtatish? (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    taskkill /F /IM python.exe >nul 2>&1
    echo Barcha Python jarayonlar to'xtatildi.
) else (
    echo Faqat port 8000 dagi jarayonlar to'xtatildi.
)

echo.
echo Jarayonlar to'xtatildi!
pause
