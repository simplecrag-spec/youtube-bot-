# YouTube Auto-Uploader

AI-powered video uploader that downloads videos from any URL, generates SEO-optimized metadata using Google Gemini, and uploads to YouTube automatically.

## Features

- 🤖 **AI-Powered SEO**: Google Gemini generates optimized titles, descriptions, and tags
- 🌐 **1000+ Sites**: Download from YouTube, TikTok, Instagram, Twitter, Facebook, and more
- ☁️ **Zero-Cost Hosting**: Optimized for free-tier platforms (Render, Railway, Fly.io)
- 📊 **Real-time Progress**: WebSocket-based live updates
- 🎨 **Modern UI**: Sleek dark-mode interface with Tailwind CSS

## Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Step 1: Setup API Keys

1. **Gemini API Key** (Required for AI-powered SEO)
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **YouTube API Credentials** (Required for uploading)
   - Visit: https://console.cloud.google.com/apis/credentials
   - Create a new project or select existing
   - Enable "YouTube Data API v3"
   - Create OAuth 2.0 credentials
   - Add `http://localhost:8000/oauth/callback` to redirect URIs
   - Download credentials or copy Client ID and Client Secret

### Step 2: Deploy to Render

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your forked repository
5. Render will auto-detect `render.yaml` configuration
6. Add environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `YOUTUBE_CLIENT_ID`: Your YouTube client ID
   - `YOUTUBE_CLIENT_SECRET`: Your YouTube client secret
7. Click "Create Web Service"
8. Wait 2-3 minutes for deployment

### Step 3: Authorize YouTube

1. Visit your deployed app URL (e.g., `https://your-app.onrender.com`)
2. Run the auth setup locally first:
   ```bash
   python setup_youtube_auth.py
   ```
3. Copy the `YOUTUBE_REFRESH_TOKEN` from output
4. Add it to Render environment variables
5. Restart the service

## Local Development

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/simplecrag-spec/youtube-bot-.git
cd youtube-bot-

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
# (Use nano, vim, or any text editor)
```

### Setup YouTube Authentication

```bash
python setup_youtube_auth.py
```

Follow the prompts to authorize your YouTube account. This will generate a refresh token that you'll add to your `.env` file.

### Run the App

```bash
python main.py
```

Visit: http://localhost:8000

## How to Use

1. Paste any video URL (YouTube, TikTok, Instagram, etc.)
2. Select privacy setting (Public/Unlisted/Private)
3. Click "Process & Upload"
4. Watch real-time progress
5. Get your YouTube video link!

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for SEO generation |
| `YOUTUBE_CLIENT_ID` | Yes | YouTube OAuth client ID |
| `YOUTUBE_CLIENT_SECRET` | Yes | YouTube OAuth client secret |
| `YOUTUBE_REFRESH_TOKEN` | Yes | Generated from setup script |
| `DEFAULT_PRIVACY_STATUS` | No | Default privacy (public/unlisted/private) |
| `MAX_VIDEO_SIZE_MB` | No | Max video size in MB (default: 450) |
| `PORT` | No | Server port (default: 8000) |

## Alternative Deployment Options

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add environment variables in Railway dashboard.

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly secrets set GEMINI_API_KEY=your_key
fly secrets set YOUTUBE_CLIENT_ID=your_id
# ... add other secrets
fly deploy
```

## Supported Video Sites

Thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp), this app supports 1000+ sites including:

- YouTube
- TikTok
- Instagram
- Twitter/X
- Facebook
- Reddit
- Vimeo
- Dailymotion
- And many more!

## API Endpoints

- `GET /` - Main web interface
- `POST /process` - Start video processing
- `GET /status` - Get current processing status
- `GET /health` - Health check
- `WebSocket /ws` - Real-time status updates

## Project Structure

```
youtube-bot-/
├── main.py                 # FastAPI application
├── setup_youtube_auth.py   # YouTube OAuth setup
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── templates/
│   └── index.html         # Web interface
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Troubleshooting

### "YouTube not authenticated" error
- Run `python setup_youtube_auth.py` locally
- Copy the refresh token to your environment variables
- Restart the app

### "Video too large" error
- Increase `MAX_VIDEO_SIZE_MB` environment variable
- Free tiers usually have limited storage

### "Download failed" error
- Check if the video URL is valid
- Some sites may require cookies or authentication
- Private/restricted videos cannot be downloaded

## License

MIT License - feel free to use and modify!

## Credits

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Video downloads: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- AI SEO: [Google Gemini](https://ai.google.dev/)
- YouTube API: [Google APIs](https://developers.google.com/youtube)
