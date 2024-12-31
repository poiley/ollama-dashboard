#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Run Flask development server
echo -e "${GREEN}Starting development server...${NC}"
echo -e "${GREEN}Dashboard will be available at: http://127.0.0.1:5000${NC}"
echo -e "${YELLOW}Connecting to Ollama at: http://localhost:11434${NC}"

export OLLAMA_HOST=localhost
export OLLAMA_PORT=11434
export FLASK_APP=wsgi.py 
export FLASK_DEBUG=1

python -m flask run --host=127.0.0.1 --port=5000 