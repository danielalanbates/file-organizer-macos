#!/bin/bash

# Generate all required icon sizes from SVG
# Requires librsvg (install with: brew install librsvg)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SVG_FILE="$SCRIPT_DIR/icon.svg"
ICONSET_DIR="$SCRIPT_DIR/AppIcon.iconset"

# Check if rsvg-convert is available
if ! command -v rsvg-convert &> /dev/null; then
    echo "Error: rsvg-convert not found. Install with: brew install librsvg"
    exit 1
fi

# Clean and create iconset directory
rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

echo "Generating icon assets from SVG..."

# Generate all required sizes
declare -a sizes=(16 32 64 128 256 512)

for size in "${sizes[@]}"; do
    echo "  Generating ${size}x${size}..."
    rsvg-convert -w $size -h $size "$SVG_FILE" > "$ICONSET_DIR/icon_${size}x${size}.png"

    # Generate @2x versions
    double=$((size * 2))
    echo "  Generating ${size}x${size}@2x..."
    rsvg-convert -w $double -h $double "$SVG_FILE" > "$ICONSET_DIR/icon_${size}x${size}@2x.png"
done

echo "Converting iconset to icns..."
iconutil -c icns "$ICONSET_DIR" -o "$SCRIPT_DIR/Build/VSCode6x.app/Contents/Resources/AppIcon.icns"

echo "✓ Icon generation complete!"
echo "Icon installed at: Build/VSCode6x.app/Contents/Resources/AppIcon.icns"
