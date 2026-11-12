import XCTest

final class CatalogueUITests: XCTestCase {
    @MainActor
    func testBrowsePersistedSampleCatalogueWithoutMapToken() {
        let app = XCUIApplication()
        app.launchArguments = ["--tokenless-preview"]
        app.launch()
        XCTAssertTrue(app.staticTexts["sample-data-notice"].waitForExistence(timeout: 10))
        let route = app.buttons["route-sample-coastal-loop"]
        XCTAssertTrue(route.waitForExistence(timeout: 5))
        route.tap()
        XCTAssertTrue(app.staticTexts["Map preview not configured"].waitForExistence(timeout: 5))
        // LabeledContent exposes its label and value as one accessibility element.
        let distance = app.staticTexts["route-distance"]
        XCTAssertTrue(distance.exists)
        XCTAssertTrue(distance.label.contains("2400 metres"), distance.label)
        app.terminate()
        app.launch()
        XCTAssertTrue(app.buttons["route-sample-coastal-loop"].waitForExistence(timeout: 10))
    }
}
