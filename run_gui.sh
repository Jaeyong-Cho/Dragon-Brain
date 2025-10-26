#!/bin/bash

# Dragon Brain GUI Launcher

echo "🐉 Dragon Brain - Markdown Similarity Analyzer"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  PyQt6 not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Launch GUI
echo ""
echo "🚀 Launching GUI..."
python3 gui.py
