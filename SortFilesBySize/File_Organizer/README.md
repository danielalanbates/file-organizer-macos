# VS Code Multi-Window Launcher

A powerful native macOS application that launches multiple VS Code windows simultaneously and automatically arranges them in customizable grid layouts. Configure panels, workspaces, and display preferences for maximum productivity.

## Features

### Core Features
- 🚀 **Instant Launch**: Opens multiple VS Code windows simultaneously
- 📐 **Custom Grid Layouts**: Choose from 2x2, 2x3, 3x2, 4x2, or 3x3 grids (4-9 windows)
- 🖥️ **Multi-Monitor Support**: Select which display to use for your windows
- 🎨 **Custom App Icon**: Beautiful gradient icon with 6-window grid design
- 📱 **Menu Bar Integration**: Quick access from your status bar
- ⚡ **Native Performance**: Built with Swift for optimal macOS integration

### Configuration Options
- 💬 **Panel Configuration**: Choose which panels to open automatically:
  - Terminal panel (Cmd+Shift+`)
  - GitHub Copilot Chat
  - File Explorer (Cmd+Shift+E)
  - Debugger (Cmd+Shift+D)
- 📁 **Workspace Support**: Open windows with a specific workspace folder
- 🎯 **Quick Presets**: One-click configurations for common setups
  - Default: 2x3 grid with Terminal + Chat
  - Minimal: 2x2 grid with no panels
  - Full: 3x3 grid with all panels

### Automation
- 🔄 **Launch at Login**: Optional auto-start when you log in
- 📦 **Easy Installation**: One-command install script with LaunchAgent setup

## Prerequisites

- macOS 13.0 or later
- Visual Studio Code installed with `code` command in PATH
- GitHub Copilot extension installed in VS Code (for chat features)
- Swift toolchain for building (Xcode Command Line Tools)
- Optional: `librsvg` for icon generation (`brew install librsvg`)

## Installation

### Quick Install

1. Clone and build:
```bash
git clone <repository-url>
cd Organizer
./build.sh
```

2. Install to Applications:
```bash
./install.sh
```

The installer will:
- Copy the app to `/Applications/VSCode6x.app`
- Optionally set up launch at login
- Create LaunchAgent configuration

### Manual Installation

1. Build the application:
```bash
./build.sh
```

2. Copy to Applications:
```bash
cp -r Build/VSCode6x.app /Applications/
```

3. Launch from Applications folder or Spotlight

## Usage

### Native App

1. Launch VSCode 6x from Applications or Spotlight
2. Configure your preferences:
   - Select grid layout (2x2, 2x3, 3x2, 4x2, 3x3)
   - Choose which display to use
   - Toggle panels (Terminal, Chat, Explorer, Debugger)
   - Optionally specify a workspace path
3. Click "Launch Windows"
4. Enjoy your perfectly organized workspace!

### Quick Presets

Use the preset buttons for instant configurations:
- **Default**: 2x3 grid (6 windows) with Terminal + Chat panels
- **Minimal**: 2x2 grid (4 windows) with no panels
- **Full**: 3x3 grid (9 windows) with all panels enabled

### Shell Script Alternative

For a script-based approach without the GUI:

```bash
./Scripts/launch_vscode_6x.sh
```

## Window Layouts

The application supports multiple grid layouts:

### 2x3 Grid (6 windows - Default)
```
┌─────────┬─────────┬─────────┐
│ Window 1│ Window 2│ Window 3│
├─────────┼─────────┼─────────┤
│ Window 4│ Window 5│ Window 6│
└─────────┴─────────┴─────────┘
```

### 3x2 Grid (6 windows)
```
┌──────────┬──────────┐
│ Window 1 │ Window 2 │
├──────────┼──────────┤
│ Window 3 │ Window 4 │
├──────────┼──────────┤
│ Window 5 │ Window 6 │
└──────────┴──────────┘
```

### 2x2 Grid (4 windows)
```
┌──────────┬──────────┐
│ Window 1 │ Window 2 │
├──────────┼──────────┤
│ Window 3 │ Window 4 │
└──────────┴──────────┘
```

### 3x3 Grid (9 windows)
```
┌─────┬─────┬─────┐
│  1  │  2  │  3  │
├─────┼─────┼─────┤
│  4  │  5  │  6  │
├─────┼─────┼─────┤
│  7  │  8  │  9  │
└─────┴─────┴─────┘
```

### 4x2 Grid (8 windows)
```
┌──────────┬──────────┐
│ Window 1 │ Window 2 │
├──────────┼──────────┤
│ Window 3 │ Window 4 │
├──────────┼──────────┤
│ Window 5 │ Window 6 │
├──────────┼──────────┤
│ Window 7 │ Window 8 │
└──────────┴──────────┘
```

## Configuration

### Multi-Monitor Setup

1. Click "Refresh Displays" to detect all connected monitors
2. Select your preferred display from the dropdown
3. Windows will be arranged on the selected display

### Panel Configuration

Toggle any combination of panels to open automatically:
- **Terminal**: Opens integrated terminal in each window
- **GitHub Copilot Chat**: Opens Copilot chat sidebar
- **File Explorer**: Opens file browser sidebar
- **Debugger**: Opens debug panel

### Workspace Mode

To open all windows with a specific workspace:
1. Enter the workspace path or click "Browse..."
2. All windows will open with that workspace loaded
3. Leave empty for blank windows

### Launch at Login

To enable launch at login:
```bash
# During installation
./install.sh
# Answer 'y' when prompted

# Manual setup
cp com.copilot.vscode6x.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.copilot.vscode6x.plist
```

To disable:
```bash
launchctl unload ~/Library/LaunchAgents/com.copilot.vscode6x.plist
rm ~/Library/LaunchAgents/com.copilot.vscode6x.plist
```

## Development

### Project Structure

```
Organizer/
├── Package.swift                    # Swift package configuration
├── Sources/VSCodeLauncher/         # Main application source
│   ├── main.swift                  # App delegate and lifecycle
│   ├── MainViewController.swift    # UI controller with configuration
│   └── VSCodeWindowManager.swift   # Window management and AppleScript
├── Scripts/                        # Shell script alternatives
│   └── launch_vscode_6x.sh        # Bash-based launcher
├── Build/VSCode6x.app/            # Built application bundle
├── AppIcon.iconset/               # Icon assets
├── build.sh                       # Build automation script
├── generate_icons.sh              # Icon generation from SVG
├── install.sh                     # Installation script
└── com.copilot.vscode6x.plist    # LaunchAgent configuration
```

### Key Components

- **AppDelegate** (main.swift): Manages app lifecycle, status bar, and main window
- **MainViewController**: Provides UI for configuration with dropdowns, checkboxes, and presets
- **VSCodeWindowManager**: Handles VS Code window creation, positioning, and panel configuration
- **LaunchConfiguration**: Struct defining grid layout, display, panels, and workspace
- **Shell Script**: Alternative bash-based implementation

### Building

```bash
# Debug build with verbose output
swift build

# Release build (optimized)
./build.sh

# Generate icons from SVG
./generate_icons.sh

# Run tests
swift test
```

### Architecture

The app uses:
- **SwiftUI/AppKit** for native macOS UI
- **AppleScript** for VS Code window manipulation
- **NSScreen API** for multi-monitor support
- **Async/await** for non-blocking operations
- **LaunchAgents** for auto-start functionality

## Customization

### Adding New Grid Layouts

Edit `VSCodeWindowManager.swift`:

```swift
struct GridLayout {
    let rows: Int
    let columns: Int

    static let custom = GridLayout(rows: X, columns: Y)
}
```

Then add to `MainViewController.swift` dropdown:

```swift
gridLayoutPopup.addItems(withTitles: [
    "XxY (Z windows)"
])
```

### Custom Panel Shortcuts

Modify `configureVSCodeWindows()` in `VSCodeWindowManager.swift`:

```swift
if panelConfig.customPanel {
    panelCommands += """
        keystroke "key" using {modifiers}
        delay 0.2
    """
}
```

### Workspace Templates

To create workspace templates, save common workspace paths in the app or create presets.

## Troubleshooting

### Common Issues

**VS Code not launching:**
- Ensure VS Code is installed and `code` command is in PATH
- Try running `code --version` in terminal
- Add VS Code to PATH: Run "Shell Command: Install 'code' command in PATH" from VS Code Command Palette

**Windows not positioning correctly:**
- Grant accessibility permissions: System Settings > Privacy & Security > Accessibility
- Add VSCode6x.app to the list of allowed apps
- Restart the app after granting permissions

**Chat panel not opening:**
- Verify GitHub Copilot extension is installed and enabled
- Check your Copilot subscription is active
- Try opening chat manually (Ctrl+Cmd+I) to verify it works

**Multiple monitors not detected:**
- Click "Refresh Displays" button
- Ensure monitors are connected before launching the app
- Try disconnecting and reconnecting external displays

**Icon not showing:**
- Rebuild with `./build.sh` to regenerate icons
- Install librsvg: `brew install librsvg`
- Clear icon cache: `rm -rf ~/Library/Caches/com.apple.iconservices.store`

**Launch at login not working:**
- Check LaunchAgent is loaded: `launchctl list | grep vscode6x`
- View logs: `cat /tmp/vscode6x.err`
- Reinstall: `./install.sh`

### Debug Mode

Run with verbose output:
```bash
# Swift app
swift run VSCodeLauncher

# Shell script with debug
DEBUG=1 ./Scripts/launch_vscode_6x.sh

# Check LaunchAgent logs
tail -f /tmp/vscode6x.out
tail -f /tmp/vscode6x.err
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on macOS
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Roadmap

- [x] Multi-monitor support
- [x] Custom grid layouts (2x2, 3x2, 4x2, 3x3)
- [x] Workspace templates
- [x] Custom panel configurations
- [x] Launch at login
- [x] App icon and branding
- [ ] Save/load configuration presets
- [ ] Keyboard shortcuts for launching
- [ ] Window animation controls
- [ ] Support for other editors (Cursor, VSCodium)
- [ ] Configuration file support (.vscode6x.json)
- [ ] CLI interface for scripting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for developers who love organized workspaces
- Inspired by tiling window managers like i3, yabai, and Amethyst
- Made possible by VS Code's extensibility and macOS APIs
- Icon design inspired by VS Code branding

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

---

**Made with ⚡ by the Copilot automation project**

Enjoy your perfectly organized VS Code workspace! 🎉
