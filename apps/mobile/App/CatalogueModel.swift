import Foundation
import HikingCore
import HikingSampleData
import Observation

@MainActor
@Observable
final class CatalogueModel {
    private(set) var routes: [RouteSummary] = []
    private(set) var failure: String?
    private(set) var isLoading = true

    func load() async {
        do {
            let directory = try FileManager.default.url(
                for: .applicationSupportDirectory, in: .userDomainMask,
                appropriateFor: nil, create: true
            )
            let store = try RouteStore(path: directory.appendingPathComponent("foundation.sqlite").path)
            var storedRoutes = try await store.routes()
            if storedRoutes.isEmpty {
                try await store.replaceCatalogue(SampleCatalogue.load())
                storedRoutes = try await store.routes()
            }
            routes = storedRoutes
            failure = nil
        } catch {
            failure = "The local sample catalogue could not be opened. \(error.localizedDescription)"
        }
        isLoading = false
    }
}
