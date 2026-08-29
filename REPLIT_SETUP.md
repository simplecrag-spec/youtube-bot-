# 🚀 Replit Deployment Guide

## Quick Start (2 Minutes)

### Step 1: Create Replit Account
1. Go to [replit.com](https://replit.com)
2. Sign up with GitHub or email (FREE, no credit card)
3. Click **"Create Repl"**

### Step 2: Import Your Project
Choose ONE method:

**Method A: Import from GitHub (Easiest)**
1. In Replit, click **"Import from GitHub"**
2. Paste: `https://github.com/simplecrag-spec/youtube-bot-`
3. Click Import
4. Wait 1-2 minutes for setup

**Method B: Upload Files
1. Create new Python Repl
2. Upload all files from your project
3. Make sure `requirements.txt` is included

### Step 3: Configure API Keys
1. Click the **"Secrets"** button (lock icon) on left sidebar
2. Add these environment variables:

```
GEMINI_API_KEY = your_key_here
YOUTUBE_CLIENT_ID = your_client_id_here
YOUTUBE_CLIENT_SECRET = your_client_secret_here
YOUTUBE_REFRESH_TOKEN = your_refresh_token_here
```

### Step 4: Run!
1. Click the **"Run"** button
2. Wait for `Application startup complete` message
3. Click the generated URL to open your app
4. Share that URL with anyone!

---

## 🔑 Getting API Keys (5 Minutes)

### Gemini API Key (Free, unlimited)
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the key
4. Add to Replit Secrets as `GEMINI_API_KEY`

### YouTube API Credentials
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or select existing)
3. Search for **"YouTube Data API v3"** and enable it
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Choose **Desktop application**
6. Download the JSON file or copy:
   - `client_id` → Add to Replit as `YOUTUBE_CLIENT_ID`
   - `client_secret` → Add to Replit as `YOUTUBE_CLIENT_SECRET`

### YouTube Refresh Token
1. **Run this locally on your computer:**
   ```bash
   git clone https://github.com/simplecrag-spec/youtube-bot-.git
   cd youtube-bot-
   pip install -r requirements.txt
   
   # Create .env locally
   echo "YOUTUBE_CLIENT_ID=your_id_here" > .env
   echo "YOUTUBE_CLIENT_SECRET=your_secret_here" >> .env
   echo "GEMINI_API_KEY=your_key_here" >> .env
   
   # Generate refresh token
   python setup_youtube_auth.py
   ```

2. A browser window will open to authorize YouTube
3. Copy the generated `YOUTUBE_REFRESH_TOKEN`
4. Add it to Replit Secrets

---

## ✅ How to Use Once Running

1. **Open your Replit app URL** (something like: `https://youtube-bot-*.replit.dev`)
2. **Paste any video URL** (YouTube, TikTok, Instagram, etc.)
3. **Select privacy** (Public/Unlisted/Private)
4. **Click "Process & Upload"**
5. **Watch real-time progress**
6. **Get your YouTube link!**

---

## 📊 Replit Free Tier Limits

- ✅ **Always free** (no credit card ever)
- ⏱️ **Runtime:** 1 hour per day (restarts automatically)
- 💾 **Storage:** 500MB
- 🌐 **Bandwidth:** Limited but sufficient
- 🔄 **Deployment:** Automatic

**For 24/7 uptime:** Upgrade to Replit Pro ($7/month optional)

---

## ⚠️ Known Limitations

1. **Free tier sleeps after inactivity** - You need to visit the URL to wake it up
2. **Can't process very large videos** - Limited to ~450MB
3. **Only 1 hour daily runtime** - Restarts each day
4. **Limited to light usage** - For personal use, not high-traffic

---

## 🆘 Troubleshooting

### "YouTube not authenticated" Error
→ Make sure `YOUTUBE_REFRESH_TOKEN` is set in Secrets

### "Gemini API not working" Error
→ Check `GEMINI_API_KEY` in Secrets is correct

### App won't start
→ Click "Stop" then "Run" again
→ Check the console for error messages

### Need more runtime?
→ Upgrade to Replit Pro ($7/month)
→ Or use multiple Repl instances

---

## 🎯 Next Steps

1. ✅ Create Replit account (free)
2. ✅ Import this project
3. ✅ Get API keys (all free)
4. ✅ Add Secrets in Replit
5. ✅ Click Run
6. ✅ Share the URL!

**That's it! You now have a working YouTube uploader!** 🎉

Need help? Check the console output for error messages.

---

## 📝 Alternative: Keep Using GitHub Pages + Local Server

If you want the UI on GitHub Pages but server running locally:
- Keep your HTML on GitHub Pages
- Run `python main.py` on your computer
- Share the localhost URL (only works while your computer is on)
- Better: Use Replit instead!
