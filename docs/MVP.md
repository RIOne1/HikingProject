# First Release MVP

**Status:** agreed specification; implementation and acceptance evidence are pending.

**Decision baseline:** 13 November 2026.

**Authority:** this English document is authoritative. [中文镜像](MVP.zh-CN.md) must retain the same requirement IDs, scope and acceptance conditions. Update both in the same PR when meaning changes.

Use [CONTRIBUTING.md](../CONTRIBUTING.md) for collaboration and [SECURITY.md](../SECURITY.md) for security and private-data handling. Research findings inform this specification but do not override its agreed scope.

## 1. Product goal and users

Deliver an iPhone app that a beginner-to-intermediate hiker can use to prepare for, follow and record a half-day or full-day hike in New Zealand. The first release must complete one useful workflow reliably:

**Choose or import a route → inspect it → prepare its offline map → start a hike → see location and off-route warnings → finish → inspect and export the recorded track.**

Begin with 20–30 curated routes in areas convenient for the team to test. Verify the sources and information for every listed route, and field-test representative routes. Record source verification and a team's actual walk separately; do not label every route as field-tested. A route line or a past walk does not prove current access or conditions.

The project is also intended to develop the owner's SQL skills through real schema, query, index, transaction and migration work. This learning goal must support product correctness.

## 2. Delivery and cost boundaries

- The consumer product direction is iPhone only, on iOS 18 or later. A React/TypeScript/Vite web companion is approved for internal team route/content work; it does not add consumer web parity, a backend or GL JS. Other consumer client platforms remain outside the agreed direction. Multi-day and advanced hiking and other countries are not first-release commitments.
- No account is required. Trip history belongs in local storage. The first release has no application backend, accounts service or cloud database.
- Current development must remain free. Do not activate paid services, paid CI or paid upgrades. A trial ending or a quota being exhausted means pausing the affected service, not authorizing payment.
- Mapbox Maps SDK for iOS is a **conditional selection**. Verify its actual no-card trial, offline behaviour and integration before relying on them. A free trial is not a permanent free production entitlement.
- The post-deployment service budget has a hard NZ$50/month limit. Mapbox's ordinary billing has no automatic spending cap; the production cost arrangement remains a release blocker until resolved. Do not silently weaken this constraint.
- Apple Developer Program membership is a later, separately budgeted expense for paid distribution capabilities. The free-development milestone does not include TestFlight or App Store publication.
- Validate user demand before selecting monetization. Do not add payments or subscriptions to the first-release implementation without a scope decision.

## 3. Must-have requirements

### MVP-01 — Curated route discovery and details

Browse the initial route catalogue and inspect a route before selecting it. Show its geometry, name, source and available planning information, including relevant known access notes. Show source/update or retrieval information; represent missing facts as unknown instead of inventing them. Catalogue content must retain stable route IDs, attribution, verification status and a version.

**Acceptance:** the initial 20–30 entries have recorded source checks; route details match the selected entry; bundled content remains readable without a network connection; claims of field testing have their own evidence. Map data and route-status information are not treated as interchangeable.

### MVP-02 — GPX route import

Import valid GPX routes or tracks into local storage. User-imported routes must support the same core preview, surrounding-map download, following, recording and off-route-warning workflow as curated routes, within documented and tested format, size and map-coverage limits. Label them as user-imported and not team-verified.

**Acceptance:** supported GPX elements, multiple-track/segment handling and import limits are documented; coordinates and timestamps are validated; malformed or unsupported input produces a useful error without corrupting existing data. Preserve meaningful segment boundaries rather than silently connecting gaps. Import does not create a route-planning or rerouting feature.

### MVP-03 — Offline map preparation

Before departure, let the user download the selected route's surrounding map and required style resources. Show the intended coverage, download progress, failure state and readiness. Mark a pack ready only after the required resources have been verified. Allow retry and removal of map downloads without deleting routes or trips.

**Acceptance:** after a completed download, airplane-mode cold launch can display the selected route, available map labels/icons, current location when available, and recorded track. Interrupted or incomplete downloads never appear ready. Coverage edges, resource limits and actual package sizes are tested and documented. Missing maps are identified clearly while existing route and trip data remain available.

### MVP-04 — Location and recording state

Show the current location and a clear recording state. Show reduced accuracy, stale location or an interruption when relevant. Request permissions when needed and explain a refusal's effect. Browsing, local history and file exchange must remain available when recording permission is denied.

**Acceptance:** permission-denied, approximate/reduced-accuracy, stale-location and resumed-location scenarios have visible, understandable states. Do not present an old location as a fresh fix or use interpolation to conceal recording gaps.

### MVP-05 — Local foreground and background recording

