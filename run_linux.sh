#!/bin/bash

set -e  # Exit on error

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "Running main program..."
python3 main.py

echo "All tasks completed successfully."
read -rp "Press Enter to exit the program..."
