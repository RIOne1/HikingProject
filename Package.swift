// swift-tools-version: 6.1
import PackageDescription

// Keep the portable data layer free of SwiftUI, Core Location and Mapbox so
// its SQL and catalogue contracts can also be checked on the Linux runner.
let package = Package(
    name: "HikingProject",
    platforms: [.iOS(.v18), .macOS(.v14)],
    products: [
        .library(name: "HikingCore", targets: ["HikingCore"]),
        .library(name: "HikingSampleData", targets: ["HikingSampleData"])
    ],
    dependencies: [
        .package(url: "https://github.com/groue/GRDB.swift.git", exact: "7.12.0")
    ],
    targets: [
        .target(name: "HikingCore", dependencies: [.product(name: "GRDB", package: "GRDB.swift")], path: "apps/mobile/Core"),
        .target(name: "HikingSampleData", dependencies: ["HikingCore"], path: "shared", exclude: ["catalogue.schema.json"], resources: [.copy("fixtures")]),
        .testTarget(name: "HikingCoreTests", dependencies: ["HikingCore", "HikingSampleData", .product(name: "GRDB", package: "GRDB.swift")], path: "apps/mobile/CoreTests")
    ],
    swiftLanguageModes: [.v6]
)
