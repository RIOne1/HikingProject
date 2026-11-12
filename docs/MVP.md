# First Release MVP

**Status:** agreed specification; the expanded planning, account and publishing scope is not implemented or accepted by this documentation update.

**Decision baseline:** 13 November 2026, [Issue #9](https://github.com/RIOne1/HikingProject/issues/9).

**Authority:** this English document is authoritative. [中文镜像](MVP.zh-CN.md) must retain the same requirement IDs, scope and acceptance conditions. Update both in the same PR when meaning changes. Use [CONTRIBUTING](../CONTRIBUTING.md) for collaboration and [SECURITY](../SECURITY.md) for security and private-data handling.

## 1. Product goal and users

Serve beginner-to-intermediate hikers taking half-day or full-day trips in New Zealand, through a native iPhone app and a Web planner with an administrator console. The core workflow is:

**Plan precisely on Web, or combine nearby routes on mobile → save a private plan → sync to iPhone → download for offline use → follow and record the hike → provide feedback → deliberately submit completion evidence → administrator review → publish for others to choose.**

Users can also choose existing routes or privately import GPX, record locally and export their own trips. Reporting a condition does not require completing the whole route. Publication, source verification and a recorded past walk do not prove current safety or access.

Start with **one connected, field-testable pilot area; its location is still undecided**. Acceptance depends on network scenarios: junctions, loops, out-and-back routes, repeated edges, partial segments and disconnected selections. The earlier 20–30 curated-route count becomes a later content target, not a substitute for a usable network or a first-release minimum. Record source/access checks separately from actual field walks.

The team is two to three people; the owner leads AI-assisted development and testing. Practical SQL learning remains a goal, supported by inspectable queries, constraints, transactions and migrations that serve product correctness.

## 2. Delivery and cost boundaries

- Mobile targets iPhone, iOS 18+. Web uses React/TypeScript/Vite for public planning, reports and administrator work, with different interfaces and permissions. Other native platforms, multi-day/advanced hiking and global coverage are not first-release commitments.
- Guests can browse, record locally and use downloaded routes. Login is required for account-owned plan synchronization, reports and publication submissions. Existing offline use must survive an expired login or unavailable backend.
- Use local Supabase with PostgreSQL, PostGIS, Auth and row-level security (RLS). Team development uses real local Auth identities, email/password and captured test mail. This simplification applies only to team development; it is not an external-user account strategy.
- Current development **must remain free**. Use local services, synthetic fixtures and the existing self-hosted CI. Do not activate paid services, paid CI or upgrades; pause affected use when an allowed free quota or trial ends.
- Mapbox iOS SDK and Mapbox GL JS are conditional selections. Verify permitted no-card access, actual limits, offline behaviour and SDK compatibility. Map rendering does not supply a verified trail network or guarantee a routing service can preserve chosen segments. The graph data and routing implementation remain validation decisions.
- The post-deployment service budget remains a **hard NZ$50/month** for maps, backend, hosting, mail and related services together. Mapbox has [no automatic billing cap](https://docs.mapbox.com/accounts/faq/can-i-set-up-a-cap-for-monthly-spending/); production costs and operating limits remain release blockers. Alerts are not spending caps.
- Apple Developer Program membership is a later, separately approved distribution expense. Free development does not include TestFlight/App Store publication. Validate demand before selecting monetization; payments and subscriptions are not in this MVP.

## 3. Must-have requirements

### MVP-01 — Route discovery and details

Browse curated and administrator-approved public routes and inspect geometry, source, revision, available planning information and known access notes. Show attribution, verification status and source/update or retrieval times. Missing facts remain unknown. Preserve stable route IDs and distinguish source checks, field evidence and publication approval.

**Acceptance:** details match the selected revision; downloaded content remains readable offline. Pilot content covers the network scenarios in section 1 with recorded provenance/access checks and representative field evidence. No fixed 20–30-route count is required. A map line, an approved route and current route status are not treated as interchangeable facts.

### MVP-02 — Private GPX route import

Import supported GPX routes/tracks into local storage for preview, surrounding-map preparation, following, recording and off-route warnings within tested format, size and coverage limits. Label imported routes as private, user-imported and unverified. They do not automatically become checked-network segments, publishable routes or evidence of an App-recorded completion.

**Acceptance:** document supported elements, multiple tracks/segments and limits; validate coordinates and timestamps. Malformed or unsupported input produces a useful error without corrupting data. Preserve meaningful gaps instead of inventing connecting lines. Exercise the private offline workflow; apply known closure restrictions where an affected segment can be identified, without claiming unknown GPX access is verified.

### MVP-03 — Offline map preparation

Download the selected route revision and its surrounding map/style resources before departure. Show coverage, progress, failure and readiness. Keep route geometry, ordered parts, version and last-known status with the pack; map cache and business data have separate ownership. Only verified complete resources count as ready.

**Acceptance:** airplane-mode cold launch shows the saved route, available map labels/icons, current location when available and recorded track. Incomplete downloads never appear ready; retry, coverage edges, resource limits and sizes are tested. Map removal or failure preserves routes/trips. An interrupted replacement retains the previous usable pack. Offline status is visibly last-known, not guaranteed current.

### MVP-04 — Location and recording state

Show current location and recording state, including reduced accuracy, stale fixes and interruptions. Explain permissions when needed; denial does not prevent browsing, history or file exchange.

**Acceptance:** denial, approximate/reduced accuracy, stale location and resumed location have understandable visible states. Old fixes are not shown as fresh; interpolation must not conceal gaps. Navigation displays saved-line position and progress without promising turn-by-turn voice guidance.

### MVP-05 — Local foreground and background recording

Start and finish a hike, persisting ordered points, timestamps and quality information locally, independent of map rendering. Support normal screen-lock/background behaviour permitted by iOS and surface storage failures.

**Acceptance:** real-device evidence covers screen lock, foreground/background changes, day-hike-duration use and interrupted-session recovery. Preserve committed points and identify unfinished trips on reopening; record time, battery and gaps. Do not promise uninterrupted recording after force-quit or device restart. Agree device coverage, duration and quantitative thresholds before marking this requirement passed.

### MVP-06 — Off-route warnings, including lock screen

Compare suitable recent location samples with the saved route locally. Provide in-app warnings and authorized local lock-screen notifications. Filter poor fixes and repeated alerts; document and validate thresholds and the effect of notification refusal.

**Acceptance:** controlled on-route, off-route, poor-accuracy and repeated-alert cases include real-device lock-screen delivery. Warnings need neither a push server nor online routing. Uncertain location does not become a confident off-route claim. Offline automatic rerouting is not part of this feature.

### MVP-07 — Recorded path for returning

Display the user's already-recorded path to assist inspection and returning along it.

**Acceptance:** recorded segments and gaps remain faithful and visible offline. This does not calculate a new return route, certify safety or provide rescue services.

### MVP-08 — Local history and GPX export

Keep completed trips available locally and allow deliberate GPX export. Use defined, tested calculations for statistics, preserving supported coordinates, timestamps and segment semantics without inventing measurements.

**Acceptance:** trips survive relaunch; an independent GPX reader can parse exports and their contents match saved data. Cancelling export leaves the trip unchanged. GPX portability is not full application backup; account synchronization does not automatically upload all trip history.

### MVP-09 — Durable SQL data and migrations

Use SQLite + GRDB on iPhone and PostgreSQL + PostGIS in the backend. Use explicit parameterized SQL, constraints, transactions and versioned migrations appropriate to each database. Stable business IDs remain independent of map caches and vendor IDs. Access the backend through Supabase SDKs and reviewed SQL/RLS; Prisma is not part of the MVP.

**Acceptance:** test relevant write failures/interruption, query/index behaviour and upgrades from representative earlier schemas without data loss. Failed imports/updates cannot leave partial user data. Map/catalogue replacement cannot delete trips or private plans. Server tests exercise migrations and user/role isolation through the actual client access path. Explain important SQL; SQLite migrations do not stand in for PostgreSQL migrations or RLS tests.

### MVP-10 — Versioned network and route content

Use GeoJSON geometry and JSON metadata for interchange, with source IDs, attribution, timestamps, access/verification state and network version. Planning needs connected topology and ordered selected segments, not just display polylines. Freeze saved route revisions; later network edits cannot silently reshape a saved, downloaded or submitted route.

**Acceptance:** reject unsupported/incompatible versions, invalid topology/content and interrupted updates while retaining usable data. Both clients agree on direction, order, repeated edges and partial-segment boundaries. Downloads and sync identify the exact route/network revisions; stale or unavailable status is explicit. Local fixtures/endpoints support free development; hosted delivery is a separate release gate. The current synthetic metadata schema is not this completed contract.

### MVP-11 — Privacy, permissions and untrusted input

Raw trip history is local and private by default. Plan sync, export and publication evidence have explicit, separate purposes. Submit only the route-relevant track portion the owner chooses, privately for review. Apply [SECURITY](../SECURITY.md) to files, accounts, logs, credentials, SDKs and AI inputs.

**Acceptance:** unauthorized users cannot read private plans or evidence. Public routes expose approved route/completion information, not raw private tracks. Permission-denied paths work; personal tracks, databases and secrets stay out of fixtures/shared logs. Verify actual SDK networking/telemetry before privacy claims; local storage does not prove zero external data transmission.

### MVP-12 — Usable and testable end-to-end flow

The owner leads real-device and Web validation of both planning interfaces, synchronization, offline walking and the feedback/review/publication cycle. Retain the guest and private GPX workflows. Check text sizing, labels and operability of important actions and states.

**Acceptance:** recorded runs cover Web selection and mobile combination, download, offline/background recording and warnings, finish/history/export, completion evidence, administrator decision and public discovery. Include denied/expired login, disconnected selections, failed sync and incomplete evidence. Record device/browser/OS, build/commit, route/fixture, conditions and limitations. Simulator-only evidence cannot establish outdoor/background reliability.

### MVP-13 — Precise Web route planning

Select a whole trail, a junction-to-junction segment or part of a segment, using snapping and via points to refine the plan within the checked pilot network. Keep selected portions, direction and order explicit. Where a connector is needed, preview its geometry and information for confirmation before it becomes part of the route.

**Acceptance:** junction, loop, out-and-back, repeated-edge and partial-segment scenarios preserve the user's choices. A disconnected selection fails with a useful explanation; do not silently shortcut, trim or replace selected portions. Unknown/off-network or confirmed-closed segments are not offered as usable connectors. Saved geometry and ordered parts agree. Freehand off-trail planning and fixed-distance chunk selection are not required.

### MVP-14 — Simplified mobile route combination

Before departure and while online, select a route and nearby routes, preview the connecting portions, confirm their order/direction and save one complete plan. Use the same checked network and route contract as Web, with simpler interaction instead of a precision editor.

**Acceptance:** the combined plan retains every selected portion and confirmed connector, including repeated traversal where needed. Reject disconnection or a closed connector; no silent shortening or replacement. The saved plan matches the preview and can be downloaded under MVP-03. Mid-hike planning, offline combination and automatic rerouting are deferred.

### MVP-15 — Accounts and permissions

Use Supabase Auth email/password with stable user IDs, ownership and controlled administrator roles. Team development uses test accounts and local captured email with real authentication/session/RLS behaviour. Guest browsing, local recording and existing offline routes remain usable without login. Login gates sync, reports and submissions, not access to the user's existing local hike.

**Acceptance:** test guest, two distinct users and administrator access, denied operations, session expiry and account switching without cross-user leakage or deletion of local trips. Test confirmation/reset flows through captured mail; server credentials and privileged keys never enter clients. Before external testing, validate real email confirmation, recovery and account deletion. Later Resend integration changes mail delivery, not the identity model.

### MVP-16 — Private plan synchronization

Authenticated owners can save private plans on Web/mobile and fetch the same revision on iPhone for download. Sync includes route geometry, ordered segments, source/version and required planning metadata; it is not cloud backup of all raw trip history. Offline navigation uses a complete local snapshot.

**Acceptance:** Web → iPhone and mobile-save/reopen scenarios retain identical selected geometry and order. Interrupted/retried writes do not create duplicate routes or partial usable revisions. A stale edit produces an explicit conflict/reload decision rather than silently overwriting newer work. Logout, expired sessions or outages do not block an existing offline hike; account changes must not expose another user's cloud data.

### MVP-17 — Completion evidence and moderated publication

After walking, the owner provides feedback and may deliberately submit the route-relevant App-recorded track portion for private administrator review, tied to the exact route revision. Evidence that supports completion permits an application, not automatic publication. Insufficient evidence requires additional evidence/manual review; clearly incomplete traversal does not qualify the whole planned route. GPS is supporting evidence, not unforgeable proof.

**Acceptance:** test supported, insufficient and clearly incomplete cases, GPS gaps and repeated segments; calibrate completion thresholds with pilot evidence before acceptance. Self-declaration or imported GPX alone cannot satisfy the App-recorded requirement; manual review cannot waive actual completion. Keep draft/submitted/needs-evidence/rejected/approved-published/withdrawn states distinguishable. Only an authorized administrator can publish an eligible submitted revision; geometry changes require a new revision, new review and evidence appropriate to that revision. Old approval/evidence never transfers automatically.

### MVP-18 — Condition reports and closure handling

Signed-in users can report route conditions even after an incomplete or aborted hike. Distinguish unverified community reports from confirmed closure/access information, with provenance and observation/update time. Administrators assess reports; a report does not automatically become an official closure.

**Acceptance:** a confirmed closure blocks affected new planning, publication and starting a new planned navigation session. Map inspection and independent recording remain available, and an ongoing hike/navigation is not forcibly stopped. Expired closure information does not imply reopening. Offline packs show last-known status and its limitations; reconnecting refreshes available status without claiming real-time coverage.

### MVP-19 — Administrator console and public-content moderation

Provide authorized administrators with user management, route/base-network maintenance, status assessment and publication review. Record consequential changes with actor, time, reason and affected revision. Administrators do not directly edit users' private plans or browse unrelated raw trip history; review access is limited to submitted evidence.

**Acceptance:** test ordinary-user denial and authorized administrator actions at the backend, not only hidden UI controls. Route geometry changes follow MVP-17; status updates retain their provenance. Before public UGC use, verify content filtering, reporting, handling of abuse, blocking abusive users and a reachable contact channel. Route approval alone does not fulfill these operations; see [Apple UGC guidance](https://developer.apple.com/app-store/review/guidelines/#user-generated-content).

### MVP-20 — Withdrawal and account deletion

Allow route withdrawal and user-initiated account deletion, including an in-app entry point. Stop server public display and further distribution of withdrawn content and handle associated personal data and user-generated content. Reconnecting clients process withdrawal information; do not delete another person's own recorded trips or forcibly interrupt an active hike.

**Acceptance:** test server access removal, deletion scope and reconnect cleanup for saved public content, alongside preservation of independent local recordings. Immediate deletion from a disconnected device cannot be guaranteed. Define cleanup timing, active-hike handling, retention and user-facing explanations, then validate them before external/public release. Do not assume anonymizing the author permits indefinite retention of their published content; verify the implemented flow against [Apple account-deletion requirements](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion).

## 4. Technical baseline

| Area | Agreed approach |
| --- | --- |
| Mobile | Swift, SwiftUI, iOS 18+; UIKit where needed; lightweight modular MVVM and Swift Concurrency |
| Web | React + TypeScript + Vite; public planner/reporting and administrator console; npm lockfile, Vitest/Testing Library and ESLint |
| Maps | Conditional Mapbox iOS SDK and Mapbox GL JS; managed map caches separate from business data |
| Planning | Checked connected network, ordered segment selection and confirmed connectors; data supplier, graph processing and routing implementation require pilot validation |
| Location and alerts | Core Location and local notifications, independent of map rendering |
| Mobile database | SQLite + GRDB; explicit SQL and versioned local migrations |
| Backend | Local Supabase: PostgreSQL + PostGIS + Auth + RLS; Supabase SDKs, explicit SQL and SQL migrations; no Prisma |
| Identity and mail | Email/password, stable Auth user IDs; local test mail now, real mail via Resend later after validation |
| Data and transfer | Versioned GeoJSON + JSON, route revisions and local snapshots; GPX via Foundation XML processing; URLSession where appropriate |
| Dependencies | Swift Package Manager and npm; stable compatible versions and reviewed lockfiles |
| Verification | Swift Testing, XCTest, Web tests, SQL/RLS integration checks when implemented, and real-device field evidence |
| Delivery | Existing self-hosted Linux CI; local Mac/Xcode iOS checks; external hosting and production mail remain unselected/unconfigured |

Mapbox rendering is not the graph/routing engine. Do not assume PostGIS alone solves routing or adopt a paid Directions service without validating ordered-selection semantics and costs. Keep business logic independent of vendor rendering types, but avoid a speculative universal framework. New dependencies and material contracts need review; later stack changes must explain requirement, migration, cost and verification impact.

## 5. Explicitly deferred

- Multi-day/advanced hiking, global coverage and other native platforms.
- Off-network/freehand wilderness planning, mid-hike replanning, offline route combination, automatic rerouting and turn-by-turn voice guidance.
- Full application backup/restore, automatic raw-history cloud backup and live location sharing. MVP-16 private-plan sync and MVP-17 deliberate evidence submission are the limited approved transfers.
- Social feeds, following, chat and general-purpose social reviews; moderated route publication and condition reports are in scope.
- Real-email delivery during team-only development. It becomes required before external users, not an optional post-release improvement.

## 6. Verification and Definition of Done

### Development acceptance

Implement MVP-01 through MVP-20 with traceable evidence, no blocking core-flow defects and non-author human review under [CONTRIBUTING](../CONTRIBUTING.md). Record checks as **Passed**, **Failed**, **Not run** with a reason, or **Not applicable** with justification. Required unrun checks remain blockers; documentation, AI review or a green foundation build is not product acceptance.

| Open validation | Evidence needed before the affected requirement can pass |
| --- | --- |
| Pilot area and network | Choose a connected field-testable area; verify licensing, attribution, access sources, topology and representative scenario coverage |
| Planner feasibility | Demonstrate selected-segment preservation, partial/repeated traversal, connector confirmation and disconnected/closed rejection in both clients; select graph/routing implementation based on this evidence |
| Mapbox | Verify permitted free access and actual map/offline limits, SDK compatibility and privacy behaviour; do not incur charges to prove feasibility |
| Recording and completion | Agree devices, duration, accuracy/alert/completion thresholds and performance/storage limits before testing; calibrate with field evidence, including GPS gaps |
| Backend and sync | Implement separate SQL migrations, ownership/RLS, two-user/admin negative tests, revision conflicts, interrupted sync and local-history preservation |
| CI environment | Add meaningful checks with each feature; backend tests need an explicitly verified free isolated environment, not an assumption that nested Docker works on the current runner |
| Withdrawal/deletion | Define data scope, cleanup timing and active-hike behaviour; test disconnected/reconnected clients and preserve independent trip records |

### External testing and public release

Before inviting external users, validate real email confirmation/recovery, account deletion, data permissions and privacy explanations; configure moderation/reporting/blocking/contact for exposed UGC. Choose and verify a free authorized testing environment or keep testing local/team-only. Local captured mail is not sufficient for external users.

Before public release, also resolve the combined NZ$50/month service cap, Mapbox billing exposure, hosting/database/mail operation and data recovery. Complete separately budgeted Apple distribution steps; verify actual App Store privacy, UGC and deletion requirements, including offline withdrawal behaviour. Verify source/attribution/access freshness, representative field results and an end-to-end confidential security-reporting channel. Maintain the required GitHub review/check protections; documents alone do not configure them.

**Current state:** only the iOS and internal React foundations, synthetic metadata schema v1, catalogue SQL store and their tests are implemented. Existing CI covers documents, contribution metadata, Web and portable Swift/SQLite; local Mac evidence covers the foundation iOS build/UI. No planner, GL JS integration, backend/Auth/RLS, synchronization, publication or deletion system has been added. Offline maps, recording, alerts, GPX and real route content also remain pending. See the [development guide](guides/DEVELOPMENT.md) and dated [foundation validation](guides/FOUNDATION-VALIDATION.md); no MVP requirement is declared accepted by the bootstrap or this specification.

## 7. Evidence and maintenance

- Create/confirm a tracking Issue before repository changes, include its number in the branch and link it in the PR. Link affected MVP IDs and validation evidence too; requirement IDs do not replace Issue numbers.
- Update both languages in the same PR. Resolve ambiguity against the English version and correct the mirror. Preserve existing IDs when extending a requirement so earlier evidence remains traceable.
- The [archived research](research/2026-11-06-user-feedback/Hiking_App_User_Feedback_Research_ZH_2026-11-06.pdf) is dated desktop research, not completed user validation or proof this combination of features is unique.
- Technical references: [Mapbox offline](https://docs.mapbox.com/ios/maps/guides/offline/), [Apple background location](https://developer.apple.com/documentation/corelocation/handling-location-updates-in-the-background), [GRDB](https://github.com/groue/GRDB.swift), [Supabase local development](https://supabase.com/docs/guides/local-development), [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [SQL migrations](https://supabase.com/docs/guides/local-development/database-migrations), [PostGIS](https://supabase.com/docs/guides/database/extensions/postgis), [local Auth testing](https://supabase.com/docs/guides/auth/testing-auth-flows) and [Resend SMTP integration](https://resend.com/docs/send-with-supabase-smtp). Platform documentation informs design; it does not prove application acceptance.
