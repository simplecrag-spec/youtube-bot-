#!/bin/bash

# Replit Start Script
# This runs when you click the "Run" button

if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run setup first and configure .env with your API keys"
    exit 1
fi

echo "🚀 Starting YouTube Auto-Uploader..."
echo "📱 Your app will be available at: $REPLIT_SERVERS"
echo ""

python main.py
