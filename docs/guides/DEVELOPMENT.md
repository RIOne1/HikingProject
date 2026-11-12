# Team development guide

Start here after reading [CONTRIBUTING](../../CONTRIBUTING.md). This foundation supports parallel mobile and internal web work; it is not MVP acceptance. The [English MVP](../MVP.md) remains the product authority.

## Workspace and ownership

| Workstream | Owns | Start with |
| --- | --- | --- |
| Mobile | SwiftUI screens, app composition, iOS adapters and device evidence in `apps/mobile/` | [Mobile guide](MOBILE.md) |
| Web/content | React route/content workspace in `apps/web/`; no consumer web app or publishing service | [Web guide](WEB.md) |
| Shared data | `shared/`, portable Swift core, catalogue contract and SQL migration decisions; coordinate with both clients | [Data guide](DATA.md) |

For a two-person team, the mobile owner can also own shared data while the other member owns web/content. A third member can take data fixtures and validation. Assign actual people through Issues; these are work boundaries, not automatic GitHub permissions or CODEOWNERS rules. Keep one primary Issue per branch/PR and obtain non-author human review under CONTRIBUTING.

Changes to the shared contract should reach agreement on fields, units, versioning and failure behaviour before either client depends on them. Include both decoders, fixtures and relevant tests in the same PR when the contract changes. Avoid moving mobile business logic into Mapbox views or introducing a shared abstraction framework.

## First local run

Run commands from the repository root. Initial npm/SPM resolution requires internet access; the sample catalogue itself requires no account or token.

```bash
npm ci
npm run dev:web
```

Use Node **24.20.0** (`.nvmrc`) and npm 11 or 12; `nvm install && nvm use` is optional if you already use nvm. Open `apps/mobile/HikingProject.xcodeproj` in Xcode and select the `HikingProject` scheme and an available iPhone simulator. The committed project is ready to open; XcodeGen is only needed to change project structure.

## Validation matrix

| Scope | Command / evidence | Where |
| --- | --- | --- |
| Documents and governance validators | `python3 scripts/ci/check_docs.py`; `python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v`; `git diff --check` | Local and Linux CI |
| Web lint, component/contract tests, typecheck and production build | `npm run check:web` | Local and Linux CI |
| Portable Swift catalogue, SQLite and transaction tests | `swift test --disable-automatic-resolution --jobs 2` | Local Mac and Linux CI |
| SwiftUI app build and XCTest UI smoke | `xcodebuild test` with the project/scheme/destination in [Mobile](MOBILE.md#build-and-test) | Local Mac/Xcode |
| Offline, location, recording, notifications, battery and public release | MVP-specific scenarios and real-device evidence | Pending feature work; not proved by this foundation |

Linux CI keeps the two existing required names. **Documentation integrity** now also executes Web and portable Swift checks so existing branch protection gates these tests without a settings change. **Contribution policy** still validates PR/Issue/commit conventions. See [CI runner guide](CI.md) for toolchain prerequisites and troubleshooting. No iOS CI claim is made for the Linux runner.

## What the foundation includes

- A native iOS 18+ sample catalogue, GRDB-backed SQLite storage and an optional Mapbox online preview. Default mode does not create a map view or require a token.
- A React/TypeScript internal catalogue preview with search, detail inspection and invalid-data/empty states.
- Two explicitly fictional metadata entries, shared JSON Schema, version validation and stable IDs. These are not part of the 20–30 verified routes and contain no route geometry.
- Locked Swift/npm dependencies and executable tests. No backend, accounts, cloud database, GL JS, publishing or deployment has been added.

Do not add stubs that claim offline packs, recording or alerts already work. Implement one reviewed workflow increment at a time, adding its meaningful tests and applicable CI coverage. Use local fixtures for content work until source verification and a static hosting decision are complete.

## Handoff and next work

After the foundation PR is reviewed and merged, create separate Issues for (1) Mapbox online/offline feasibility and cost validation, (2) catalogue geometry/source provenance and content validation, and (3) recording state/persistence design followed by real-device testing. The web member can build local validation/import previews while the mobile member works on map feasibility, using an agreed contract. These are proposed next tasks, not acceptance already completed.

See [foundation validation](FOUNDATION-VALIDATION.md) for the actual evidence and remaining limits. Keep generated builds, databases, tokens, local configuration and personal test tracks out of commits. All development remains free; no paid Apple enrollment, Mapbox billing, hosted CI or deployment is included.
