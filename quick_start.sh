#!/bin/bash

# Quick Start Script for Audio Transcription System
# This script helps you get started quickly

echo "=================================================="
echo "Audio Transcription System - Quick Start"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Create necessary directories
echo "Creating storage directories..."
mkdir -p uploads transcripts summaries notes
echo "✅ Directories created"
echo ""

echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend API:"
echo "   python3 backend_api.py"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   streamlit run frontend_app.py"
echo ""
echo "3. Open your browser to:"
echo "   http://localhost:8501"
echo ""
echo "=================================================="
