#!/bin/bash

echo "🔧 Setting up environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "🧠 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt || {
    echo "⚠️ Couldn't install from requirements.txt. Installing manually..."
    pip install ffmpeg-python pytube openai-whisper torch rich beautifulsoup4 requests
}

# Run the script
echo "🚀 Running video transcriber..."
python video_transcriber.py
