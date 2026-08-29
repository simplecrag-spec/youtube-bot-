@echo off
echo ========================================
echo YouTube Auto-Uploader Setup Assistant
echo ========================================
echo.

echo Step 1: Installing dependencies...
echo Please run this command in Command Prompt:
echo.
echo pip install google-auth google-auth-oauthlib python-dotenv fastapi uvicorn yt-dlp
echo.
echo Press any key after installing...
pause > nul

echo.
echo Step 2: Getting YouTube Refresh Token...
echo This will open a browser to authorize the app...
echo Press any key to continue...
pause > nul

python setup_youtube_auth.py

echo.
echo Step 3: Check if .env has your refresh token...
if exist .env (
    echo Opening .env file...
    notepad .env
) else (
    echo .env file not found. Please check setup...
)

echo.
echo Step 4: Git Setup Instructions...
echo.
echo 1. Install Git from: https://git-scm.com/download/win
echo.
echo 2. Open Command Prompt in this folder (D:\free ai)
echo.
echo 3. Run these commands one by one:
echo    git init
echo    git add .
echo    git commit -m "YouTube Auto-Uploader"
echo    git branch -M main
echo    git remote add origin https://github.com/simplecrag-spec/youtube-bot-.git
echo    git push -u origin main
echo.
echo 4. Then go to https://render.com to deploy
echo.
echo Press any key to exit...
pause > nul
