#!/bin/bash

echo "🎵 Starting Orpheus WebUI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.template .env
    echo "Please edit .env with your Bastion API details"
fi

# Launch the app
echo "Launching Gradio interface on http://localhost:7860"
python app.py
