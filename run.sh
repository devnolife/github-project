#!/bin/bash
# GitHub Proposal Generator - Unix/Linux/macOS Run Script

echo "Starting GitHub Proposal Generator..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing/updating requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo
    echo "Warning: .env file not found"
    echo "Please copy .env.example to .env and configure your settings"
    echo
    read -p "Press Enter to continue..."
fi

# Run the application
echo
echo "Starting application..."
echo
python src/main.py
