# Changelog

All notable changes to the VS Code Multi-Window Launcher project.

## [2.0.0] - 2025-10-16

### Added

#### Multi-Monitor Support
- Detect all connected displays automatically
- Select target display from dropdown menu
- "Refresh Displays" button to update monitor list
- Display resolution shown in monitor selection

#### Custom Grid Layouts
- 2x2 grid (4 windows)
- 2x3 grid (6 windows) - Default
- 3x2 grid (6 windows)
- 4x2 grid (8 windows)
- 3x3 grid (9 windows)
- Dynamic window positioning based on selected layout

#### Panel Configuration
- Toggle Terminal panel (Cmd+Shift+`)
- Toggle GitHub Copilot Chat panel
- Toggle File Explorer panel (Cmd+Shift+E)
- Toggle Debugger panel (Cmd+Shift+D)
- Panels open automatically in each window

#### Workspace Support
- Open all windows with a specific workspace folder
- Browse button for easy workspace selection
- Leave empty for blank windows

#### Quick Presets
- **Default Preset**: 2x3 grid with Terminal + Chat
- **Minimal Preset**: 2x2 grid with no panels
- **Full Preset**: 3x3 grid with all panels
- One-click application of preset configurations

#### App Icon & Branding
- Beautiful gradient icon with 6-window grid design
- SVG source file for easy customization
- Automated icon generation script
- All required icon sizes (16x16 to 512x512, @1x and @2x)
- ICNS bundle properly integrated

#### Installation & Automation
- Automated installation script (`install.sh`)
- LaunchAgent configuration for launch at login
- Interactive installer with user prompts
- Proper app bundle structure in /Applications

#### Enhanced UI
- Scrollable configuration panel
- Section headers for organization
- Larger window (550x650) for better UX
- Resizable window with minimum size constraints
- Status messages for user feedback
- Color-coded status (blue for info, green for success)

#### Build System Improvements
- Enhanced build script with emoji progress indicators
- Automatic icon generation during build
- Resource copying automation
- Clean build output messages

### Changed
- Window size increased from 400x300 to 550x650
- MainViewController redesigned with configuration options
- VSCodeWindowManager refactored to support configurations
- AppleScript commands now conditional based on panel config
- Window positioning algorithm supports arbitrary grid sizes

### Technical Improvements
- Introduced `LaunchConfiguration` struct for configuration management
- Added `GridLayout` struct with predefined layouts
- Added `PanelConfiguration` struct for panel toggles
- Multi-monitor support via NSScreen.screens API
- Backward compatibility maintained with `launchSixWindows()` method
- Type-safe configuration with Swift structs
- Async/await pattern for non-blocking operations

### Files Added
- `generate_icons.sh` - Icon generation automation
- `install.sh` - Installation script with LaunchAgent setup
- `com.copilot.vscode6x.plist` - LaunchAgent configuration
- `CHANGELOG.md` - This file
- `AppIcon.icns` - Generated icon bundle

### Files Modified
- `README.md` - Comprehensive documentation update
- `build.sh` - Enhanced with icon generation
- `main.swift` - Larger window size and resizable
- `MainViewController.swift` - Complete UI redesign
- `VSCodeWindowManager.swift` - Configuration support added
- `Info.plist` - Icon reference added

## [1.0.0] - 2025-10-15

### Initial Release
- Basic 2x3 grid layout (6 windows)
- Menu bar integration
- Terminal and Chat panel opening
- Shell script alternative
- Native Swift/AppKit application
- AppleScript-based window management

---

## Migration Guide

### From 1.0.0 to 2.0.0

The 2.0.0 release is backward compatible. Existing functionality works as before with the addition of new configuration options.

**New Features Available:**
1. Open the app and explore the new configuration UI
2. Try different grid layouts from the dropdown
3. Use quick presets for instant configurations
4. Configure which panels open automatically
5. Run `./install.sh` to set up launch at login

**No Breaking Changes:**
- The app still launches the default 2x3 grid if you don't change settings
- Shell script (`launch_vscode_6x.sh`) continues to work
- Status bar integration unchanged

**Recommended Actions:**
1. Rebuild: `./build.sh`
2. Install: `./install.sh`
3. Grant Accessibility permissions if prompted
4. Explore new configuration options
