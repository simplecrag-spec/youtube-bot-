# YouTube Auto-Uploader

A production-ready, zero-cost cloud web application that downloads videos from any link, generates SEO-optimized metadata using AI, and uploads directly to YouTube.

## Features

- **AI-Powered SEO**: Google Gemini generates click-worthy titles, keyword-rich descriptions, and trending tags
- **1000+ Sites Supported**: Powered by yt-dlp (YouTube, TikTok, Instagram, Twitter, Facebook, etc.)
- **Real-Time Progress**: WebSocket-based live status updates
- **Zero-Cost Hosting**: Optimized for free-tier platforms (Render, Railway, Fly.io)
- **Smart Resource Management**: Automatic cleanup of temporary files to prevent disk exhaustion
- **Production Ready**: Full error handling, logging, and health checks

## Quick Start

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` and fill in your credentials:

#### Google Gemini API Key (Required for SEO)
1. Visit https://aistudio.google.com/app/apikey
2. Create an API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

#### YouTube OAuth Credentials (Required for Upload)
1. Go to https://console.cloud.google.com/apis/credentials
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 Client ID** (Desktop application)
5. Add to `.env`:
   ```
   YOUTUBE_CLIENT_ID=your_client_id
   YOUTUBE_CLIENT_SECRET=your_client_secret
   ```

### 3. Generate YouTube Refresh Token

Run the setup script locally:

```bash
python setup_youtube_auth.py
```

This will open a browser for Google authorization. After authorizing, the refresh token will be added to your `.env` file.

### 4. Run Locally

```bash
python main.py
```

Visit http://localhost:8000

## Deployment

### Option 1: Render (Recommended - Easiest)

1. Push code to GitHub
2. Go to https://render.com and create account
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

6. Add environment variables in Render dashboard:
   - `GEMINI_API_KEY`
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
   - `APP_SECRET_KEY` (random string)

7. Deploy!

### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Set variables: `railway variables set GEMINI_API_KEY=your_key`
5. Deploy: `railway up`

### Option 3: Fly.io

1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Login: `fly auth login`
3. Launch: `fly launch`
4. Set secrets:
   ```bash
   fly secrets set GEMINI_API_KEY=your_key
   fly secrets set YOUTUBE_CLIENT_ID=your_id
   fly secrets set YOUTUBE_CLIENT_SECRET=your_secret
   fly secrets set YOUTUBE_REFRESH_TOKEN=your_token
   ```
5. Deploy: `fly deploy`

## Free Tier Limits & Optimization

### Resource Management
- Uses `tempfile` for ephemeral storage
- Automatic cleanup after upload completion
- Maximum video size: 450MB (configurable)
- Timeout: 30 minutes for large files

### Platform Limits
| Platform | RAM | Disk | Bandwidth |
|----------|-----|------|-----------|
| Render   | 512MB | Ephemeral | 100GB/mo |
| Railway  | 512MB | 1GB | 100GB/mo |
| Fly.io   | 256MB | 1GB | 160GB/mo |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web dashboard |
| `/process` | POST | Start video processing |
| `/status` | GET | Current processing status |
| `/ws` | WS | Real-time updates |
| `/health` | GET | Health check |

## Project Structure

```
youtube-auto-uploader/
├── main.py              # FastAPI application
├── setup_youtube_auth.py # OAuth setup helper
├── requirements.txt     # Python dependencies
├── Procfile            # Render deployment
├── Dockerfile          # Container deployment
├── .env.example        # Environment template
├── README.md           # This file
└── templates/
    └── index.html      # Web UI
```

## Troubleshooting

### "YouTube not authenticated"
Run `python setup_youtube_auth.py` to generate a refresh token.

### "Video too large"
Adjust `MAX_VIDEO_SIZE_MB` in `.env` (default: 450MB).

### "Download failed"
- Check if the URL is valid
- Some sites may be geo-restricted
- Try updating yt-dlp: `pip install -U yt-dlp`

### Memory Issues on Free Tier
- Process one video at a time
- Reduce `MAX_VIDEO_SIZE_MB`
- The app automatically cleans up temp files

## Security Notes

- Never commit `.env` to version control
- Keep `YOUTUBE_CLIENT_SECRET` private
- The refresh token provides upload access to your YouTube channel
- Use `APP_SECRET_KEY` for session security in production

## License

MIT License - Use freely for personal and commercial projects.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.