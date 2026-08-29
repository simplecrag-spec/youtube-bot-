"""
YouTube Auto-Uploader - Main Application
A production-ready FastAPI application that downloads videos from links,
generates SEO-optimized metadata using AI, and uploads to YouTube.
"""

import os
import sys
import json
import shutil
import logging
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

import httpx
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request as GoogleRequest

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Global state for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message: {e}")

manager = ConnectionManager()

# Global temp directory for video files
TEMP_DIR = Path(tempfile.gettempdir()) / "youtube_uploader"
TEMP_DIR.mkdir(exist_ok=True)

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
DEFAULT_PRIVACY_STATUS = os.getenv("DEFAULT_PRIVACY_STATUS", "public")
MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", "450"))
PORT = int(os.getenv("PORT", "8000"))

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Video processing state
current_process = {
    "status": "idle",
    "progress": 0,
    "message": "",
    "video_path": None,
    "youtube_url": None
}


class VideoRequest(BaseModel):
    url: str
    privacy: Optional[str] = None


class SEOMetadata(BaseModel):
    title: str
    description: str
    tags: list[str]


def cleanup_temp_files(video_path: Optional[str] = None):
    """Clean up temporary video files to prevent disk space exhaustion."""
    try:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            logger.info(f"Cleaned up video file: {video_path}")

        # Also clean up any yt-dlp temp files
        for f in TEMP_DIR.glob("*.part"):
            try:
                f.unlink()
            except:
                pass
        for f in TEMP_DIR.glob("*.temp"):
            try:
                f.unlink()
            except:
                pass
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


async def log_status(manager: ConnectionManager, status: str, progress: int, message: str):
    """Send status update to all connected clients."""
    current_process["status"] = status
    current_process["progress"] = progress
    current_process["message"] = message

    payload = json.dumps({
        "status": status,
        "progress": progress,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    await manager.send_message(payload)
    logger.info(f"[{status}] {message}")


def generate_seo_metadata(original_title: str, original_description: str = "") -> SEOMetadata:
    """Generate SEO-optimized metadata using Google Gemini AI."""
    if not GEMINI_API_KEY:
        # Fallback to simple SEO if no API key
        return SEOMetadata(
            title=original_title[:100] if original_title else "Video",
            description=original_description or original_title or "Check out this video!",
            tags=["video", "trending", "viral"]
        )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""You are a YouTube SEO expert. Analyze this video and generate optimized metadata:

Original Title: {original_title}
Original Description: {original_description}

Generate the following in JSON format:
1. A click-worthy, SEO-optimized title (under 100 characters)
2. A comprehensive description (200-300 words) with relevant hashtags
3. A comma-separated list of 10-15 high-performing tags

Return ONLY valid JSON like this:
{{
    "title": "your optimized title here",
    "description": "your optimized description with #hashtags",
    "tags": "tag1, tag2, tag3, tag4, tag5"
}}

JSON:"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Parse JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        data = json.loads(text.strip())

        return SEOMetadata(
            title=data.get("title", original_title[:100])[:100],
            description=data.get("description", original_description),
            tags=[t.strip() for t in data.get("tags", "").split(",") if t.strip()]
        )
    except Exception as e:
        logger.error(f"Error generating SEO metadata: {e}")
        # Fallback
        return SEOMetadata(
            title=original_title[:100] if original_title else "Video",
            description=original_description or original_title or "Check out this video!",
            tags=["video", "trending"]
        )


def get_youtube_client():
    """Get authenticated YouTube API client."""
    credentials = None

    # Try to use refresh token
    if YOUTUBE_REFRESH_TOKEN:
        try:
            credentials = Credentials(
                token=None,
                refresh_token=YOUTUBE_REFRESH_TOKEN,
                client_id=YOUTUBE_CLIENT_ID,
                client_secret=YOUTUBE_CLIENT_SECRET,
                token_uri="https://oauth2.googleapis.com/token",
                scopes=SCOPES
            )
            credentials.refresh(GoogleRequest())
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            credentials = None

    if not credentials:
        raise Exception("YouTube not authenticated. Please run the auth setup.")

    return build('youtube', 'v3', credentials=credentials)


def upload_to_youtube(video_path: str, title: str, description: str, tags: list[str], privacy: str) -> str:
    """Upload video to YouTube and return the video URL."""
    youtube = get_youtube_client()

    # Prepare tags as comma-separated string
    tags_str = ",".join(tags[:15])  # YouTube allows max 15 tags

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22',  # People & Blogs
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False,
        }
    }

    # Create media upload
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    # Execute upload
    response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()

    video_id = response['id']
    return f"https://www.youtube.com/watch?v={video_id}"


