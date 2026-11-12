# Mobile foundation guide

## Project and boundaries

Open [HikingProject.xcodeproj](../../apps/mobile/HikingProject.xcodeproj/) and select scheme **HikingProject**. Minimum deployment is iOS 18, iPhone only. The observed local baseline is Xcode 27.2 / Swift 6.4.2; the root Swift package uses tools 6.1 and Swift 6 language mode. Linux CI uses Swift 6.2.1 for the portable core. Other toolchains and iOS versions need their own evidence.

| Path | Responsibility |
| --- | --- |
| `apps/mobile/App/` | SwiftUI screens, observable catalogue model, app storage location and Mapbox adapter |
| `apps/mobile/Core/` | Foundation-only catalogue model/validation and GRDB store; no Mapbox or UIKit dependency |
| `apps/mobile/CoreTests/` | Swift Testing for validation, persisted data, SQL binding and rollback |
| `apps/mobile/UITests/` | XCTest browse/detail/relaunch smoke test |
| `shared/` | Single sample catalogue resource and JSON contract shared with React |
| `apps/mobile/project.yml` | XcodeGen project source; generated `.xcodeproj`, shared scheme and plist are committed |

Core Location is an Apple framework used here only for the map camera coordinate. There is no location request, background mode, recording service or notification permission in the foundation. Add capabilities and permission explanations with the feature that needs them and test refusal paths. Foundation XML processing and URLSession need no third-party package; GPX and content downloading remain future implementation.

The expanded MVP also adds online predeparture route combination, private-plan sync and evidence submission. None is implemented here, and no Supabase SDK/Auth flow is installed. The build commands below continue to verify the existing foundation, not these future features.

## Build and test

From the repository root, resolve and test the portable core:

```bash
swift package resolve --force-resolved-versions
swift test --disable-automatic-resolution --jobs 2
```

Use the committed root `Package.resolved` for both commands and the app graph. With this project/toolchain, Xcode records Mapbox's transitive pins there alongside GRDB; the portable package itself only depends on GRDB. A plain `swift package resolve` removes the app-only pins, so use the locked commands below and review any lockfile change as a dependency change. Resolve the app's package graph and list available simulators:

```bash
xcodebuild -resolvePackageDependencies -onlyUsePackageVersionsFromResolvedFile \
  -project apps/mobile/HikingProject.xcodeproj -scheme HikingProject
xcrun simctl list devices available
```

Set `IOS_SIMULATOR_ID` to an actual available iPhone simulator's UUID, then run:

```bash
xcodebuild test \
  -project apps/mobile/HikingProject.xcodeproj \
  -scheme HikingProject \
  -onlyUsePackageVersionsFromResolvedFile \
  -destination "platform=iOS Simulator,id=$IOS_SIMULATOR_ID" \
  -derivedDataPath tmp/mobile/DerivedData \
  CODE_SIGNING_ALLOWED=NO
```

This builds the app and runs XCTest UI tests. It does **not** run the root Swift Testing suite; run both commands. Use `xcodebuild build` with the same project, scheme and destination for a build-only check. Simulator work does not require paid Apple enrollment. Real-device signing is local and is not established by simulator success. Never commit a personal signing team or identity.

## Mapbox and local configuration

Mapbox Maps SDK **11.34.2** is pinned through SPM. Its dependency graph and binaries resolved without a Mapbox credential during foundation verification. This is evidence of dependency access, not proof of ongoing free map usage, offline support or privacy behaviour. See [Mapbox installation](https://docs.mapbox.com/ios/maps/guides/install/) and the MVP's technical/cost gates.

By default `MAPBOX_ACCESS_TOKEN` is empty. The app does not instantiate a Mapbox view without a `pk.` token and displays an explanatory placeholder while retaining the catalogue. Do not create/activate a paid account for this task. Only after permitted no-card access and applicable limits are verified, copy `apps/mobile/Config/Local.example.xcconfig` to `apps/mobile/Config/Local.xcconfig` from the repository root and set an authorized public token. That local file is ignored. Never put a secret token or actual public token in committed source, screenshots or PRs. A public app token will be embedded in a configured build and is not a server secret.

The optional preview shows the area around a **synthetic start point**, not a route line. Map attribution controls are left to the SDK. UI smoke tests pass `--tokenless-preview` so tests do not consume map usage even on a locally configured machine. Runtime map rendering, telemetry, offline packs and production costs remain unverified.

## Editing project structure

Use XcodeGen **2.46.0** to regenerate after changing targets, sources or package configuration. Edit `project.yml` first, not only the generated project:

```bash
xcodegen generate --spec apps/mobile/project.yml
```

Use the official [XcodeGen release](https://github.com/yonaskolb/XcodeGen/releases/tag/2.46.0). The `xcodegen.zip` used for this foundation has SHA-256 `4d9e34b62172d645eed6457cac13fc222569974098ef4ee9c3368bedf0196806`; verify a download before running it. A locally unpacked `bin/xcodegen` works without global installation. Commit the generated project/plist/scheme and dependency lockfile together. Do not commit `xcuserdata`, DerivedData or `Local.xcconfig`.

The generated app plist binds its version fields to `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` in `project.yml` (currently `0.1.0` / `1`). Change those settings and regenerate when versioning a build; do not edit a second literal version in the plist.

## SQL and future features

`CatalogueModel` selects the app's Application Support location and seeds `foundation.sqlite` only when the catalogue is empty. `RouteStore` owns migrations and SQL; the Mapbox adapter never owns the database. See [data guide](DATA.md) before changing schema or catalogue semantics. Add recording models and point storage only with their real requirements, tests and failure/recovery design; do not treat this sample catalogue table as a trip-history schema.

## Planned hiking workflow

- While online and before departure, combine a selected route with nearby routes using the checked network. Preserve all selected parts, direction/order and repetitions; preview and confirm connectors. Reject disconnected/closed combinations instead of shortening them. Mobile does not need Web's precision editor.
- Fetch or save the exact private plan revision and prepare a complete local snapshot plus map pack. Geometry must not change silently after server/network edits. Show last-known status; a confirmed closure blocks starting new planned navigation, but must not forcibly stop an ongoing hike or independent recording.
- Keep saved-line navigation/progress and locally calculated off-route alerts independent of authentication and online routing. Guests and expired sessions retain existing offline use. Mid-hike/offline combination, automatic rerouting and turn-by-turn voice guidance remain deferred.
- Preserve private unverified GPX import/navigation and GPX export with a local revision and original segments/gaps; do not fabricate network IDs or snap imports to fit the planning contract. Imported files are not sufficient publication evidence. Store raw recordings locally; deliberate review evidence must support the submitted route, including connectors/repeated traversals, while excluding unrelated locations.
- Implement account-scoped caches/session handling without cross-user exposure or loss of recordings on logout/expiry. Explicit account deletion is a separate operation: define the requesting user's data cleanup and distinguish unrelated guest-local records. Withdrawal of another user's route must preserve this user's independent recording and active hike. Validate cleanup timing before external users.

Use MVP-02 through MVP-12 and MVP-14 through MVP-20 for complete conditions. Add relevant SQL/logic tests and local Xcode checks with implementation; real-device evidence is still required for offline/background/lock-screen/battery claims. See [Backend](BACKEND.md) for planned identity/data boundaries and [CI](CI.md) for what the Linux runner can actually verify.
