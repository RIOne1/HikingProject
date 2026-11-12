# Shared catalogue and SQL guide

## Foundation contract

The single [sample catalogue](../../shared/fixtures/catalogue.sample.json) is bundled by the Swift `HikingSampleData` target and imported by React. Its [JSON Schema](../../shared/catalogue.schema.json) describes **schemaVersion 1**, a metadata-only development contract. These fictional entries are not source-verified routes, and their coordinates are synthetic test points. This is not yet the complete GeoJSON + JSON delivery format required by MVP-10.

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
