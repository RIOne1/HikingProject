import Foundation
import Testing
@testable import HikingCore
import HikingSampleData

@Test func sharedFixtureLoadsWithExplicitUnits() throws {
    let catalogue = try SampleCatalogue.load()
    #expect(catalogue.schemaVersion == 1)
    #expect(catalogue.routes.count == 2)
    #expect(catalogue.routes[0].distanceMetres == 2400)
    #expect(catalogue.routes.allSatisfy { $0.sourceKind == "synthetic" })
}

func modifiedFixture(_ edit: (inout [String: Any]) -> Void) throws -> Data {
    var json = try #require(JSONSerialization.jsonObject(with: SampleCatalogue.data()) as? [String: Any])
    edit(&json)
    return try JSONSerialization.data(withJSONObject: json)
}

@Test func unsupportedCatalogueVersionIsRejected() throws {
    let data = try modifiedFixture { $0["schemaVersion"] = 2 }
    #expect(throws: Catalogue.ValidationError.unsupportedVersion(2)) { try Catalogue.decode(data) }
}

@Test func duplicateIDsAreRejected() throws {
    let data = try modifiedFixture { json in
        let routes = json["routes"] as! [[String: Any]]
        json["routes"] = [routes[0], routes[0]]
    }
    #expect(throws: Catalogue.ValidationError.duplicateID("sample-coastal-loop")) { try Catalogue.decode(data) }
}

@Test(arguments: ["startLatitude", "startLongitude", "distanceMetres", "estimatedMinutes"])
func invalidNumericFieldsAreRejected(field: String) throws {
    let data = try modifiedFixture { json in
        var routes = json["routes"] as! [[String: Any]]
        routes[0][field] = field == "startLatitude" || field == "startLongitude" ? 999 : -1
        json["routes"] = routes
    }
    #expect(throws: Catalogue.ValidationError.invalidRoute("sample-coastal-loop")) { try Catalogue.decode(data) }
}

@Test func productionContentCannotMasqueradeAsFoundationData() throws {
    let data = try modifiedFixture { json in
        var routes = json["routes"] as! [[String: Any]]
        routes[0]["sourceKind"] = "verified"
        json["routes"] = routes
    }
    #expect(throws: Catalogue.ValidationError.invalidRoute("sample-coastal-loop")) { try Catalogue.decode(data) }
}
