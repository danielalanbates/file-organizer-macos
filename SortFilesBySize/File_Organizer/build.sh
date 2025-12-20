#!/bin/bash

# Build script for VSCode 6x Launcher macOS app
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Building VSCode 6x Launcher ==="
echo ""

# Step 1: Generate app icons
echo "1️⃣  Generating app icons..."
if command -v rsvg-convert &> /dev/null; then
    "$SCRIPT_DIR/generate_icons.sh"
else
    echo "⚠️  Warning: rsvg-convert not found. Skipping icon generation."
    echo "   Install with: brew install librsvg"
fi

# Step 2: Clean previous builds
echo ""
echo "2️⃣  Cleaning previous build..."
rm -rf Build/VSCode6x.app/Contents/MacOS/VSCode6x

# Step 3: Compile Swift sources
echo ""
echo "3️⃣  Compiling Swift sources..."
swiftc -o Build/VSCode6x.app/Contents/MacOS/VSCode6x \
    Sources/VSCodeLauncher/*.swift \
    -framework Cocoa \
    -framework Foundation \
    -O

# Step 4: Copy resources
echo ""
echo "4️⃣  Copying resources..."
cp Scripts/launch_vscode_6x.sh Build/VSCode6x.app/Contents/Resources/
chmod +x Build/VSCode6x.app/Contents/Resources/launch_vscode_6x.sh

echo ""
echo "=== Build Complete! ==="
echo ""
echo "App bundle created at: Build/VSCode6x.app"
echo ""
echo "Next steps:"
echo "  • Test the app: open Build/VSCode6x.app"
echo "  • Install to /Applications: ./install.sh"
echo ""