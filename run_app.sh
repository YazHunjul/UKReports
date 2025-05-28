#!/bin/bash

# Canopy Commissioning Report Generator - Run Script
# This script ensures the application runs with the correct virtual environment

echo "🏭 Starting Canopy Commissioning Report Generator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if streamlit-drawable-canvas is available
echo "🔍 Checking streamlit-drawable-canvas availability..."
python -c "
try:
    import streamlit_drawable_canvas
    print('✅ streamlit-drawable-canvas is available - drawing canvas will be enabled')
except ImportError:
    print('⚠️  streamlit-drawable-canvas not available - will use file upload fallback')
"

# Start the application
echo "🚀 Starting Streamlit application..."
echo "📱 The application will be available at: http://localhost:8509"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run main.py --server.port 8509 