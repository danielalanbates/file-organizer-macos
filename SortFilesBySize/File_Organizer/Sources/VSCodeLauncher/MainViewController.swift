import Cocoa
import Foundation

class MainViewController: NSViewController {
    private var launchButton: NSButton!
    private var statusLabel: NSTextField!

    // Configuration controls
    private var gridLayoutPopup: NSPopUpButton!
    private var screenPopup: NSPopUpButton!
    private var terminalCheckbox: NSButton!
    private var chatCheckbox: NSButton!
    private var explorerCheckbox: NSButton!
    private var debuggerCheckbox: NSButton!
    private var workspaceField: NSTextField!

    override func loadView() {
        view = NSView(frame: NSRect(x: 0, y: 0, width: 500, height: 600))
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.controlBackgroundColor.cgColor

        setupUI()
    }

    private func setupUI() {
        let scrollView = NSScrollView(frame: view.bounds)
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.hasVerticalScroller = true
        scrollView.hasHorizontalScroller = false
        scrollView.autohidesScrollers = true

        let contentView = NSView()
        contentView.translatesAutoresizingMaskIntoConstraints = false

        let stackView = NSStackView()
        stackView.orientation = .vertical
        stackView.spacing = 15
        stackView.alignment = .leading
        stackView.translatesAutoresizingMaskIntoConstraints = false

        // Title
        let titleLabel = NSTextField(labelWithString: "VS Code Multi-Window Launcher")
        titleLabel.font = NSFont.boldSystemFont(ofSize: 18)
        titleLabel.alignment = .center
        titleLabel.translatesAutoresizingMaskIntoConstraints = false

        // Grid Layout Section
        let gridSection = createSectionLabel("Grid Layout")
        gridLayoutPopup = NSPopUpButton()
        gridLayoutPopup.addItems(withTitles: [
            "2x3 (6 windows)",
            "3x2 (6 windows)",
            "2x2 (4 windows)",
            "4x2 (8 windows)",
            "3x3 (9 windows)"
        ])
        gridLayoutPopup.selectItem(at: 0)

        // Screen Selection Section
        let screenSection = createSectionLabel("Display")
        screenPopup = NSPopUpButton()
        updateScreenList()

        let refreshButton = NSButton()
        refreshButton.title = "Refresh Displays"
        refreshButton.bezelStyle = .rounded
        refreshButton.target = self
        refreshButton.action = #selector(refreshDisplays)

        let screenStack = NSStackView(views: [screenPopup, refreshButton])
        screenStack.orientation = .horizontal
        screenStack.spacing = 10

        // Panel Configuration Section
        let panelSection = createSectionLabel("Panels to Open")

        terminalCheckbox = NSButton(checkboxWithTitle: "Terminal", target: nil, action: nil)
        terminalCheckbox.state = .on

        chatCheckbox = NSButton(checkboxWithTitle: "GitHub Copilot Chat", target: nil, action: nil)
        chatCheckbox.state = .on

        explorerCheckbox = NSButton(checkboxWithTitle: "File Explorer", target: nil, action: nil)
        explorerCheckbox.state = .off

        debuggerCheckbox = NSButton(checkboxWithTitle: "Debugger", target: nil, action: nil)
        debuggerCheckbox.state = .off

        // Workspace Section
        let workspaceSection = createSectionLabel("Workspace (Optional)")
        workspaceField = NSTextField()
        workspaceField.placeholderString = "Path to workspace folder"
        workspaceField.translatesAutoresizingMaskIntoConstraints = false

        let browseButton = NSButton()
        browseButton.title = "Browse..."
        browseButton.bezelStyle = .rounded
        browseButton.target = self
        browseButton.action = #selector(browseWorkspace)

        let workspaceStack = NSStackView(views: [workspaceField, browseButton])
        workspaceStack.orientation = .horizontal
        workspaceStack.spacing = 10
        workspaceStack.translatesAutoresizingMaskIntoConstraints = false

        // Presets Section
        let presetsSection = createSectionLabel("Quick Presets")

        let defaultPresetBtn = NSButton()
        defaultPresetBtn.title = "Default (2x3, Terminal + Chat)"
        defaultPresetBtn.bezelStyle = .rounded
        defaultPresetBtn.target = self
        defaultPresetBtn.action = #selector(applyDefaultPreset)

        let minimalPresetBtn = NSButton()
        minimalPresetBtn.title = "Minimal (2x2, No Panels)"
        minimalPresetBtn.bezelStyle = .rounded
        minimalPresetBtn.target = self
        minimalPresetBtn.action = #selector(applyMinimalPreset)

        let fullPresetBtn = NSButton()
        fullPresetBtn.title = "Full (3x3, All Panels)"
        fullPresetBtn.bezelStyle = .rounded
        fullPresetBtn.target = self
        fullPresetBtn.action = #selector(applyFullPreset)

        let presetStack = NSStackView(views: [defaultPresetBtn, minimalPresetBtn, fullPresetBtn])
        presetStack.orientation = .horizontal
        presetStack.spacing = 10

        // Launch button
        launchButton = NSButton()
        launchButton.title = "Launch Windows"
        launchButton.bezelStyle = .rounded
        launchButton.controlSize = .large
        launchButton.target = self
        launchButton.action = #selector(launchVSCodeWindows)
        launchButton.translatesAutoresizingMaskIntoConstraints = false

        // Status label
        statusLabel = NSTextField(labelWithString: "Ready to launch")
        statusLabel.alignment = .center
        statusLabel.textColor = .secondaryLabelColor
        statusLabel.translatesAutoresizingMaskIntoConstraints = false

        // Add all to stack view
        stackView.addArrangedSubview(gridSection)
        stackView.addArrangedSubview(gridLayoutPopup)
        stackView.addArrangedSubview(createSpacer(height: 10))

        stackView.addArrangedSubview(screenSection)
        stackView.addArrangedSubview(screenStack)
        stackView.addArrangedSubview(createSpacer(height: 10))

        stackView.addArrangedSubview(panelSection)
        stackView.addArrangedSubview(terminalCheckbox)
        stackView.addArrangedSubview(chatCheckbox)
        stackView.addArrangedSubview(explorerCheckbox)
        stackView.addArrangedSubview(debuggerCheckbox)
        stackView.addArrangedSubview(createSpacer(height: 10))

        stackView.addArrangedSubview(workspaceSection)
        stackView.addArrangedSubview(workspaceStack)
        stackView.addArrangedSubview(createSpacer(height: 10))

        stackView.addArrangedSubview(presetsSection)
        stackView.addArrangedSubview(presetStack)
        stackView.addArrangedSubview(createSpacer(height: 20))

        stackView.addArrangedSubview(launchButton)
        stackView.addArrangedSubview(statusLabel)

        contentView.addSubview(titleLabel)
        contentView.addSubview(stackView)

        scrollView.documentView = contentView
        view.addSubview(scrollView)

        // Constraints
        NSLayoutConstraint.activate([
            scrollView.topAnchor.constraint(equalTo: view.topAnchor),
            scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            scrollView.bottomAnchor.constraint(equalTo: view.bottomAnchor),

            titleLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 20),
            titleLabel.centerXAnchor.constraint(equalTo: contentView.centerXAnchor),

            stackView.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 30),
            stackView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 30),
            stackView.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -30),
            stackView.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -30),

            contentView.widthAnchor.constraint(equalTo: scrollView.widthAnchor),

            workspaceField.widthAnchor.constraint(equalToConstant: 300),
            launchButton.widthAnchor.constraint(equalToConstant: 200),
            statusLabel.widthAnchor.constraint(equalToConstant: 400)
        ])
    }

    private func createSectionLabel(_ text: String) -> NSTextField {
        let label = NSTextField(labelWithString: text)
        label.font = NSFont.boldSystemFont(ofSize: 14)
        return label
    }

    private func createSpacer(height: CGFloat) -> NSView {
        let spacer = NSView()
        spacer.translatesAutoresizingMaskIntoConstraints = false
        spacer.heightAnchor.constraint(equalToConstant: height).isActive = true
        return spacer
    }

    private func updateScreenList() {
        screenPopup.removeAllItems()
        let screens = VSCodeWindowManager.shared.getAvailableScreens()
        for screen in screens {
            screenPopup.addItem(withTitle: "\(screen.name) (\(screen.resolution))")
        }
        if screens.isEmpty {
            screenPopup.addItem(withTitle: "Main Display")
        }
    }

    @objc private func refreshDisplays() {
        updateScreenList()
        statusLabel.stringValue = "Display list refreshed"
        statusLabel.textColor = .systemBlue

        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.statusLabel.stringValue = "Ready to launch"
            self.statusLabel.textColor = .secondaryLabelColor
        }
    }

    @objc private func browseWorkspace() {
        let openPanel = NSOpenPanel()
        openPanel.canChooseFiles = false
        openPanel.canChooseDirectories = true
        openPanel.allowsMultipleSelection = false
        openPanel.prompt = "Select Workspace"

        openPanel.begin { response in
            if response == .OK, let url = openPanel.url {
                self.workspaceField.stringValue = url.path
            }
        }
    }

    @objc private func applyDefaultPreset() {
        gridLayoutPopup.selectItem(at: 0) // 2x3
        terminalCheckbox.state = .on
        chatCheckbox.state = .on
        explorerCheckbox.state = .off
        debuggerCheckbox.state = .off
        statusLabel.stringValue = "Default preset applied"
        statusLabel.textColor = .systemBlue
    }

    @objc private func applyMinimalPreset() {
        gridLayoutPopup.selectItem(at: 2) // 2x2
        terminalCheckbox.state = .off
        chatCheckbox.state = .off
        explorerCheckbox.state = .off
        debuggerCheckbox.state = .off
        statusLabel.stringValue = "Minimal preset applied"
        statusLabel.textColor = .systemBlue
    }

    @objc private func applyFullPreset() {
        gridLayoutPopup.selectItem(at: 4) // 3x3
        terminalCheckbox.state = .on
        chatCheckbox.state = .on
        explorerCheckbox.state = .on
        debuggerCheckbox.state = .on
        statusLabel.stringValue = "Full preset applied"
        statusLabel.textColor = .systemBlue
    }

    private func getCurrentConfiguration() -> LaunchConfiguration {
        let gridLayout: GridLayout
        switch gridLayoutPopup.indexOfSelectedItem {
        case 0: gridLayout = .twoByThree
        case 1: gridLayout = .threeByTwo
        case 2: gridLayout = .twoByTwo
        case 3: gridLayout = .fourByTwo
        case 4: gridLayout = .threeByThree
        default: gridLayout = .twoByThree
        }

        let panelConfig = PanelConfiguration(
            openTerminal: terminalCheckbox.state == .on,
            openChat: chatCheckbox.state == .on,
            openExplorer: explorerCheckbox.state == .on,
            openDebugger: debuggerCheckbox.state == .on
        )

        let workspace = workspaceField.stringValue.isEmpty ? nil : workspaceField.stringValue

        return LaunchConfiguration(
            gridLayout: gridLayout,
            screenIndex: screenPopup.indexOfSelectedItem,
            panelConfig: panelConfig,
            workspace: workspace
        )
    }

    @objc private func launchVSCodeWindows() {
        launchButton.isEnabled = false
        let config = getCurrentConfiguration()
        statusLabel.stringValue = "Launching \(config.gridLayout.windowCount) VS Code windows..."
        statusLabel.textColor = .controlAccentColor

        Task {
            await VSCodeWindowManager.shared.launchWindows(config: config)

            DispatchQueue.main.async {
                self.launchButton.isEnabled = true
                self.statusLabel.stringValue = "Launch completed!"
                self.statusLabel.textColor = .systemGreen

                // Reset status after 3 seconds
                DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                    self.statusLabel.stringValue = "Ready to launch"
                    self.statusLabel.textColor = .secondaryLabelColor
                }
            }
        }
    }
}
