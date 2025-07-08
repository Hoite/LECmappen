#!/bin/bash
# LEC Mappen Generator - Unix/Linux/macOS Wrapper
# Controleert of Python beschikbaar is en start het script

echo "LEC Mappen Generator"
echo ""

# Controleer of Python beschikbaar is
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is niet geinstalleerd of niet gevonden in PATH"
    echo "Installeer Python 3 via je package manager of van https://python.org"
    exit 1
fi

# Maak het script executable
chmod +x lec_mappen.py

# Start het Python script in interactieve modus
python3 lec_mappen.py --interactive
