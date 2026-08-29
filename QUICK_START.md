# YouTube Auto-Uploader - Quick Start Guide

## 🚀 Run Locally (Easiest Right Now!)

### Windows:
1. Double-click: **`run.bat`**
2. Wait for message: "Application startup complete"
3. Open browser: **http://localhost:8000**

### Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

---

## 📋 First Time Setup

### 1. Create `.env` file

Copy this and save as `.env` in the project folder:

```
GEMINI_API_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
PORT=8000
```

### 2. Get Gemini API Key (2 minutes)
- Go to: https://aistudio.google.com/app/apikey
- Click "Create API Key"
- Copy the key
- Paste in `.env`

### 3. Get YouTube Credentials (5 minutes)
- Go to: https://console.cloud.google.com
- Create new project (or use existing)
- Search: "YouTube Data API v3"
- Click "Enable"
- Go to "Credentials"
- Click "Create Credentials" → "OAuth 2.0 Client ID"
- Choose "Desktop application"
- Download JSON or copy:
  - Client ID → paste in `.env` as `YOUTUBE_CLIENT_ID`
  - Client Secret → paste in `.env` as `YOUTUBE_CLIENT_SECRET`

### 4. Generate YouTube Refresh Token (3 minutes)
Run in command line:
```bash
python setup_youtube_auth.py
```

A browser will open. Log in with your Google account and authorize.

Copy the generated token and paste in `.env` as `YOUTUBE_REFRESH_TOKEN`

### 5. Run the App
```bash
python main.py
```

Open: http://localhost:8000

---

## 🎯 Use It!

1. Paste any video URL (YouTube, TikTok, Instagram, etc.)
2. Select privacy (Public/Unlisted/Private)
3. Click "Process & Upload"
4. Watch real-time progress
5. Get your YouTube link!

---

## 📤 Share Your Local App

To let others use it while your computer is on:

### Option 1: Share Local Network (Same WiFi)
- Get your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Share: `http://YOUR_IP:8000`
- They can use it if on same WiFi

### Option 2: Use ngrok (Simple Tunneling)
```bash
pip install ngrok
ngrok http 8000
```
Share the ngrok URL with anyone!

### Option 3: Share Files + Instructions
Send them this folder + tell them to run `run.bat` or `run.sh`

---

## ❌ Troubleshooting

### "Python not found"
- Install Python: https://www.python.org/downloads
- Check "Add Python to PATH"
- Restart computer

### "YouTube not authenticated"
- Run: `python setup_youtube_auth.py`
- Follow browser prompts
- Copy token to `.env`

### "Port 8000 already in use"
- Change PORT in `.env` to 8001 or 8002
- Or close other apps using port 8000

### "Gemini API not working"
- Check API key is correct in `.env`
- Check you have API quota

---

## 🎉 Next: Deploy to Cloud (Optional)

Once this works locally, you can deploy to:
- **Replit** (free, no CC) - See REPLIT_SETUP.md
- **Render** (free) - See README.md
- **Others** - Railway, Fly.io, etc.

**For now, just run locally!**
