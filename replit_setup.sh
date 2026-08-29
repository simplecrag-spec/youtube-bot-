#!/bin/bash

# Replit Setup Script
echo "🚀 Setting up YouTube Auto-Uploader on Replit..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env with your API keys:"
    echo "   1. GEMINI_API_KEY - Get from https://aistudio.google.com/app/apikey"
    echo "   2. YOUTUBE_CLIENT_ID - Get from https://console.cloud.google.com/apis/credentials"
    echo "   3. YOUTUBE_CLIENT_SECRET - Same place as above"
    echo "   4. YOUTUBE_REFRESH_TOKEN - Run: python setup_youtube_auth.py"
fi

echo ""
echo "✅ Setup complete!"
echo "🎯 Next steps:"
echo "   1. Edit .env with your API keys"
echo "   2. Click 'Run' button to start the server"
echo "   3. Open the Replit URL provided"
