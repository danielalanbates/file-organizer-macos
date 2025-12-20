#!/bin/bash
###############################################################################
# CodeMaster Launcher (Double-click to run)
###############################################################################

clear

echo "╔═══════════════════════════════════════╗"
echo "║       CodeMaster Launcher v1.0        ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Kill existing instances
echo "🔄 Stopping old instances..."
pkill -9 -f "python.*codemaster" 2>/dev/null
sleep 1

# Launch CodeMaster
echo "🚀 Starting CodeMaster..."
cd /Applications/CodeMaster.app/Contents/Resources/src

/Library/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python \
    codemaster.py \
    > /tmp/codemaster.log 2>&1 &

CODEMASTER_PID=$!

sleep 3

if ps -p $CODEMASTER_PID > /dev/null 2>&1; then
    echo "✅ CodeMaster Started!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  🤖 Look at the TOP-RIGHT of your screen"
    echo "     for the robot emoji icon!"
    echo ""
    echo "  📍 Click the 🤖 to open the menu"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Process ID: $CODEMASTER_PID"
    echo "Log file: /tmp/codemaster.log"
    echo ""
    echo "Press Enter to close this window..."
    read
else
    echo "❌ Failed to start. Checking log..."
    cat /tmp/codemaster.log
    echo ""
    echo "Press Enter to close..."
    read
    exit 1
fi
