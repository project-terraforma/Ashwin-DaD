#!/bin/bash

echo "🚀 Starting LLM Data Explorer Feedback System"
echo "=============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed"
    echo "   Please install pip: python3 -m ensurepip --upgrade"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Error installing dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Start the server
echo "🌐 Starting Flask API server..."
echo "   API: http://localhost:5000"
echo "   Dashboard: Open admin_dashboard.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

python3 feedback_api.py
