# Deploy to Render - One Click Instructions

## Quick Deployment Steps:

1. **Sign up at https://render.com** (use GitHub login)

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repo:** `simplecrag-spec/youtube-bot-`

4. **Settings:**
   - **Name:** `youtube-auto-uploader` (or any name)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Plan:** Free

5. **Add Environment Variables:**
   ```
   GEMINI_API_KEY = [YOUR_GEMINI_API_KEY]
   YOUTUBE_CLIENT_ID = [YOUR_YOUTUBE_CLIENT_ID]
   YOUTUBE_CLIENT_SECRET = [YOUR_YOUTUBE_CLIENT_SECRET]
   YOUTUBE_REFRESH_TOKEN = [YOUR_YOUTUBE_REFRESH_TOKEN]
   PORT = 8000
   APP_SECRET_KEY = yt-auto-uploader-secret-key-2026-secure-random-string
   ```

6. **Click "Create Web Service"**

7. **Wait 2-3 minutes** for deployment

8. **Your app will be live at:** `https://youtube-auto-uploader.onrender.com`

## Ready to Go URL:
https://render.com/new?template=https://github.com/simplecrag-spec/youtube-bot-
*(This might open the template directly)*

## Alternative: One-Click Deploy Button
```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/simplecrag-spec/youtube-bot-)
```

## Notes:
- The `YOUTUBE_REFRESH_TOKEN` needs to be added AFTER you run `setup_youtube_auth.py`
- Check `SETUP_GUIDE.md` for how to get the refresh token
- Your app will be completely free on Render's free tier

## Success Indicators:
- ✅ Build completes without errors
- ✅ Health check passes
- ✅ You can visit your app URL
- ✅ You see the upload form at your app URL

## Need Help?
- Check Render logs in the dashboard
- Make sure all environment variables are set
- Verify your refresh token is correct
