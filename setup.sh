#!/bin/bash
# Setup script for Blob Tracker project

echo "=================================="
echo "Blob Tracker - Setup Script"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✓ Setup Complete!"
    echo "=================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Activate the environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Try the quick test:"
    echo "   python create_test_video.py"
    echo "   python blob_tracker.py test_input.mp4 test_output.mp4 --preview"
    echo ""
    echo "3. Or process your own video:"
    echo "   python blob_tracker.py your_video.mp4 output.mp4"
    echo ""
    echo "For more info, see QUICKSTART.md"
    echo ""
else
    echo ""
    echo "❌ Error installing dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi
