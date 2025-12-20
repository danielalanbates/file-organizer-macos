#!/bin/bash

###############################################################################
# File Automation Suite - Release Build Script
# Builds, signs, and packages the app for Gumroad/Lemon Squeezy distribution
#
# Prerequisites:
# 1. Apple Developer Account ($99/year)
# 2. Developer ID Application certificate installed
# 3. create-dmg installed: brew install create-dmg
# 4. Python 3.8+ with py2app: pip install py2app
#
# Usage:
#   ./build_release.sh
###############################################################################

set -e  # Exit on error

# Configuration
APP_NAME="File Automation Suite"
BUNDLE_ID="com.daniel.fileautomationsuite"
VERSION="1.0.0"
DEVELOPER_ID="Developer ID Application: Your Name (TEAM_ID)"  # TODO: Update this
APPLE_ID="your@email.com"  # TODO: Update this
TEAM_ID="YOUR_TEAM_ID"  # TODO: Update this

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}File Automation Suite - Release Build${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Step 1: Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build dist
mkdir -p dist

# Step 2: Build the app with py2app
echo -e "${YELLOW}🏗️  Building application bundle...${NC}"
python3 setup_menubar.py py2app

if [ ! -d "dist/$APP_NAME.app" ]; then
    echo -e "${RED}❌ Build failed! App bundle not found.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ App bundle created${NC}"

# Step 3: Code sign the app
echo -e "${YELLOW}✍️  Signing application bundle...${NC}"

# Sign all binaries in the app
find "dist/$APP_NAME.app/Contents/MacOS" -type f -exec \
    codesign --force --sign "$DEVELOPER_ID" --options runtime {} \;

# Sign the app bundle itself
codesign --deep --force --verify --verbose \
    --sign "$DEVELOPER_ID" \
    --options runtime \
    --timestamp \
    "dist/$APP_NAME.app"

# Verify signature
if codesign --verify --deep --strict "dist/$APP_NAME.app"; then
    echo -e "${GREEN}✅ Code signing successful${NC}"
else
    echo -e "${RED}❌ Code signing failed!${NC}"
    exit 1
fi

# Step 4: Create DMG installer
echo -e "${YELLOW}📦 Creating DMG installer...${NC}"

DMG_NAME="$APP_NAME-$VERSION.dmg"

# Remove old DMG if exists
rm -f "dist/$DMG_NAME"

# Create beautiful DMG with create-dmg
create-dmg \
    --volname "$APP_NAME" \
    --volicon "assets/app_icon.icns" \
    --window-pos 200 120 \
    --window-size 800 450 \
    --icon-size 100 \
    --icon "$APP_NAME.app" 200 190 \
    --hide-extension "$APP_NAME.app" \
    --app-drop-link 600 185 \
    --background "assets/dmg_background.png" \
    "dist/$DMG_NAME" \
    "dist/$APP_NAME.app"

if [ -f "dist/$DMG_NAME" ]; then
    echo -e "${GREEN}✅ DMG created${NC}"
else
    echo -e "${RED}❌ DMG creation failed!${NC}"
    exit 1
fi

# Step 5: Sign the DMG
echo -e "${YELLOW}✍️  Signing DMG...${NC}"
codesign --sign "$DEVELOPER_ID" "dist/$DMG_NAME"

# Step 6: Notarize with Apple
echo -e "${YELLOW}📤 Submitting for notarization...${NC}"
echo -e "${YELLOW}This may take 5-15 minutes...${NC}"

# Submit for notarization
xcrun notarytool submit "dist/$DMG_NAME" \
    --apple-id "$APPLE_ID" \
    --team-id "$TEAM_ID" \
    --password "@keychain:AC_PASSWORD" \
    --wait

# Check notarization result
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Notarization successful${NC}"

    # Staple the notarization ticket
    echo -e "${YELLOW}📎 Stapling notarization ticket...${NC}"
    xcrun stapler staple "dist/$DMG_NAME"

    echo -e "${GREEN}✅ Notarization ticket stapled${NC}"
else
    echo -e "${RED}❌ Notarization failed!${NC}"
    echo -e "${YELLOW}Check notarization log with:${NC}"
    echo -e "xcrun notarytool log <submission-id> --apple-id $APPLE_ID --team-id $TEAM_ID --password @keychain:AC_PASSWORD"
    exit 1
fi

# Step 7: Create distribution folder
echo -e "${YELLOW}📁 Creating distribution package...${NC}"

DIST_DIR="dist/FileAutomationSuite-v$VERSION"
mkdir -p "$DIST_DIR"

cp "dist/$DMG_NAME" "$DIST_DIR/"
cp README.md "$DIST_DIR/README.txt"
cp LICENSE "$DIST_DIR/LICENSE.txt"

# Create release notes
cat > "$DIST_DIR/RELEASE_NOTES.txt" << EOF
File Automation Suite v$VERSION
================================

Thank you for purchasing File Automation Suite!

What's New in v$VERSION:
- Professional menu bar application
- Real-time system monitoring
- Large file finder
- Time Machine backup status
- Disk space alerts

Installation:
1. Open the DMG file
2. Drag "File Automation Suite" to your Applications folder
3. Launch from Applications
4. Enter your license key when prompted

System Requirements:
- macOS 11.0 (Big Sur) or later
- 50 MB free disk space

Support:
Email: support@yourdomain.com
Documentation: https://yourdomain.com/docs

© 2025 Daniel. All rights reserved.
EOF

# Create ZIP for distribution
cd dist
zip -r "FileAutomationSuite-v$VERSION.zip" "FileAutomationSuite-v$VERSION"
cd ..

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ BUILD COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Distribution package: ${YELLOW}dist/FileAutomationSuite-v$VERSION.zip${NC}"
echo -e "DMG installer: ${YELLOW}dist/$DMG_NAME${NC}"
echo -e "App size: $(du -sh "dist/$APP_NAME.app" | cut -f1)"
echo -e "DMG size: $(du -sh "dist/$DMG_NAME" | cut -f1)"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "1. Test the DMG on a clean Mac"
echo -e "2. Upload to Gumroad/Lemon Squeezy"
echo -e "3. Update product page with download link"
echo ""
