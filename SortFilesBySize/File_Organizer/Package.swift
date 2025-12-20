// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "VSCodeLauncher",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "VSCodeLauncher",
            targets: ["VSCodeLauncher"]
        ),
    ],
    dependencies: [
        // Dependencies for macOS app development and window management
    ],
    targets: [
        .executableTarget(
            name: "VSCodeLauncher",
            dependencies: [],
            path: "Sources/VSCodeLauncher"
        ),
        .testTarget(
            name: "VSCodeLauncherTests",
            dependencies: ["VSCodeLauncher"],
            path: "Tests/VSCodeLauncherTests"
        ),
    ]
)