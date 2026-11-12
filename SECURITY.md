# Security Policy

## Supported state

HikingProject is in private, pre-release development. There is no public released version or security-support lifetime to promise. The team handles findings in the current development baseline and assesses their effect on any affected branches. Review requirements in [CONTRIBUTING.md](CONTRIBUTING.md) also apply to security fixes.

## Reporting a vulnerability

**No external confidential reporting channel is currently configured.** Do not treat a GitHub username as a private messaging address or assume that adding this file enables vulnerability reporting. Do not send vulnerability details to an unverified destination.

While the project is private, team members should first agree a private communication channel with the repository maintainer without disclosing sensitive details in the request. Keep vulnerability details, exploit material, tokens, exact personal locations and private GPX files out of public Issues, PRs and discussions.

Security work also needs a tracking Issue before repository edits, as required by [CONTRIBUTING.md](CONTRIBUTING.md). Keep that Issue and the linked PR description sanitized; record only a non-sensitive scope and acceptance criteria, and keep confidential details in the agreed private channel.

Before public app release, the maintainer MUST complete a confidential reporting setup. Choose the repository-publication sequence explicitly:

1. While the repository is private, choose the reporting method and responsible humans. If a working channel is required before any source becomes public, configure another genuinely usable confidential method first.
2. If using GitHub Private vulnerability reporting, an authorized human must first make the repository public and then enable and verify the feature as part of that publication process. It cannot be enabled on the current private repository. Do not announce the reporting channel as ready before verification.
3. Test that a report can be submitted and received by the responsible humans, whichever method is chosen.
4. Update this policy with the verified method and any response commitments the team can actually maintain.

An unverified reporting channel blocks public app release. Repository visibility changes require their own authorization; this policy does not authorize making the code public. No email address, active report link or response-time guarantee is implied today. GitHub's private-reporting feature is not currently available here. [Official setup](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

Once a confidential channel is agreed, a useful report includes the affected version/build, device/OS where relevant, impact, minimal reproduction steps and redacted supporting evidence. Prefer synthetic reproductions. Never include working credentials or another person's location data without their explicit authorization.

## Secrets and Mapbox access

- Do not commit live tokens, credentials, signing material, personal configuration or secrets in source, examples, screenshots, reports or PR text. Use placeholder examples and appropriate local configuration.
- Distinguish client-intended Mapbox tokens from secret management/download credentials. Client tokens can be extracted from a distributed app; they still need appropriate scopes and usage controls. Secret credentials must never be embedded in the app.
- Verify the selected SDK's actual configuration requirements; do not invent token requirements or request broader access than necessary.
- If a credential is exposed, stop spreading it and notify the responsible maintainer privately. The authorized owner handles revocation/rotation and any history remediation. Do not use an exposed token to test its power or rewrite shared history autonomously.
- Development stays free. Never bind a paid service, upgrade a trial or weaken usage controls as a shortcut. Mapbox's production spending-limit issue remains an explicit release gate in [MVP.md](docs/MVP.md).

## Personal tracks, diagnostics and AI inputs

- Application-owned trip history is local and private by default. Export/sharing must be user-initiated; map-cache cleanup must not delete business data.
- Use synthetic or explicitly authorized GPX/JSON fixtures. Do not commit personal tracks, local database files, home coordinates or unredacted diagnostic captures.
- Logs and error reports should avoid precise coordinates and identifying route names unless essential and appropriately protected. Shared evidence must be minimized and redacted.
- Do not upload private tracks, databases, credentials, logs or screenshots to AI services or other external tools without the relevant data owner's explicit authorization. A general request to fix code is not permission to disclose private location history.
- Verify actual SDK networking/telemetry and any available controls before privacy disclosures or App Store declarations. Local trip storage does not mean the app makes no network requests or that third-party SDKs collect nothing.
- GPX export is not a complete backup. Full application backup/restore, cloud backup and live location sharing are deferred features; do not add uploads as an undocumented implementation shortcut.

## Untrusted imports and local storage

- Treat GPX, JSON, filenames, route metadata and content updates as untrusted input. Define and test reasonable limits for sizes, element/point counts and nesting before shipping import support.
- Validate coordinates, timestamps, format versions and segment semantics. Reject invalid input with a useful error without damaging existing data.
- Prevent XML external-entity resolution and unintended file/network access. Do not follow links embedded in imported files automatically.
- Use parameterized SQL for values. Any dynamic SQL identifiers must come from controlled, validated choices rather than imported text. Use transactions for changes that must succeed or fail together.
- Test schema migrations, write failures and interrupted operations. Keep business records separate from Mapbox's managed cache and avoid destructive fallbacks that silently reset a user's database.
- Verify iOS file-protection behaviour with locked-screen recording and after restart. Protect data without assuming that a database which works while unlocked will remain writable in every device state.

## Dependencies and secure review

Use reviewed dependencies and stable, recorded versions. Check upstream provenance, licenses, required permissions and relevant advisories. New runtime dependencies, permissions, SQL/schema changes, imports, storage protection and sharing behaviour must be made explicit in the PR.

Do not disable validation or security checks just to make a build pass. Use free local tools and existing authorized checks; adding a scanner or CI service does not authorize payment. No paid scanner or external security-reporting integration is currently promised or configured.

Security fixes still require a non-author human reviewer under [CONTRIBUTING.md](CONTRIBUTING.md) and the normal merge procedure; other contributors may review. When public detail would expose an unresolved vulnerability, coordinate the confidential review method with the maintainer before posting a normal public PR.
