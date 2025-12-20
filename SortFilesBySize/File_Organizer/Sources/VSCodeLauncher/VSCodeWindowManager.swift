import Foundation
import AppKit
import Cocoa

struct LaunchConfiguration {
    let gridLayout: GridLayout
    let screenIndex: Int
    let panelConfig: PanelConfiguration
    let workspace: String?

    static let `default` = LaunchConfiguration(
        gridLayout: .twoByThree,
        screenIndex: 0,
        panelConfig: .default,
        workspace: nil
    )
}

struct GridLayout {
    let rows: Int
    let columns: Int

    var windowCount: Int { rows * columns }

    static let twoByThree = GridLayout(rows: 2, columns: 3)
    static let threeByTwo = GridLayout(rows: 3, columns: 2)
    static let fourByTwo = GridLayout(rows: 4, columns: 2)
    static let twoByTwo = GridLayout(rows: 2, columns: 2)
    static let threeByThree = GridLayout(rows: 3, columns: 3)
}

struct PanelConfiguration {
    let openTerminal: Bool
    let openChat: Bool
    let openExplorer: Bool
    let openDebugger: Bool

    static let `default` = PanelConfiguration(
        openTerminal: true,
        openChat: true,
        openExplorer: false,
        openDebugger: false
    )

    static let minimal = PanelConfiguration(
        openTerminal: false,
        openChat: false,
        openExplorer: false,
        openDebugger: false
    )

    static let full = PanelConfiguration(
        openTerminal: true,
        openChat: true,
        openExplorer: true,
        openDebugger: true
    )
}

class VSCodeWindowManager {
    static let shared = VSCodeWindowManager()

    private init() {}

    // New method with configuration support
    func launchWindows(config: LaunchConfiguration = .default) async {
        guard let screen = getScreen(at: config.screenIndex) else {
            print("Could not get screen at index \(config.screenIndex)")
            return
        }

        let screenFrame = screen.visibleFrame
        let windowPositions = calculateWindowPositions(for: screenFrame, layout: config.gridLayout)

        print("Launching \(config.gridLayout.windowCount) windows in \(config.gridLayout.rows)x\(config.gridLayout.columns) grid")

        // Launch VS Code instances sequentially with positioning
        for (index, position) in windowPositions.enumerated() {
            await launchVSCodeWindow(at: position, windowIndex: index + 1, workspace: config.workspace)

            // Add a small delay between launches to ensure proper positioning
            try? await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
        }

        // After all windows are launched, configure them
        try? await Task.sleep(nanoseconds: 2_000_000_000) // 2 seconds
        await configureVSCodeWindows(panelConfig: config.panelConfig)
    }

    // Legacy method for backward compatibility
    func launchSixWindows() async {
        await launchWindows(config: .default)
    }

    // Get available screens
    func getAvailableScreens() -> [(index: Int, name: String, resolution: String)] {
        return NSScreen.screens.enumerated().map { index, screen in
            let frame = screen.frame
            let resolution = "\(Int(frame.width))x\(Int(frame.height))"
            let name = screen.localizedName
            return (index, name, resolution)
        }
    }

    private func getScreen(at index: Int) -> NSScreen? {
        let screens = NSScreen.screens
        guard index >= 0 && index < screens.count else {
            return NSScreen.main
        }
        return screens[index]
    }
    
    private func calculateWindowPositions(for screenFrame: NSRect, layout: GridLayout) -> [WindowPosition] {
        let windowWidth = screenFrame.width / CGFloat(layout.columns)
        let windowHeight = screenFrame.height / CGFloat(layout.rows)

        var positions: [WindowPosition] = []

        // Generate positions for each row and column
        for row in 0..<layout.rows {
            for col in 0..<layout.columns {
                let x = screenFrame.origin.x + (windowWidth * CGFloat(col))
                // macOS coordinates start from bottom, so we reverse row order
                let y = screenFrame.origin.y + screenFrame.height - (windowHeight * CGFloat(row + 1))

                positions.append(WindowPosition(
                    x: Int(x),
                    y: Int(y),
                    width: Int(windowWidth),
                    height: Int(windowHeight)
                ))
            }
        }

        return positions
    }
    
    private func launchVSCodeWindow(at position: WindowPosition, windowIndex: Int, workspace: String?) async {
        // If workspace is provided, launch with workspace, otherwise create new window
        let openCommand: String
        if let workspace = workspace {
            openCommand = "do shell script \"code --new-window '\(workspace)'\""
        } else {
            openCommand = """
            tell application "System Events"
                tell process "Visual Studio Code"
                    keystroke "n" using {shift down, command down}
                    delay 1
                end tell
            end tell
            """
        }

        let script = """
        tell application "Visual Studio Code"
            activate
            delay 0.5

            -- Create new window or open workspace
            \(openCommand)

            -- Position and resize the window
            tell application "System Events"
                tell process "Visual Studio Code"
                    set frontmost to true
                    delay 0.5
                    set position of front window to {\(position.x), \(position.y)}
                    set size of front window to {\(position.width), \(position.height)}
                end tell
            end tell
        end tell
        """

        await executeAppleScript(script)
    }
    
    private func configureVSCodeWindows(panelConfig: PanelConfiguration) async {
        // Build panel configuration commands based on settings
        var panelCommands = ""

        if panelConfig.openTerminal {
            panelCommands += """
                        -- Open terminal panel (Cmd+Shift+`)
                        keystroke "`" using {command down, shift down}
                        delay 0.2

            """
        }

        if panelConfig.openExplorer {
            panelCommands += """
                        -- Open explorer (Cmd+Shift+E)
                        keystroke "e" using {command down, shift down}
                        delay 0.2

            """
        }

        if panelConfig.openDebugger {
            panelCommands += """
                        -- Open debug panel (Cmd+Shift+D)
                        keystroke "d" using {command down, shift down}
                        delay 0.2

            """
        }

        if panelConfig.openChat {
            panelCommands += """
                        -- Open chat panel through Command Palette
                        keystroke "p" using {shift down, command down}
                        delay 0.3
                        keystroke "GitHub Copilot: Open Chat"
                        delay 0.2
                        key code 36 -- Enter key
                        delay 0.5

            """
        }

        let configScript = """
        tell application "Visual Studio Code"
            activate
            delay 1

            -- Get all VS Code windows
            tell application "System Events"
                tell process "Visual Studio Code"
                    repeat with win in windows
                        -- Click on the window to focus it
                        click win
                        delay 0.3

                        \(panelCommands)
                    end repeat
                end tell
            end tell
        end tell
        """

        await executeAppleScript(configScript)
    }
    
    private func executeAppleScript(_ script: String) async {
        await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                let appleScript = NSAppleScript(source: script)
                var errorInfo: NSDictionary?

                _ = appleScript?.executeAndReturnError(&errorInfo)

                if let error = errorInfo {
                    print("AppleScript error: \(error)")
                } else {
                    print("AppleScript executed successfully")
                }
                
                continuation.resume()
            }
        }
    }
}

struct WindowPosition {
    let x: Int
    let y: Int
    let width: Int
    let height: Int
}