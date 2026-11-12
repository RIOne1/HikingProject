import CoreLocation
import HikingCore
import MapboxMaps
import SwiftUI

struct RouteMapPreview: View {
    let route: RouteSummary

    private var hasPublicToken: Bool {
        // UI smoke tests stay tokenless even on a developer's configured machine.
        guard !ProcessInfo.processInfo.arguments.contains("--tokenless-preview") else { return false }
        let token = Bundle.main.object(forInfoDictionaryKey: "MBXAccessToken") as? String ?? ""
        return token.hasPrefix("pk.")
    }

    var body: some View {
        if hasPublicToken {
            Map(initialViewport: .camera(
                center: CLLocationCoordinate2D(latitude: route.startLatitude, longitude: route.startLongitude),
                zoom: 11
            ))
            .accessibilityLabel("Map preview around the synthetic start point")
        } else {
            ContentUnavailableView(
                "Map preview not configured", systemImage: "map",
                description: Text("The catalogue works without a Mapbox token. See the mobile development guide to enable an online preview.")
            )
            .background(.quaternary)
            .accessibilityIdentifier("map-preview-unconfigured")
        }
    }
}
