#!/bin/bash

###############################################################################
# File Automation Suite - Launch Script
# Launches the menu bar app with proper error handling
###############################################################################

cd "$(dirname "$0")"

echo "🚀 Launching File Automation Suite..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import rumps, psutil" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Missing dependencies. Installing..."
    pip3 install rumps psutil
fi

# Check if app is already running
if pgrep -f "file_automation_menubar.py" > /dev/null; then
    echo "⚠️  App is already running!"
    echo ""
    echo "To quit the existing instance, look for the 📁 icon in your menu bar"
    echo "and select 'Quit File Automation Suite'"
    exit 1
fi

# Launch the app
echo "🚀 Starting File Automation Suite..."
echo ""
echo "Look for the 📁 icon in your menu bar!"
echo ""
echo "To quit this script: Press Ctrl+C"
echo "To quit the app: Click the menu bar icon → Quit"
echo ""

# Run the app and capture output
python3 file_automation_menubar.py 2>&1 | while read -r line; do
    echo "[App] $line"
done