Let the user start and finish a hike. Record ordered track points, timestamps and relevant quality information locally. Recording must be independent of the map view's lifecycle and support normal locked-screen/background use under the platform's permitted behaviour. Persist points deliberately and surface storage failures.

**Acceptance:** real-device evidence covers normal screen lock, foreground/background transitions, day-hike-duration use and interrupted-session recovery. Preserve committed points and identify an unfinished trip on reopening. Record time, battery use and gaps. Do not promise uninterrupted recording after user force-quit or device restart. Device coverage, duration and quantitative pass thresholds must be agreed in the validation plan before this requirement is marked passed.

### MVP-06 — Off-route warnings, including lock screen

Compare suitable recent location samples with the selected route locally. Provide in-app warnings and, when authorized, local notifications during locked-screen use. Filter poor-quality fixes and repeated alerts; document and validate the thresholds. Notification permission being disabled must have an explicit visible effect.

**Acceptance:** controlled on-route, off-route, poor-accuracy and repeated-alert scenarios are tested, including locked-screen delivery on a real device. Warnings do not depend on a push server or online routing request. Uncertain location must not automatically become a confident off-route claim.

### MVP-07 — Recorded path for returning

Display the path already recorded so the user can inspect their previous route and use it to assist returning along it.

**Acceptance:** saved segments and gaps are represented faithfully and remain visible offline. This feature does not calculate a new return route, establish that a path is safe, or provide emergency/rescue services.

### MVP-08 — Local history and GPX export

Keep completed trips available for later inspection and user-initiated GPX export. Derived statistics must use defined, tested calculations and must not fabricate absent measurements. Export must preserve the supported coordinates, timestamps and segment semantics.

**Acceptance:** completed trips survive app relaunch; exported files can be parsed by an independent GPX reader and compared with the saved data. Cancelling export does not change the trip. GPX export is route/track portability, **not a complete application backup**; full backup and restore are deferred.

### MVP-09 — Durable SQL data and migrations

Use SQLite with GRDB as the business database. Use parameterized SQL, appropriate constraints, transactional writes and versioned migrations. Keep important SQL inspectable for review and learning. Use stable business IDs independent of Mapbox identifiers and caches.

**Acceptance:** demonstrate relevant write-failure and interruption handling, query/index behaviour, and migration from an earlier test schema with representative data. A failed import or update must not leave partial user data. Removing or replacing a map cache must not remove trip history. Explain important SQL and any schema changes in the PR.

### MVP-10 — Versioned route content

Bundle the initial catalogue as GeoJSON geometry plus JSON metadata. Design a versioned static-content update path using URLSession, retaining the last usable content until a replacement is verified. During free development, exercise updates with local fixtures or a local test endpoint; decide and validate static hosting before public distribution. Development acceptance does not require deploying a remote host; hosted updates are a public-release gate.

**Acceptance:** unsupported versions, invalid content, interrupted downloads and incompatible updates are rejected safely. Source IDs, attribution and timestamps remain traceable. Define how closure information is checked and how stale or unavailable information is presented; do not claim real-time status without a verified source and update mechanism.

### MVP-11 — Privacy, permissions and untrusted files

Keep the application-owned trip history local and private by default. Sharing/export must be deliberate. Apply [SECURITY.md](../SECURITY.md) to GPX/JSON parsing, logs, screenshots, tokens, dependencies and AI inputs. Review Mapbox and other actual SDK network/telemetry behaviour before making privacy statements.

**Acceptance:** permission-denied paths are tested; personal tracks, production tokens and local databases do not appear in repository fixtures or shared logs. Test imports with synthetic or appropriately authorized data. Do not equate local trip storage with a claim that the whole app or its SDKs send no data.

### MVP-12 — Usable and testable end-to-end flow

The owner leads real-device tests of the complete workflow on representative routes, including a supported imported GPX route. Important controls and status messages must remain readable and operable; check text sizing and accessibility labels for the main actions.

**Acceptance:** a recorded validation run covers route choice/import, offline preparation, recording, background use, warning behaviour, finish, history and export. Document the device, OS, build/commit, route or fixture, conditions, result and remaining limitations. An emulator-only run is insufficient evidence for outdoor/background reliability.

## 4. Technical baseline

