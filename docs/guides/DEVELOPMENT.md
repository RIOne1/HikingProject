# Team development guide

Start here after reading [CONTRIBUTING](../../CONTRIBUTING.md). The existing foundation supports mobile and React catalogue work; the expanded [English MVP](../MVP.md) is the product authority for future public planning, accounts and moderated publication. Approved scope is not implemented or accepted functionality.

## Workspace and ownership

| Workstream | Owns | Start with |
| --- | --- | --- |
| Mobile | SwiftUI screens, app composition, iOS adapters and device evidence in `apps/mobile/` | [Mobile guide](MOBILE.md) |
| Web | Public planner/reporting and administrator console in `apps/web/`; currently only a local catalogue preview | [Web guide](WEB.md) |
| Shared data/planning | `shared/`, portable Swift core, network/route revision contracts and selection semantics; coordinate with both clients | [Data guide](DATA.md) |
| Backend | Local Supabase, PostgreSQL/PostGIS migrations, Auth/RLS, sync and publication authorization; not yet initialized | [Backend guide](BACKEND.md) |

For a two-person team, split mobile and Web implementation while jointly reviewing the data/backend contract; sequence backend work explicitly instead of assuming a separate backend engineer. A third member can own data/backend validation. Assign actual people through Issues; these are work boundaries, not automatic GitHub permissions or CODEOWNERS rules. Keep one primary Issue per branch/PR and obtain non-author human review under CONTRIBUTING.

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
| PostgreSQL migrations, Auth/RLS, sync and publishing | Commands/tests must be established by their implementation Issues; see [Backend](BACKEND.md) | Not implemented or covered by current CI |
| Planning semantics and cross-client revisions | Shared synthetic network cases, then pilot-network evidence under MVP-10/MVP-13/MVP-14/MVP-16 | Pending feature work |
| Offline, location, recording, notifications, battery and public release | MVP-specific scenarios and real-device evidence | Pending feature work; not proved by this foundation |

Linux CI keeps the two existing required names. **Documentation integrity** now also executes Web and portable Swift checks so existing branch protection gates these tests without a settings change. **Contribution policy** still validates PR/Issue/commit conventions. See [CI runner guide](CI.md) for toolchain prerequisites and troubleshooting. No iOS CI claim is made for the Linux runner.

## What the foundation includes

- A native iOS 18+ sample catalogue, GRDB-backed SQLite storage and an optional Mapbox online preview. Default mode does not create a map view or require a token.
- A React/TypeScript internal catalogue preview with search, detail inspection and invalid-data/empty states.
- Two explicitly fictional metadata entries, shared JSON Schema, version validation and stable IDs. These contain no route geometry or connected network and are not source-verified routes. The later 20–30-route content target is not the pilot acceptance gate.
- Locked Swift/npm dependencies and executable tests. No backend, accounts, cloud database, GL JS, publishing or deployment has been added.

Do not add stubs that claim planners, accounts, offline packs, recording or alerts already work. Implement one reviewed increment at a time with meaningful tests and applicable CI coverage. Use synthetic local fixtures until real network provenance, access and licensing are verified. No cloud service is needed to begin local backend development.

## Handoff and next work

PR #8 supplies the merged foundation. Create separate, scoped Issues for the following proposed sequence; this documentation update does not create or implement these feature tasks:

1. Select the pilot area and validate source/access/licensing plus connected topology. In parallel, verify permitted free Mapbox iOS/GL JS access and offline behaviour. Do not select a routing provider on rendering capability alone.
2. Agree a versioned network/ordered-route contract using synthetic junction, loop, out-and-back, repeated-edge, partial-edge and disconnected cases. Prototype segment preservation/connector preview before building a full editor.
3. Initialize local Supabase and both client access paths, with SQL migrations, real local Auth, ownership/RLS negative tests and a verified free CI approach. Keep schema v1 fixtures intact until a reviewed replacement contract is implemented.
4. Divide Web precision planning and mobile online combination against the same contract. Add private-plan sync and offline snapshots with conflict/interruption tests. Mobile recording, GPX and alerts can proceed independently using agreed local data boundaries and real-device validation.
5. Add completion assessment, deliberate evidence submission, reports, administrator review and withdrawal/deletion. Validate the full loop and external-user gates before inviting users.

The sequence identifies dependencies, not five oversized PRs. Split work into reviewable Issues. In particular, pilot choice, graph/routing feasibility and production costs are unresolved; do not claim them decided to unblock unrelated local work.

See [foundation validation](FOUNDATION-VALIDATION.md) for the actual evidence and remaining limits. Keep generated builds, databases, tokens, local configuration and personal test tracks out of commits. All development remains free; no paid Apple enrollment, Mapbox billing, hosted CI or deployment is included.
