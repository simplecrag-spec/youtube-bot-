"""
YouTube OAuth Setup Script
Run this locally to generate your YouTube refresh token.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def setup_youtube_auth():
    """Setup YouTube OAuth and get refresh token."""

    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET must be set in .env")
        return

    print("Setting up YouTube OAuth...")
    print("A browser window will open for you to authorize the application.")
    print("Please log in with the Google account you want to upload videos to.\n")

    # Create OAuth flow
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_local_server(port=0)

    print("\n" + "="*50)
    print("SUCCESS! Add this to your .env file:\n")
    print(f"YOUTUBE_REFRESH_TOKEN={credentials.refresh_token}")
    print("="*50)

    # Optionally save to .env
    save = input("\nWould you like to automatically add this to .env? (y/n): ")
    if save.lower() == 'y':
        with open('.env', 'a') as f:
            f.write(f"\nYOUTUBE_REFRESH_TOKEN={credentials.refresh_token}\n")
        print("Token saved to .env file!")

if __name__ == "__main__":
    setup_youtube_auth()