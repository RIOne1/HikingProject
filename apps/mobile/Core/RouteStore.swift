import GRDB

/// A catalogue store, separate from map caches and future recorded-trip storage.
public final class RouteStore: Sendable {
    private let database: DatabaseQueue

    public convenience init(path: String) throws {
        try self.init(database: DatabaseQueue(path: path))
    }

    init(database: DatabaseQueue) throws {
        self.database = database
        var migrator = DatabaseMigrator()
        migrator.registerMigration("v1_catalogue") { db in
            // IDs belong to our catalogue, never to a map provider's cache.
            try db.execute(sql: """
                CREATE TABLE routes (
                    id TEXT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'moderate')),
                    distanceMetres INTEGER NOT NULL CHECK (distanceMetres BETWEEN 1 AND 100000),
                    estimatedMinutes INTEGER NOT NULL CHECK (estimatedMinutes BETWEEN 1 AND 1440),
                    startLatitude REAL NOT NULL CHECK (startLatitude BETWEEN -90 AND 90),
                    startLongitude REAL NOT NULL CHECK (startLongitude BETWEEN -180 AND 180),
                    sourceKind TEXT NOT NULL CHECK (sourceKind = 'synthetic'),
                    attribution TEXT NOT NULL
                )
                """)
        }
        try migrator.migrate(database)
    }

    public func routes() async throws -> [RouteSummary] {
        try await database.read { db in
            try Row.fetchAll(db, sql: "SELECT * FROM routes ORDER BY id").map { row in
                guard let difficulty = RouteSummary.Difficulty(rawValue: row["difficulty"]) else {
                    throw Catalogue.ValidationError.invalidRoute(row["id"])
                }
                return RouteSummary(
                    id: row["id"], name: row["name"], difficulty: difficulty,
                    distanceMetres: row["distanceMetres"], estimatedMinutes: row["estimatedMinutes"],
                    startLatitude: row["startLatitude"], startLongitude: row["startLongitude"],
                    sourceKind: row["sourceKind"], attribution: row["attribution"]
                )
            }
        }
    }

    public func replaceCatalogue(_ catalogue: Catalogue) async throws {
        try catalogue.validate()
        // GRDB's write transaction rolls back deletion and all inserts together
        // if a constraint or disk write fails. Never leave a partial catalogue.
        try await database.write { db in
            try db.execute(sql: "DELETE FROM routes")
            for route in catalogue.routes {
                try db.execute(sql: """
                    INSERT INTO routes
                    (id, name, difficulty, distanceMetres, estimatedMinutes,
                     startLatitude, startLongitude, sourceKind, attribution)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, arguments: [route.id, route.name, route.difficulty.rawValue,
                        route.distanceMetres, route.estimatedMinutes, route.startLatitude,
                        route.startLongitude, route.sourceKind, route.attribution])
            }
        }
    }
}
