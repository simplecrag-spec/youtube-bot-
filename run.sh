#!/bin/bash
# YouTube Auto-Uploader - Mac/Linux Starter

echo ""
echo "========================================"
echo "YouTube Auto-Uploader"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python from: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/3] Checking dependencies..."
pip3 show fastapi > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[2/3] Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo "[3/3] Starting server..."
echo ""
echo "========================================"
echo "Server is starting..."
echo "Wait for: 'Application startup complete'"
echo "Then open: http://localhost:8000"
echo "========================================"
echo ""

python3 main.py
