import Foundation
import AppKit
import Cocoa

// Create and run the application
let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusBarItem: NSStatusItem?
    var window: NSWindow?
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        setupStatusBar()
        setupMainWindow()
    }
    
    private func setupStatusBar() {
        statusBarItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        statusBarItem?.button?.title = "VSCode 6x"
        statusBarItem?.button?.action = #selector(statusBarButtonClicked)
        statusBarItem?.button?.target = self
    }
    
    private func setupMainWindow() {
        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 550, height: 650),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        window?.title = "VS Code Multi-Window Launcher"
        window?.center()
        window?.contentViewController = MainViewController()
        window?.makeKeyAndOrderFront(nil)
        window?.minSize = NSSize(width: 500, height: 600)
    }
    
    @objc private func statusBarButtonClicked() {
        window?.makeKeyAndOrderFront(nil)
    }
    
    func applicationWillTerminate(_ aNotification: Notification) {
        // Cleanup if needed
    }
    
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return false // Keep app running even when window is closed
    }
}