async def process_video(url: str, privacy: str, background_tasks: BackgroundTasks):
    """Main video processing pipeline."""
    video_path = None

    try:
        # Step 1: Download video
        await log_status(manager, "downloading", 10, "Downloading video from source...")

        # Use yt-dlp to get video info first
        info_cmd = [
            sys.executable, "-m", "yt_dlp",
            "--dump-json",
            "--no-download",
            url
        ]

        try:
            result = subprocess.run(
                info_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            video_info = json.loads(result.stdout)
            original_title = video_info.get("title", "Untitled Video")
            original_description = video_info.get("description", "")
            duration = video_info.get("duration", 0)
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            original_title = "Video"
            original_description = ""
            duration = 0

        # Download the video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_template = str(TEMP_DIR / f"video_{timestamp}.%(ext)s")

        download_cmd = [
            sys.executable, "-m", "yt_dlp",
            "-f", "best[ext=mp4]/best",
            "-o", output_template,
            "--no-playlist",
            url
        ]

        result = subprocess.run(
            download_cmd,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes max
        )

        if result.returncode != 0:
            raise Exception(f"Download failed: {result.stderr}")

        # Find the downloaded file
        downloaded_files = list(TEMP_DIR.glob(f"video_{timestamp}.*"))
        if not downloaded_files:
            raise Exception("Downloaded video file not found")

        video_path = str(downloaded_files[0])

        # Check file size
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        if file_size_mb > MAX_VIDEO_SIZE_MB:
            cleanup_temp_files(video_path)
            raise Exception(f"Video too large: {file_size_mb:.1f}MB (max: {MAX_VIDEO_SIZE_MB}MB)")

        current_process["video_path"] = video_path
        await log_status(manager, "downloaded", 30, f"Downloaded: {original_title}")

        # Step 2: Generate SEO metadata
        await log_status(manager, "generating_seo", 40, "Generating SEO-optimized metadata with AI...")

        seo = generate_seo_metadata(original_title, original_description)

        await log_status(manager, "seo_generated", 60, f"Generated: {seo.title}")

        # Step 3: Upload to YouTube
        await log_status(manager, "uploading", 70, "Uploading to YouTube...")

        youtube_url = upload_to_youtube(
            video_path=video_path,
            title=seo.title,
            description=seo.description,
            tags=seo.tags,
            privacy=privacy
        )

        current_process["youtube_url"] = youtube_url
        await log_status(manager, "completed", 100, f"Upload complete! {youtube_url}")

    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await log_status(manager, "error", 0, f"Error: {str(e)}")

    finally:
        # Always clean up temporary files
        if video_path:
            cleanup_temp_files(video_path)
            current_process["video_path"] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting YouTube Auto-Uploader...")
    logger.info(f"Temporary directory: {TEMP_DIR}")
    yield
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="YouTube Auto-Uploader",
    description="AI-powered video uploader with SEO optimization",
    version="1.0.0",
    lifespan=lifespan
)

# Setup templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main dashboard."""
    config = {
        "has_gemini": bool(GEMINI_API_KEY),
        "has_youtube": bool(YOUTUBE_REFRESH_TOKEN and YOUTUBE_CLIENT_ID),
        "default_privacy": DEFAULT_PRIVACY_STATUS
    }
    return templates.TemplateResponse("index.html", {"request": request, "config": config})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time status updates."""
    await manager.connect(websocket)
    try:
        # Send current status on connect
        if current_process["status"] != "idle":
            await websocket.send_text(json.dumps(current_process))

        while True:
            data = await websocket.receive_text()
            # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.post("/process")
async def process_video_endpoint(request: VideoRequest, background_tasks: BackgroundTasks):
    """Start video processing."""
    if not request.url:
        return JSONResponse({"error": "URL is required"}, status_code=400)

    privacy = request.privacy or DEFAULT_PRIVACY_STATUS

    # Run processing in background
    background_tasks.add_task(process_video, request.url, privacy, background_tasks)

    return JSONResponse({
        "status": "started",
        "message": "Video processing started"
    })


@app.get("/status")
async def get_status():
    """Get current processing status."""
    return JSONResponse(current_process)


@app.post("/auth/setup")
async def setup_youtube_auth():
    """Setup YouTube OAuth authentication."""
    if not YOUTUBE_CLIENT_ID or not YOUTUBE_CLIENT_SECRET:
        return JSONResponse({
            "error": "YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET required"
        }, status_code=400)

    # Create local server for OAuth
    flow = InstalledAppFlow.from_client_secrets_file(
        'youtube_credentials.json' if os.path.exists('youtube_credentials.json') else None,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/oauth/callback"
    )

    # Use client config from env
    client_config = {
        "web": {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "redirect_uris": ["http://localhost:8000/oauth/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    auth_url, _ = flow.authorization_url(prompt='consent')

    return JSONResponse({
        "auth_url": auth_url,
        "message": "Visit the URL to authorize, then provide the authorization code"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Ensure temp directory exists
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return JSONResponse({
        "status": "healthy",
        "temp_dir": str(TEMP_DIR),
        "temp_dir_exists": TEMP_DIR.exists(),
        "has_gemini": bool(GEMINI_API_KEY),
        "has_youtube": bool(YOUTUBE_REFRESH_TOKEN)
    })


@app.get("/oauth/callback")
async def oauth_callback(code: str = None, error: str = None):
    """OAuth callback handler for local development."""
    if error:
        return JSONResponse({"error": error}, status_code=400)
    if not code:
        return JSONResponse({"error": "No authorization code provided"}, status_code=400)
    return JSONResponse({
        "message": "Authorization code received. Run setup script locally to generate refresh token."
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)