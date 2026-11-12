import Foundation

public struct RouteSummary: Codable, Equatable, Identifiable, Sendable {
    public enum Difficulty: String, Codable, Sendable { case easy, moderate }
    public let id: String
    public let name: String
    public let difficulty: Difficulty
    public let distanceMetres: Int
    public let estimatedMinutes: Int
    public let startLatitude: Double
    public let startLongitude: Double
    public let sourceKind: String
    public let attribution: String
}

public struct Catalogue: Codable, Equatable, Sendable {
    public let schemaVersion: Int
    public let routes: [RouteSummary]

    public enum ValidationError: Error, Equatable {
        case unsupportedVersion(Int)
        case tooManyRoutes
        case invalidRoute(String)
        case duplicateID(String)
    }

    public static func decode(_ data: Data) throws -> Catalogue {
        let catalogue = try JSONDecoder().decode(Catalogue.self, from: data)
        try catalogue.validate()
        return catalogue
    }

    public func validate() throws {
        guard schemaVersion == 1 else { throw ValidationError.unsupportedVersion(schemaVersion) }
        guard routes.count <= 100 else { throw ValidationError.tooManyRoutes }
        var ids = Set<String>()
        for route in routes {
            guard route.id.range(of: "^[a-z0-9]+(?:-[a-z0-9]+)*$", options: .regularExpression) != nil,
                  !route.name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  !route.attribution.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  (1...100_000).contains(route.distanceMetres),
                  (1...1440).contains(route.estimatedMinutes),
                  route.startLatitude.isFinite, (-90...90).contains(route.startLatitude),
                  route.startLongitude.isFinite, (-180...180).contains(route.startLongitude),
                  route.sourceKind == "synthetic" else {
                throw ValidationError.invalidRoute(route.id)
            }
            guard ids.insert(route.id).inserted else { throw ValidationError.duplicateID(route.id) }
        }
    }
}
