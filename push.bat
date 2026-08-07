@echo off
color 0b
echo ========================================
echo       TabStudio Git Auto-Push
echo ========================================
echo.

git add .

set /p "msg=Enter commit message (Press Enter for 'Quick update'): "
if "%msg%"=="" set "msg=Quick update"

git commit -m "%msg%"
git push origin main

echo.
echo ========================================
echo        Successfully Pushed to Vercel!
echo ========================================
pause