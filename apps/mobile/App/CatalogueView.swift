import HikingCore
import SwiftUI

struct CatalogueView: View {
    @State private var model = CatalogueModel()

    var body: some View {
        NavigationStack {
            Group {
                if model.isLoading {
                    ProgressView("Opening sample catalogue…")
                } else if let failure = model.failure {
                    ContentUnavailableView {
                        Label("Catalogue unavailable", systemImage: "externaldrive.badge.exclamationmark")
                    } description: {
                        Text(failure)
                    } actions: {
                        Button("Retry") { Task { await model.load() } }
                    }
                } else {
                    List {
                        Section {
                            Text("Fictional development routes. Do not use these for a hike.")
                                .foregroundStyle(.secondary)
                                .accessibilityIdentifier("sample-data-notice")
                        }
                        Section("Sample routes") {
                            ForEach(model.routes) { route in
                                NavigationLink {
                                    RouteDetailView(route: route)
                                } label: {
                                    VStack(alignment: .leading, spacing: 6) {
                                        Text(route.name).font(.headline)
                                        Text("\(route.difficulty.rawValue.capitalized) · \(route.distanceMetres) m · \(route.estimatedMinutes) min")
                                            .font(.subheadline).foregroundStyle(.secondary)
                                    }
                                    .padding(.vertical, 4)
                                }
                                .accessibilityIdentifier("route-\(route.id)")
                            }
                        }
                    }
                }
            }
            .navigationTitle("Route catalogue")
            .task { await model.load() }
        }
    }
}

private struct RouteDetailView: View {
    let route: RouteSummary

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Label("Synthetic sample · not hiking guidance", systemImage: "info.circle")
                    .font(.subheadline).foregroundStyle(.secondary)
                RouteMapPreview(route: route)
                    .frame(height: 260).clipShape(.rect(cornerRadius: 16))
                LabeledContent("Difficulty", value: route.difficulty.rawValue.capitalized)
                LabeledContent("Distance", value: "\(route.distanceMetres) metres")
                    .accessibilityIdentifier("route-distance")
                LabeledContent("Estimated time", value: "\(route.estimatedMinutes) minutes")
                Text(route.attribution).font(.footnote).foregroundStyle(.secondary)
                Text("This foundation contains metadata and a sample start point. Route geometry, offline maps and recording are not implemented yet.")
                    .font(.footnote)
            }
            .padding()
        }
        .navigationTitle(route.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}