| Area | Agreed approach |
| --- | --- |
| Client | Swift, SwiftUI, iOS 18+; UIKit integration where required |
| Internal content tool | React + TypeScript + Vite, local-first team workspace; npm lockfile, Vitest/Testing Library and ESLint |
| Maps | Mapbox Maps SDK for iOS; its managed offline cache stays separate from business data |
| Location and alerts | Core Location and local notifications; recording independent of map rendering |
| Persistence | SQLite + GRDB, explicit parameterized SQL and schema migrations |
| Architecture | One modular app, lightweight MVVM, Swift Concurrency, clear data-access boundaries |
| Dependencies | Swift Package Manager; stable versions locked after compatibility checks |
| Content and exchange | GeoJSON + JSON catalogue; GPX import/export using Foundation XML processing |
| Downloads | URLSession with validation and retention of the previous usable version |
| Verification | Swift Testing for logic/data, XCTest for UI, Xcode diagnostics and real-device testing |
| Services | No first-release application backend, account service or cloud database |

Keep route, recording and persistence logic independent of vendor rendering types where practical. Do not build a universal abstraction framework in anticipation of unspecified future products. Any later technology change must identify the requirement, data-migration impact, cost and verification plan.

## 5. Explicitly deferred

- Arbitrary start/end route planning, mid-hike replanning and offline automatic rerouting.
- User-published route communities, reviews, social feeds, following and social interaction.
- Full application backup/restore, cloud backup and multi-device synchronization.
- Live location sharing and associated network services.
- Mapbox GL JS browser tools.
- Multi-day/advanced hiking, global catalogue coverage and other unapproved feature expansion.

These are future candidates, not first-release promises. Additional consumer client platforms are outside the agreed direction, not scheduled later work. The internal React tool above supports team content work only. A scope change needs a reviewed update to both MVP language versions before it is treated as required work.

## 6. Verification and Definition of Done

### Development acceptance

- The implemented scope satisfies MVP-01 through MVP-12, with traceable evidence and no unresolved blocking defects in the core workflow.
- Select representative routes, supported devices, a day-hike recording duration, alert thresholds and performance/storage limits **before** claiming their tests pass. Record the choices and reasons; do not invent numerical results or assume SDK documentation proves the app works.
- Verify Mapbox trial access and offline behaviour, SDK/toolchain compatibility, locked-screen recording, location-quality handling, notification delivery, GPX interoperability and database migrations.
- Record each check as **Passed**, **Failed**, **Not run** with a reason, or **Not applicable** with a justification. Unrun required acceptance tests remain blockers.
- Complete non-author human review under [CONTRIBUTING.md](../CONTRIBUTING.md). Documentation completion or AI review alone is not product acceptance.

### Public-release acceptance

In addition to development acceptance:

- Resolve Mapbox's production cost arrangement while retaining the NZ$50/month hard limit; verify static hosting costs and content-update operation.
- Complete required Apple enrollment/distribution steps with the separately approved budget, and check the actual App Store privacy, permission and submission requirements.
- Verify all catalogue sources/attributions, record representative field-test evidence and state freshness limitations accurately.
- Configure and test a real confidential security-reporting channel as required by [SECURITY.md](../SECURITY.md).
- Configure and verify the GitHub review protections described in [CONTRIBUTING.md](../CONTRIBUTING.md); file-based policy alone does not enforce them.
- Verify privacy disclosures against the implemented app and actual SDK behaviour.

**Current state:** the repository has iOS and internal React foundations, a shared synthetic metadata catalogue, SQL storage and automated tests. CI covers documentation, contribution metadata, Web and portable Swift/data checks; local Mac/Xcode covers iOS build/UI verification. The [development guide](guides/DEVELOPMENT.md) and [foundation validation record](guides/FOUNDATION-VALIDATION.md) distinguish actual evidence from remaining checks. The sample catalogue is not the 20–30 verified routes, and no MVP requirement is declared accepted by this bootstrap. Offline maps, location/recording, warnings, GPX, real content and release gates remain pending.

## 7. Evidence and maintenance

- Before repository changes, create or confirm a tracking Issue under [CONTRIBUTING.md](../CONTRIBUTING.md); include its number in the task branch and link the same Issue in every PR. Also link PRs and validation records to the affected `MVP-XX` IDs; requirement IDs do not replace Issue numbers.
- Keep the English and Chinese requirements aligned in the same PR. Where a translation is ambiguous, resolve it against this English version and correct the mirror.
- The [archived research](research/2026-11-06-user-feedback/Hiking_App_User_Feedback_Research_ZH_2026-11-06.pdf) is a dated desktop study, not completed user validation or a specification of implemented features.
- Platform references: [Mapbox offline maps](https://docs.mapbox.com/ios/maps/guides/offline/), [Mapbox trial](https://docs.mapbox.com/accounts/guides/signup/), [Mapbox billing](https://docs.mapbox.com/accounts/guides/invoices/), [Apple background location](https://developer.apple.com/documentation/corelocation/handling-location-updates-in-the-background), [GRDB](https://github.com/groue/GRDB.swift).
