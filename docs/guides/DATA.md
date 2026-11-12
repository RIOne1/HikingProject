# Shared data and SQL guide

## Foundation contract

The single [sample catalogue](../../shared/fixtures/catalogue.sample.json) is bundled by the Swift `HikingSampleData` target and imported by React. Its [JSON Schema](../../shared/catalogue.schema.json) describes **schemaVersion 1**, a metadata-only development contract. These fictional entries are not source-verified routes, and their coordinates are synthetic test points. This is not the network/route revision contract required by MVP-10. Issue #9 changes documentation only; it does not change schema v1, fixtures, SQL or decoders.

| Field | Meaning / validation |
| --- | --- |
| `schemaVersion` | Exactly `1`; reject unsupported versions |
| `routes` | At most 100 entries; empty is valid |
| `id` | Stable lowercase ASCII letters/digits/hyphens, nonempty and unique within the catalogue |
| `name`, `attribution` | Text containing a character outside Unicode `White_Space` and U+FEFF (BOM); preserve the original text |
| `difficulty` | `easy` or `moderate`; synthetic categorization, not a verified external grading system |
| `distanceMetres` | Integer 1–100000, metres |
| `estimatedMinutes` | Integer 1–1440, minutes |
| `startLatitude`, `startLongitude` | Finite WGS84 degrees, respectively −90…90 and −180…180 |
| `sourceKind` | Exactly `synthetic`; the foundation must not imply verified or user-imported content support |

The bounds protect this small fixture contract; they are not GPX import limits or product acceptance thresholds. Unknown object fields are ignored; required fields and types remain checked. Unique IDs are an additional decoder rule beyond the JSON Schema. Both Swift and TypeScript validate at the data boundary before display or persistence. Tests cover the shared fixture, representative invalid values and Unicode text boundaries in both clients; Web tests also exercise the schema. Use the explicit nonblank rule rather than platform-default trimming, which differs for U+0085 (NEL) and U+FEFF.

When adding real content, design versioning, geometry/segment semantics, source/update timestamps, attribution and verification states together. Do not relabel these fixtures as real routes or silently broaden version 1 into a production contract. Include both clients and compatibility/failure evidence in the contract PR.

## SQLite ownership and queries

The root [Swift package](../../Package.swift) exposes `HikingCore`; [RouteStore.swift](../../apps/mobile/Core/RouteStore.swift) contains the important SQL directly. GRDB **7.12.0** manages the database queue, transactions and migration history. No Core Data or ORM-generated schema is used.

`v1_catalogue` creates one `routes` table with a stable text primary key and constraints on difficulty, units, coordinate ranges and synthetic provenance. `SELECT ... ORDER BY id` makes read order deterministic. The primary-key index handles identity; no additional index is justified for this tiny, fully read catalogue. Query/index performance for real route/trip data remains future work.

`replaceCatalogue` validates the complete input, then deletes and inserts inside one GRDB write transaction. Values use SQL placeholders and bound arguments. If any insert fails, the transaction rolls back; the previous catalogue remains available. This replacement API applies only to catalogue metadata. Future user trips must have separate ownership and must never be deleted as part of catalogue replacement or map cache removal.

## Migrations and tests

Once shared, preserve existing migration identifiers and SQL; append a new migration for later schema changes. Do not enable erase-on-schema-change for application data. Keep important SQL and the reason for non-obvious constraints readable in review.

The Swift tests cover decoding/ranges/version rejection, persistence across reopening, repeated migration application, text bound as a SQL value, and rollback after an injected SQLite trigger failure. The rollback test causes an actual database write failure after deletion, rather than only checking pre-validation rejection. Tests use temporary isolated databases and remove only their own temporary files.

This first schema has no earlier production schema to upgrade. It does not establish migration from a populated earlier version, abrupt process interruption, storage exhaustion or trip recovery. Add representative earlier-schema fixtures and preservation tests when the next migration is introduced. The full MVP-09 gate remains open.

## Planned network and route contract

The following are logical responsibilities to resolve in implementation Issues, **not tables, fields or APIs already present**. Keep local SQLite and server PostgreSQL migrations separate. Use Supabase SDKs plus explicit SQL/RLS for server access; no Prisma. Add only the structures needed by the assigned increment, with reviewed units, constraints and compatibility behaviour.

| Concept | Required meaning |
| --- | --- |
| Checked network | Stable node/edge identity and connectivity, geometry, source/version, attribution and checked access conditions; visual crossings alone do not imply a junction |
| Selected route parts | Ordered edge references, traversal direction and partial-edge boundaries with defined units/convention; preserve repetitions. Confirmed connectors are identifiable and never replace selected portions silently |
| Route and immutable revision | Separate stable route identity from a saved geometry/selection snapshot and its source-network version. Editing creates a revision; updates do not silently rewrite downloaded or submitted geometry |
| Ownership | Stable Auth user ID for private cloud records, independent of mutable email and map vendor IDs; distinguish guest-local records from account-owned plans |
| Local trip | Ordered points, time, quality, gaps and the followed revision where known; separate from map cache, catalogue replacement and publication evidence |
| Submission and evidence | Owner-selected route-relevant App-recorded portion plus feedback, bound to the exact revision; private review access and explicit decision/completion state |
| Status/report | Provenance, observation/update time, affected segments/revisions and verification state; status can change without rewriting geometry. Expired closure data does not mean open |
| Offline pack and sync | Exact revision/coverage, readiness and last-known status; complete replacement, retry/conflict handling and preservation of an existing usable snapshot |
| Withdrawal/deletion | Stop server distribution and supply reconnect cleanup information without deleting independent user recordings; retention and active-hike handling require validation |

GeoJSON geometry alone does not encode all these semantics. Agree the contract and representative fixtures with both clients before depending on them. Base-network changes must preserve old revision interpretation or make an incompatibility explicit; do not silently remap an old edge ID onto different geometry. Confirmed current closures still constrain new use of an older saved revision.

## Planned verification cases

- Test junctions, loops, out-and-back, repeated edges, partial edges and disconnection against the same expected ordered selections in Swift/Web. Freeze coordinate/partial-boundary conventions in the contract PR rather than guessing them in each UI.
- Demonstrate Web-save → iPhone-fetch and mobile-save/reopen equality, stale-edit conflicts and retried/interrupted writes. Repeated writes must not duplicate a logical route or expose a partial revision.
- Test SQLite and PostgreSQL migrations with relevant earlier data, failed writes and ownership constraints. Query/index decisions must follow actual access patterns; important SQL and non-obvious constraints need explanations.
- Exercise RLS through anonymous, two-user and administrator sessions, including denied private-plan/evidence access, prohibited role changes and unauthorized publication. Passing tests with a privileged service key cannot establish client RLS correctness.
- Verify completion-state/evidence binding, geometry revision review, closures and withdrawal/reconnect behaviour, preserving independent trip history. Quantitative completion thresholds remain pilot-validation work; a GPS record is not unforgeable proof.

These are future acceptance cases, not existing test results. The [backend guide](BACKEND.md) covers local service preparation and the [foundation record](FOUNDATION-VALIDATION.md) preserves the narrower evidence that exists today.
