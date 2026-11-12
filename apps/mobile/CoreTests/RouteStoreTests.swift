import Foundation
import GRDB
import Testing
@testable import HikingCore
import HikingSampleData

@Test func catalogueSurvivesReopenAndRepeatedMigration() async throws {
    let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
    try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    defer { try? FileManager.default.removeItem(at: directory) }
    let path = directory.appendingPathComponent("routes.sqlite").path
    let catalogue = try SampleCatalogue.load()
    do {
        let store = try RouteStore(path: path)
        try await store.replaceCatalogue(catalogue)
    }
    let reopened = try RouteStore(path: path)
    #expect(try await reopened.routes() == catalogue.routes)
}

@Test func writeFailureRollsBackTheWholeReplacement() async throws {
    let database = try DatabaseQueue()
    let store = try RouteStore(database: database)
    let catalogue = try SampleCatalogue.load()
    let original = Catalogue(schemaVersion: 1, routes: [catalogue.routes[0]])
    try await store.replaceCatalogue(original)
    // Fail the second valid insert after DELETE and the first insert have run.
    try await database.write { db in
        try db.execute(sql: """
            CREATE TRIGGER simulated_write_failure BEFORE INSERT ON routes
            WHEN NEW.id = 'sample-ridge-walk'
            BEGIN SELECT RAISE(ABORT, 'simulated write failure'); END
            """)
    }
    await #expect(throws: (any Error).self) { try await store.replaceCatalogue(catalogue) }
    #expect(try await store.routes() == original.routes)
}

@Test func routeNamesAreBoundAsSQLValues() async throws {
    let name = "Robert'); DROP TABLE routes;--"
    let data = try modifiedFixture { json in
        var routes = json["routes"] as! [[String: Any]]
        routes[0]["name"] = name
        json["routes"] = routes
    }
    let store = try RouteStore(database: DatabaseQueue())
    try await store.replaceCatalogue(Catalogue.decode(data))
    #expect(try await store.routes().first?.name == name)
    #expect(try await store.routes().count == 2)
}
