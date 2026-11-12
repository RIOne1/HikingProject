import Foundation
import HikingCore

public enum SampleCatalogue {
    public static func data() throws -> Data {
        guard let url = Bundle.module.url(forResource: "catalogue.sample", withExtension: "json", subdirectory: "fixtures") else {
            throw CocoaError(.fileNoSuchFile)
        }
        return try Data(contentsOf: url)
    }

    public static func load() throws -> Catalogue {
        try Catalogue.decode(data())
    }
}
