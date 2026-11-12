# Foundation validation record

Recorded **13 November 2026 (Pacific/Auckland)** for [Issue #7](https://github.com/RIOne1/HikingProject/issues/7), branch `build/7-mobile-web-foundation`. These results apply to the bootstrap scope and synthetic fixtures. They do not mark any MVP requirement accepted. Commands below ran from the repository root unless stated otherwise; logs and Xcode results are local ignored files under `tmp/foundation/` and `tmp/review8/`.

## Initial local evidence

| Check | Environment | Result |
| --- | --- | --- |
| `swift test --scratch-path tmp/foundation/swift-build --disable-automatic-resolution --jobs 2` | macOS, Swift 6.4.2 | Passed: 8 Swift Testing functions, including 4 numeric-validation cases; persistence/reopen, parameterized SQL and write-failure rollback |
| `npm ci` followed by `npm run check:web` | Node 24.20.0, npm 11.19.0 | Passed: ESLint, 13 Vitest tests including JSON Schema checks, TypeScript checking and Vite production build |
| npm installation audit | Same locked dependency graph | 0 known vulnerabilities reported after the documented minimatch override; this is not a complete dependency security review |
| `xcodebuild -resolvePackageDependencies -project apps/mobile/HikingProject.xcodeproj -scheme HikingProject` | Xcode 27.2 | Passed: GRDB 7.12.0, Mapbox 11.34.2 and transitive dependencies resolved without entering a map credential |
| `xcodebuild test -project apps/mobile/HikingProject.xcodeproj -scheme HikingProject -destination 'platform=iOS Simulator,id=2A18306D-5CB2-4976-8FB2-B3913DEB00D4' -derivedDataPath tmp/foundation/DerivedData -resultBundlePath tmp/foundation/ios-tests-2.xcresult CODE_SIGNING_ALLOWED=NO` | iPhone 18 Pro simulator, iOS 27.2 | Passed: app compiled and 1 XCTest UI scenario browsed the sample, opened details, checked tokenless map state/distance and relaunched |
| Browser scenario: catalogue → search `ridge` → inspect → close → unmatched search → clear | Chrome, local Vite production preview | Passed; metadata, selection and empty state matched the fixture. Development-mode catalogue also displayed after restarting Vite following dependency installation |
| `python3 scripts/ci/check_docs.py`; `git diff --cached --check`; XcodeGen regeneration comparison; YAML parsing | Local working tree | Passed: 13 Markdown files, bilingual structure/links, whitespace, stable generated project and valid workflow YAML |
| `python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v` | Python 3.14 | Passed: 15 governance/document-validator regression tests |

The first UI run exposed an incorrect assumption that SwiftUI `LabeledContent` exposes its value separately. The final test identifies the combined accessibility element and still asserts the actual distance. No production assertion was removed to obtain a pass. Restart a running Vite server after dependency replacement; an already-running process can retain stale optimized modules.

The root `Package.resolved` records the resolved graph used here, including Mapbox's transitive versions. The portable package only depends on GRDB; its locked test command does not compile the map SDK. Both Swift and npm lockfiles belong in review.

## PR #8 review follow-up

The review reproduced and corrected three inconsistencies:

- XcodeGen's default plist version was `1.0` despite the project setting `0.1.0`. The plist now references the marketing/build settings; the rebuilt app reports `0.1.0` / `1`.
- Foundation trimming and JavaScript trimming disagreed on Unicode NEL/BOM-only names and attribution. Swift, TypeScript and JSON Schema now use the same explicit nonblank rule. Regression tests failed before the fix (Swift accepted BOM; Web/schema accepted NEL) and passed afterward, while preserving meaningful Māori/Chinese text.
- In an isolated checkout of the pre-fix revision, plain `swift package resolve` removed Mapbox's pins from the combined lockfile. `swift package resolve --force-resolved-versions` followed by `xcodebuild -resolvePackageDependencies -onlyUsePackageVersionsFromResolvedFile -project apps/mobile/HikingProject.xcodeproj -scheme HikingProject` preserved it byte-for-byte. The [Mobile guide](MOBILE.md#build-and-test) now uses locked resolution and builds.

| Follow-up check | Result |
| --- | --- |
| `npm ci` then `npm run check:web` | Passed on Node 24.20.0 / npm 11.19.0: ESLint, 19 Vitest tests, TypeScript and production build; install audit reported 0 known vulnerabilities |
| `swift test --scratch-path tmp/foundation/swift-build --disable-automatic-resolution --jobs 2` | Passed on local Swift 6.4.2: 10 Swift Testing functions, including 10 blank-text and 4 numeric cases, SQL binding, persistence and rollback |
| `xcodebuild test -project apps/mobile/HikingProject.xcodeproj -scheme HikingProject -onlyUsePackageVersionsFromResolvedFile -destination 'platform=iOS Simulator,id=2A18306D-5CB2-4976-8FB2-B3913DEB00D4' -derivedDataPath tmp/foundation/DerivedData -resultBundlePath tmp/review8/ios-tests.xcresult CODE_SIGNING_ALLOWED=NO` | Passed on Xcode 27.2 / iPhone 18 Pro / iOS 27.2: build and the tokenless browse/detail/relaunch UI test; built plist inspected with Python `plistlib`, version `0.1.0` / `1`; root lockfile unchanged |

The new regression cases are discovered by the existing Web/Swift commands in `Documentation integrity`; no extra workflow or hosted runner is needed. No screen layout changed, so the initial sanitized screenshots below still describe the foundation UI. Current-revision Linux results are linked in the PR; local results do not substitute for its required checks.

## CI and remaining gates

The workflow runs Web and portable Swift tests inside the existing required `Documentation integrity` check, alongside the unchanged `Contribution policy` check. After the owner updated the runner image, [run 43209940168, attempt 2](https://github.com/RIOne1/HikingProject/actions/runs/43209940168/attempts/2) passed both checks on 13 November 2026 (Pacific/Auckland), for commit `5b384ac9299cc89766562242527ccba126b2b350`.

The `HikingProject-PC` logs confirm Node 24.20.0, 13 passing Web tests with lint/typecheck/build, native-prerequisite and Swift setup success, and Swift 6.2.1 targeting `x86_64-unknown-linux-gnu`. The exact command `swift test --scratch-path .build/ci --disable-automatic-resolution --jobs 2` built the portable package and passed all 8 Swift Testing functions, including the 4 numeric-validation cases, SQLite persistence, SQL binding and failed-write rollback. These tests ran rather than being skipped.

The earlier missing-tool failure is resolved. Keep the [documented image prerequisites](CI.md#ubuntu-2404-image-preparation) when rebuilding the runner. This evidence records the verified revision; the PR's checks track subsequent commits, which must also pass before merge. Human inspection and non-author approval remain merge gates. The owner's follow-up instruction authorizes marking PR #8 ready once its current checks pass; it does not authorize merging.

Not run / not implemented: real-device installation, iOS 18 runtime coverage, token-enabled map rendering, offline packs, SDK telemetry/privacy behaviour, location permissions, foreground/background recording, notification delivery, battery endurance, GPX import/export, genuine route geometry/provenance, earlier-version schema upgrades, abrupt process interruption and App Store distribution. These remain their feature/product/release gates, not claims established by a sample catalogue. No paid service, Apple enrollment, Mapbox account activation, hosted runner or deployment was performed.

## Screenshots

Only synthetic fixture content is shown.

![Internal React catalogue](images/web-foundation.png)

![iOS sample catalogue](images/mobile-foundation.png)
