# File Automation Suite - Build Instructions

Complete guide to building and distributing the professional macOS app.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Building for Gumroad/Lemon Squeezy](#building-for-gumroadlemon-squeezy)
4. [Building for Mac App Store](#building-for-mac-app-store)
5. [Testing](#testing)
6. [Distribution](#distribution)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Apple Developer Account
- **Cost:** $99/year
- **Sign up:** https://developer.apple.com/programs/
- **Required for:** Code signing and notarization

### Development Tools

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install create-dmg for beautiful DMG installers
brew install create-dmg

# Install Python dependencies
pip3 install --upgrade pip
pip3 install py2app rumps psutil
```

### Code Signing Certificate

1. Open **Keychain Access**
2. Go to **Certificate Assistant** → **Request a Certificate from a Certificate Authority**
3. Fill in your email and name
4. Save to disk
5. Go to [Apple Developer Certificates](https://developer.apple.com/account/resources/certificates/list)
6. Create **Developer ID Application** certificate
7. Upload your certificate request
8. Download and install the certificate (double-click .cer file)

### App-Specific Password (for Notarization)

```bash
# Generate app-specific password at:
# https://appleid.apple.com/account/manage → Security → App-Specific Passwords

# Store in keychain
xcrun notarytool store-credentials "AC_PASSWORD" \
    --apple-id "your@email.com" \
    --team-id "YOUR_TEAM_ID" \
    --password "xxxx-xxxx-xxxx-xxxx"
```

---

## Initial Setup

### 1. Clone/Navigate to Project

```bash
cd /Users/daniel/Documents/aicode/03-File_Automation
```

### 2. Update Configuration

Edit `build_release.sh` with your details:

```bash
DEVELOPER_ID="Developer ID Application: Your Name (TEAM_ID)"
APPLE_ID="your@email.com"
TEAM_ID="YOUR_TEAM_ID"
```

To find your Team ID:
```bash
# List all certificates
security find-identity -v -p codesigning

# Your Team ID is in parentheses
```

### 3. Create App Icon

You need an icon in multiple sizes. Use the existing `icon.svg` or create new:

```bash
# Install iconutil (built into macOS)
# Convert icon to .icns format

mkdir -p AppIcon.iconset
sips -z 16 16     icon.png --out AppIcon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out AppIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out AppIcon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out AppIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out AppIcon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out AppIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out AppIcon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out AppIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out AppIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out AppIcon.iconset/icon_512x512@2x.png

iconutil -c icns AppIcon.iconset -o assets/app_icon.icns
```

### 4. Create DMG Background (Optional)

Create a 800x450px background image for the DMG installer:

- Put your app screenshot or branding
- Save as `assets/dmg_background.png`
- Or skip and remove `--background` line from build script

---

## Building for Gumroad/Lemon Squeezy

This creates a **non-sandboxed** version with full functionality.

### Build Steps

```bash
# Run the build script
./build_release.sh
```

This will:
1. ✅ Build the app with py2app
2. ✅ Code sign all binaries
3. ✅ Create beautiful DMG installer
4. ✅ Sign the DMG
5. ✅ Notarize with Apple (5-15 minutes)
6. ✅ Staple notarization ticket
7. ✅ Create distribution ZIP

### Output

```
dist/
├── File Automation Suite.app           # Signed app bundle
├── File Automation Suite-1.0.0.dmg     # Notarized DMG
└── FileAutomationSuite-v1.0.0.zip     # Distribution package
    ├── File Automation Suite-1.0.0.dmg
    ├── README.txt
    ├── LICENSE.txt
    └── RELEASE_NOTES.txt
```

### Upload to Gumroad/Lemon Squeezy

1. **Gumroad:**
   - Go to [gumroad.com/products](https://gumroad.com/products)
   - Click **"New Product"**
   - Upload `FileAutomationSuite-v1.0.0.zip`
   - Set price: $39
   - Enable license keys
   - Publish!

2. **Lemon Squeezy:**
   - Go to [lemonsqueezy.com/products](https://lemonsqueezy.com/products)
   - Click **"New Product"**
   - Upload ZIP
   - Configure pricing and license keys
   - Activate!

---

## Building for Mac App Store

The Mac App Store version requires **sandboxing** and has more restrictions.

### Key Differences

| Feature | Gumroad/Lemon | Mac App Store |
|---------|---------------|---------------|
| Sandbox | ❌ No | ✅ Yes (required) |
| Full disk access | ✅ Yes | ⚠️ Needs entitlements |
| Price | $39 | $49 (to account for 30% fee) |
| Updates | Manual | Through App Store |
| Distribution | Direct download | App Store only |

### Additional Requirements

1. **Mac App Distribution Certificate**
   - Different from Developer ID
   - Get from [Apple Developer Certificates](https://developer.apple.com/account/resources/certificates/list)
   - Choose "Mac App Distribution"

2. **App Sandbox Entitlements**

Create `entitlements_mas.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Enable App Sandbox -->
    <key>com.apple.security.app-sandbox</key>
    <true/>

    <!-- Allow file access (user-selected files only) -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>

    <!-- Allow reading system info -->
    <key>com.apple.security.temporary-exception.files.absolute-path.read-only</key>
    <array>
        <string>/usr/sbin/tmutil</string>
    </array>

    <!-- Outgoing network (for license validation) -->
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
</plist>
```

3. **Build for App Store**

```bash
# Sign with Mac App Distribution certificate
codesign --deep --force --sign "3rd Party Mac Developer Application: Your Name (TEAM_ID)" \
    --entitlements entitlements_mas.plist \
    "dist/File Automation Suite.app"

# Create .pkg for App Store submission
productbuild --component "dist/File Automation Suite.app" /Applications \
    --sign "3rd Party Mac Developer Installer: Your Name (TEAM_ID)" \
    "dist/FileAutomationSuite-MAS.pkg"
```

4. **Submit to App Store**

Use **Transporter** app (free from Mac App Store):
- Open Transporter
- Drag `FileAutomationSuite-MAS.pkg`
- Click **Deliver**

### App Store Limitations

⚠️ **Features that won't work in sandboxed version:**
- Direct access to Time Machine without user permission
- System-wide file scanning (user must select folders)
- Launch at login (requires additional entitlement)

**Workaround:** Ask user to grant Full Disk Access in System Settings.

---

## Testing

### Pre-Release Testing Checklist

- [ ] Test on **clean Mac** (not your development machine)
- [ ] Test on macOS 11 (Big Sur) minimum
- [ ] Test on macOS 15 (Sequoia) latest
- [ ] Verify code signature: `codesign --verify --deep --strict app.app`
- [ ] Verify notarization: `spctl --assess --type execute -vv app.app`
- [ ] Test DMG installer: Open, drag to Applications, launch
- [ ] Test license key activation
- [ ] Test all menu items
- [ ] Test system monitoring alerts
- [ ] Test file scanning
- [ ] Test Time Machine status

### Test Commands

```bash
# Verify code signature
codesign --verify --deep --strict "dist/File Automation Suite.app"

# Verify notarization
spctl --assess --type execute -vv "dist/File Automation Suite.app"

# Check app info
codesign -dvvv "dist/File Automation Suite.app"

# Test DMG
hdiutil mount "dist/File Automation Suite-1.0.0.dmg"
```

---

## Distribution

### Gumroad Distribution

1. **Upload ZIP** (FileAutomationSuite-v1.0.0.zip)
2. **Product Settings:**
   - Name: File Automation Suite for Mac
   - Price: $39
   - Description: (Use landing page copy)
   - Screenshots: Upload 4-6 images
3. **Enable License Keys:**
   - Settings → License Keys → Enable
   - Format: `XXXX-XXXX-XXXX-XXXX`
4. **Customize Email:**
   ```
   Thanks for purchasing File Automation Suite!

   Your license key: {license_key}

   Download: {download_link}

   Installation:
   1. Open the DMG file
   2. Drag to Applications
   3. Launch and enter your license key

   Need help? Reply to this email!
   ```

### Lemon Squeezy Distribution

Similar to Gumroad but with better webhooks:

```python
# Example webhook handler for license validation
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    """Verify Lemon Squeezy webhook signature."""
    computed = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
```

### Mac App Store Distribution

1. **App Store Connect:**
   - Create new app
   - Fill in metadata (screenshots, description)
   - Submit for review (7-14 days)

2. **Pricing:**
   - Set to $49 (accounts for 30% Apple fee)
   - Or use tiered pricing

3. **Updates:**
   - Increment version number
   - Upload new build
   - Submit for review

---

## Troubleshooting

### Code Signing Errors

**Problem:** `code object is not signed at all`

**Solution:**
```bash
# Sign all frameworks first
find "dist/File Automation Suite.app" -name "*.dylib" -exec codesign --force --sign "$DEVELOPER_ID" {} \;

# Then sign the app
codesign --deep --force --sign "$DEVELOPER_ID" "dist/File Automation Suite.app"
```

### Notarization Fails

**Problem:** `The binary is not signed with a valid Developer ID certificate`

**Solution:**
- Make sure you're using "Developer ID Application" certificate (not "Mac App Distribution")
- Check certificate validity: `security find-identity -v -p codesigning`

### DMG Won't Open

**Problem:** `"File Automation Suite.dmg" is damaged and can't be opened`

**Solution:**
- This usually means notarization failed
- Check notarization status: `xcrun notarytool info <submission-id>`
- Re-notarize and staple

### App Won't Launch

**Problem:** `"File Automation Suite" is damaged and can't be opened`

**Solution:**
```bash
# Remove quarantine attribute
xattr -cr "File Automation Suite.app"

# Or user can right-click → Open (instead of double-click)
```

### License Key Not Saving

**Problem:** License key doesn't persist after restart

**Solution:**
- Check file permissions: `ls -la ~/.file_automation_suite/`
- Recreate config directory:
  ```bash
  rm -rf ~/.file_automation_suite
  # Launch app and re-enter license
  ```

---

## Version Updates

### Bumping Version

1. Update version in:
   - `setup_menubar.py` → `CFBundleVersion`
   - `build_release.sh` → `VERSION`
   - `file_automation_menubar.py` (if shown in UI)

2. Update `CHANGELOG.md`

3. Rebuild:
   ```bash
   ./build_release.sh
   ```

4. Upload new version to Gumroad/Lemon Squeezy

5. Notify customers via email:
   ```
   File Automation Suite v1.1.0 is now available!

   What's new:
   - New feature X
   - Bug fix Y

   Download: [link]
   ```

---

## Support Resources

- **Apple Developer Forums:** https://developer.apple.com/forums/
- **Notarization Guide:** https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- **py2app Docs:** https://py2app.readthedocs.io/
- **Gumroad Help:** https://help.gumroad.com/

---

## Quick Reference

```bash
# Build for direct sale
./build_release.sh

# Test signature
codesign --verify --deep "dist/File Automation Suite.app"

# Test notarization
spctl --assess -vv "dist/File Automation Suite.app"

# Check certificates
security find-identity -v -p codesigning

# View app version
defaults read "dist/File Automation Suite.app/Contents/Info.plist" CFBundleShortVersionString
```

---

**Ready to build?** Start with the Gumroad version, it's the fastest path to revenue!
