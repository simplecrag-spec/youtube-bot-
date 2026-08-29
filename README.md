# YouTube Auto-Uploader

AI-powered video uploader that downloads videos from any URL, generates SEO-optimized metadata using Google Gemini, and uploads to YouTube automatically.

## 🚀 Deploy Now (Completely Free, No Credit Card!)

### Option 1: Replit (Recommended) ⭐
1. Click: [Import on Replit](https://replit.com/github/simplecrag-spec/youtube-bot-)
2. Add API keys to Secrets (see guide below)
3. Click "Run"
4. **Done!** Share your URL

👉 **[Full Replit Setup Guide →](REPLIT_SETUP.md)**

### Option 2: Deploy to Render (Needs Free Account)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 3: Railway / Fly.io / Others
See [README.md](README.md) for alternative deployment options

---

## ✨ Features

- 🤖 **AI-Powered SEO**: Google Gemini generates optimized titles, descriptions, and tags
- 🌐 **1000+ Sites**: Download from YouTube, TikTok, Instagram, Twitter, Facebook, and more
- ☁️ **Zero-Cost Hosting**: Deploy free on Replit (no credit card ever)
- 📊 **Real-time Progress**: WebSocket-based live updates
- 🎨 **Modern UI**: Sleek dark-mode interface with Tailwind CSS

---

## 🎯 Quick Start

### 1. Get API Keys (All Free)

**Gemini API:**
- Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- Click "Create API Key"
- Copy it

**YouTube API:**
- Go to [console.cloud.google.com](https://console.cloud.google.com)
- Create new project
- Enable "YouTube Data API v3"
- Create OAuth 2.0 credentials (Desktop app)
- Copy Client ID and Client Secret

**YouTube Refresh Token:**
- Run locally: `python setup_youtube_auth.py`
- Follow browser prompt
- Copy the generated token

### 2. Deploy on Replit
- [Import on Replit](https://replit.com/github/simplecrag-spec/youtube-bot-)
- Add secrets (Gemini API, YouTube credentials)
- Click "Run"

### 3. Use It!
- Paste video URL
- Select privacy (Public/Unlisted/Private)
- Click "Process & Upload"
- Share your YouTube link!

---

## 📖 Deployment Guides

| Platform | Cost | Setup Time | No Credit Card |
|----------|------|------------|---|
| **Replit** | FREE | 2 min | ✅ Yes |
| **Render** | FREE | 3 min | ❌ Needs card |
| **Railway** | FREE | 3 min | ❌ Needs card |
| **Fly.io** | FREE | 5 min | ❌ Needs card |
| **Local** | FREE | 5 min | ✅ Yes |

### Detailed Guides:
- 🚀 [**Replit Setup (Easiest)**](REPLIT_SETUP.md)
- 🔧 [Render Deployment](README_RENDER.md)
- 💻 [Local Development](#local-development)

---

## 💻 Local Development

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/simplecrag-spec/youtube-bot-.git
cd youtube-bot-
pip install -r requirements.txt
cp .env.example .env
```

### Setup YouTube Auth
```bash
python setup_youtube_auth.py
```

### Run Locally
```bash
python main.py
```

Visit: http://localhost:8000

---

## 🌐 Supported Video Sites

Thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp), supports 1000+ sites:

- YouTube
- TikTok  
- Instagram
- Twitter/X
- Facebook
- Reddit
- Vimeo
- Dailymotion
- And many more!

---

## 📚 How It Works

1. **Download** - Downloads video from any platform using yt-dlp
2. **Analyze** - Extracts title, description, metadata
3. **Generate SEO** - Uses Google Gemini AI to create:
   - Click-worthy title
   - Keyword-rich description with hashtags
   - 10-15 trending tags
4. **Upload** - Uploads to YouTube with optimized metadata
5. **Return** - Gives you the YouTube link

---

## 🔐 Environment Variables

```
GEMINI_API_KEY              # Google Gemini API key
YOUTUBE_CLIENT_ID           # YouTube OAuth client ID
YOUTUBE_CLIENT_SECRET       # YouTube OAuth client secret
YOUTUBE_REFRESH_TOKEN       # Generated from setup script
DEFAULT_PRIVACY_STATUS      # public/unlisted/private (default: public)
MAX_VIDEO_SIZE_MB          # Max video size in MB (default: 450)
PORT                       # Server port (default: 8000)
```

---

## 📁 Project Structure

```
youtube-bot-/
├── main.py                  # FastAPI application
├── setup_youtube_auth.py    # YouTube OAuth setup
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── .replit                 # Replit config
├── replit.nix              # Replit dependencies
├── render.yaml             # Render deployment config
├── REPLIT_SETUP.md         # Replit guide (START HERE!)
├── README_RENDER.md        # Render guide
└── templates/
    └── index.html          # Web interface
```

---

## 🆘 Troubleshooting

### "YouTube not authenticated"
→ Run `python setup_youtube_auth.py` locally to get refresh token

### "Video too large"
→ Increase `MAX_VIDEO_SIZE_MB` in environment

### "Gemini API not working"
→ Verify `GEMINI_API_KEY` is correct and has quota

### App won't start on Replit
→ Check console for error messages
→ Verify all secrets are set correctly
→ Click "Stop" then "Run" to restart

---

## 🚀 What's Included

✅ Production-ready FastAPI backend  
✅ WebSocket real-time updates  
✅ AI-powered SEO generation  
✅ Support for 1000+ video sites  
✅ One-click Replit deployment  
✅ Modern dark-mode UI  
✅ Health checks & error handling  
✅ Comprehensive logging  

---

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/process` | POST | Start video processing |
| `/status` | GET | Get current status |
| `/health` | GET | Health check |
| `/ws` | WebSocket | Real-time updates |

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [yt-dlp Docs](https://github.com/yt-dlp/yt-dlp)
- [Google Gemini API](https://ai.google.dev/)
- [YouTube Data API](https://developers.google.com/youtube)

---

## 📄 License

MIT License - Free to use and modify!

---

## 🤝 Support

- Check [REPLIT_SETUP.md](REPLIT_SETUP.md) for Replit-specific help
- Check console logs for error messages
- Verify API keys are correct
- Ensure you have sufficient API quota

---

**👉 [Start with Replit Setup Guide](REPLIT_SETUP.md)**

No credit card, no complicated setup. Just deploy and share the link! 🎉

