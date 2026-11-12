# Backend and account development guide

## Status and selected approach

The approved target is **local Supabase with PostgreSQL + PostGIS + Auth + RLS**, accessed through Supabase SDKs, explicit SQL and SQL migrations. MVP does not use Prisma. This guide records boundaries for future implementation: the repository currently has no Supabase configuration, server migrations, client SDK integration or backend test command. Do not describe a local service as running or a permission policy as tested until its implementation Issue establishes evidence.

The existing [data guide](DATA.md) distinguishes the synthetic schema v1 from the planned network/route contract. SQLite + GRDB remains the iPhone database; adopting PostgreSQL does not replace local offline storage or authorize automatic trip-history upload.

## First backend implementation Issue

Create a scoped Issue and numbered branch under [CONTRIBUTING](../../CONTRIBUTING.md). That task should establish:

1. Verified free local container/CLI prerequisites and pinned compatible versions, with reproducible setup/reset/test commands. Bind development services and captured mail to the authorized local environment. Do not create a cloud project or enable paid services as an incidental setup step.
2. Committed configuration, explicit SQL migrations and synthetic seed data without working credentials. Run migrations through controlled tooling, separately from ordinary-client RLS tests. Separate disposable test resets from migrations that preserve application data. Document extension setup, including PostGIS, and important SQL/constraints.
3. Real local Auth users and client access for guest, two distinct users and an administrator. Test ownership/RLS and privileged operations through actual access paths, not only service-role queries.
4. A verified free CI approach and the checks that the PR runs. The existing runner is a container; see [CI limitations](CI.md#expanded-mvp-coverage-to-add-with-implementation) before assuming it can run a nested Supabase stack.

Use [Supabase local development](https://supabase.com/docs/guides/local-development), [SQL migrations](https://supabase.com/docs/guides/local-development/database-migrations) and [PostGIS](https://supabase.com/docs/guides/database/extensions/postgis) to choose concrete setup steps in that Issue. These references are not executable setup already installed in this repository.

## Identity, permissions and email

- Use email/password with stable Auth user IDs. Application profiles and ownership reference those IDs, not email strings. Leave credentials/password handling to Auth; no custom password table or fake production-login bypass.
- Keep roles controlled by trusted server operations. A user-editable profile field must not grant administrator permission. Use RLS on client-accessible private data and equivalent checks for privileged functions/endpoints; test unauthorized reads and writes as well as allowed operations.
- Only client-intended keys belong in browser/mobile configuration. Secret/service-role keys, database credentials and SMTP/API mail keys stay server-side. Such keys can bypass controls and cannot prove an ordinary client's authorization behaviour.
- Team development uses disposable test accounts and captured local mail, while retaining real sessions, expiry and ownership checks. Follow [Auth-flow testing](https://supabase.com/docs/guides/auth/testing-auth-flows): enable email confirmation explicitly in the local configuration when testing it; local defaults must not silently stand in for a confirmation test. Exercise confirmation and recovery links without publishing tokens or inbox contents.
- Real email delivery through Resend is later work. Resend is an SMTP delivery provider, not the account database or authentication layer; see its [Supabase integration](https://resend.com/docs/send-with-supabase-smtp). Before inviting external users, validate real confirmation, recovery, account deletion, privacy and applicable costs. No production domain, SMTP service or cloud database is configured by this guide.

## Data and operation boundaries

Private-plan synchronization transfers owned checked-network plan revisions with geometry/ordered parts and planning metadata. It does not upload all raw trip history or add a private-GPX cloud workflow. Keep raw recordings local by default; publication receives deliberate route-relevant App-recorded evidence plus feedback, covering the complete submitted revision including connectors/repeated traversals without requiring unrelated locations. Geometry edits require new review and appropriate evidence; current closure/status updates must still affect new use of older saved geometry.

Public clients may discover approved content; they must not read private plans/evidence or invoke administrator actions. Administrators manage users, base content, status and submissions, with recorded reasons/revisions, without directly editing private plans or browsing unrelated history. Keep state changes transactional where partial writes could expose a route prematurely.

Design retried writes, stale-edit conflicts and interrupted sync before connecting both clients. Login expiry/outage cannot block existing offline navigation or delete local history; account switching must isolate account-owned caches. Do not silently resolve conflicting geometry by replacing the user's chosen segments.

Withdrawal/deletion must stop server public display/distribution, process personal data/UGC and provide reconnect cleanup information. Define deletion of the requesting account's server data/evidence and the client's corresponding account-data handling; preservation of other users' independent recordings is not an exemption for the deleting user's data. Distinguish unrelated guest-local records and logout from explicit deletion. Retention, cleanup timing and active-hike behaviour remain external-release validation gates, not permission to retain content indefinitely. See [SECURITY](../../SECURITY.md) and MVP-17 through MVP-20 for the full requirements.

## Evidence expected with feature PRs

Run relevant migration/constraint and RLS tests with synthetic fixtures. Include two-user isolation, forbidden role escalation, unauthorized publication, rejected/insufficient completion evidence, stale updates/retry and deletion/withdrawal cases as those flows are implemented. Verify privileged server operations separately from ordinary client access. Do not add empty checks that merely assert a policy exists.

Report exact commands, versions, covering CI job and remaining manual/device gates. Existing catalogue tests do not cover these operations. Keep real-device offline/background evidence in mobile work and distinguish team-local Auth success from external email/deletion readiness. All current development remains free.
