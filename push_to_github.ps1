# GitHubga Push Qilish Script
# Bu script GitHub Personal Access Token yordamida push qiladi

Write-Host "GitHubga Push Qilish" -ForegroundColor Green
Write-Host ""

# GitHub Personal Access Token so'raladi
$token = Read-Host "GitHub Personal Access Token ni kiriting (agar yo'q bo'lsa, GITHUB_PUSH.md faylini o'qing)"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "Token kiritilmadi. Push qilish bekor qilindi." -ForegroundColor Red
    Write-Host ""
    Write-Host "Token yaratish uchun:" -ForegroundColor Yellow
    Write-Host "1. GitHub.com -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic)" -ForegroundColor White
    Write-Host "2. Generate new token -> repo scope ni tanlang" -ForegroundColor White
    Write-Host "3. Token yaratib oling va qayta urinib ko'ring" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Remote URL ni o'zgartirish..." -ForegroundColor Yellow
git remote set-url origin "https://$token@github.com/aiziyrak-coder/SotialHunter.git"

Write-Host ""
Write-Host "GitHubga push qilish..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Muvaffaqiyatli push qilindi!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/aiziyrak-coder/SotialHunter" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "Push qilishda xatolik yuz berdi." -ForegroundColor Red
    Write-Host "Token'ni tekshirib, qayta urinib ko'ring." -ForegroundColor Yellow
}
