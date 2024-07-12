#!/bin/bash

# Create virtual environment
echo "Creating venv with name 'myenv'"
echo "------------------------------------------------"
read -p "Press Enter to continue..."
python -m venv myenv

# Activate virtual environment
echo "Activating virtual environment"
echo "------------------------------------------------"
read -p "Press Enter to continue..."
source myenv/Scripts/activate

# Install required dependencies
echo "Installing requirements.txt"
echo "------------------------------------------------"
read -p "Press Enter to continue..."
pip install -r requirements.txt
read -p "Press Enter to exit..."

# Run main.py
echo "Running main.py"
echo "------------------------------------------------"
read -p "Press Enter to continue..."
python main.py

# Wait for user input before exiting
read -p "Press Enter to exit..."
