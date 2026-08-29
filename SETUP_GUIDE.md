# YouTube Auto-Uploader - Setup Guide

## Step 1: Get Your YouTube Refresh Token

1. Install dependencies:
   ```
   pip install google-auth google-auth-oauthlib python-dotenv
   ```

2. Run the auth setup:
   ```
   python setup_youtube_auth.py
   ```

3. A browser will open - sign in with your YouTube account and authorize the app

4. The script will show you a refresh token. When asked "Would you like to automatically add this to .env?", type `y` and press Enter.

## Step 2: Push to GitHub

1. **Install Git** if you haven't: https://git-scm.com/download/win

2. Open a terminal in `D:\free ai` and run:
   ```
   git init
   git add .
   git commit -m "Initial commit: YouTube Auto-Uploader"
   git branch -M main
   git remote add origin https://github.com/simplecrag-spec/youtube-bot-.git
   git push -u origin main
   ```

## Step 3: Deploy to Render

1. Go to https://render.com and sign in (or create account)

2. Click **"New +"** → **"Web Service"**

3. Connect your GitHub repo: `simplecrag-spec/youtube-bot-`

4. Settings:
   - **Name**: youtube-auto-uploader (or any name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

5. **Add Environment Variables** (click "Add Environment Variable"):
   - `GEMINI_API_KEY` = `[YOUR_GEMINI_API_KEY]`
   - `YOUTUBE_CLIENT_ID` = `[YOUR_YOUTUBE_CLIENT_ID]`
   - `YOUTUBE_CLIENT_SECRET` = `[YOUR_YOUTUBE_CLIENT_SECRET]`
   - `YOUTUBE_REFRESH_TOKEN` = (the token you got from Step 1)
   - `PORT` = `8000`
   - `APP_SECRET_KEY` = `yt-auto-uploader-secret-key-2026-secure-random-string`

6. Click **"Create Web Service"**

7. Wait for deployment (takes 2-3 minutes)

8. Your app will be live at: `https://youtube-auto-uploader.onrender.com` (or whatever name you chose)

## ✅ You're Done!

Visit your Render URL and start uploading videos to YouTube automatically!

---

**Need help?** Check the README.md for more details.
