#!/bin/bash
# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the game
echo "Starting Onions May Cry..."
cd src
python main.py
