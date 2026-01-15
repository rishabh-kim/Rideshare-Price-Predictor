#!/bin/bash
# Quick Start Script for Rideshare Streamlit App

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚗 Rideshare Price Predictor - Quick Start${NC}"
echo "=========================================="

# Navigate to app directory
cd "$(dirname "$0")"

# Check if rideshare_kaggle.csv exists
if [ ! -f "rideshare_kaggle.csv" ]; then
    echo -e "${RED}❌ Error: rideshare_kaggle.csv not found!${NC}"
    echo "Please ensure the CSV file is in this directory."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found!${NC}"
    exit 1
fi

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
python3 -m pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Start Streamlit app
echo -e "${GREEN}✅ Starting Streamlit app...${NC}"
echo "📱 Open your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 -m streamlit run app.py --logger.level=error
