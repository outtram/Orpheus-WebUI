#!/bin/bash

echo "📦 Updating dependencies for Python 3.13 compatibility..."
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install/update dependencies
pip install --upgrade -r requirements.txt

echo "✅ Dependencies updated!"
echo "🚀 Starting Orpheus WebUI..."

# Run the application
python app.py
