#!/bin/bash

# Installation script for VSCode 6x Launcher
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="VSCode6x.app"
APP_PATH="$SCRIPT_DIR/Build/$APP_NAME"
INSTALL_PATH="/Applications/$APP_NAME"
LAUNCH_AGENT_SRC="$SCRIPT_DIR/com.copilot.vscode6x.plist"
LAUNCH_AGENT_DEST="$HOME/Library/LaunchAgents/com.copilot.vscode6x.plist"

echo "=== VSCode 6x Launcher Installer ==="
echo ""

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "❌ Error: App not found at $APP_PATH"
    echo "Please build the app first using ./build.sh"
    exit 1
fi

# Install to /Applications
echo "📦 Installing app to /Applications..."
if [ -d "$INSTALL_PATH" ]; then
    echo "⚠️  Removing existing installation..."
    rm -rf "$INSTALL_PATH"
fi

cp -R "$APP_PATH" "$INSTALL_PATH"
echo "✓ App installed to $INSTALL_PATH"

# Ask about launch at login
echo ""
read -p "Would you like to launch VSCode 6x at login? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Setting up launch at login..."

    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$HOME/Library/LaunchAgents"

    # Copy launch agent plist
    cp "$LAUNCH_AGENT_SRC" "$LAUNCH_AGENT_DEST"

    # Load the launch agent
    launchctl unload "$LAUNCH_AGENT_DEST" 2>/dev/null || true
    launchctl load "$LAUNCH_AGENT_DEST"

    echo "✓ Launch at login configured"
    echo ""
    echo "To disable launch at login later, run:"
    echo "  launchctl unload ~/Library/LaunchAgents/com.copilot.vscode6x.plist"
    echo "  rm ~/Library/LaunchAgents/com.copilot.vscode6x.plist"
else
    echo "ℹ️  Skipping launch at login setup"
    echo ""
    echo "To enable launch at login later, run:"
    echo "  cp $LAUNCH_AGENT_SRC ~/Library/LaunchAgents/"
    echo "  launchctl load ~/Library/LaunchAgents/com.copilot.vscode6x.plist"
fi

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "You can now:"
echo "  • Find VSCode 6x in your Applications folder"
echo "  • Launch it from Spotlight (Cmd+Space, type 'VSCode 6x')"
echo "  • Access it from the menu bar when running"
echo ""
echo "Enjoy your multi-window VS Code setup! 🎉"
