# Security Policy

## Supported state

HikingProject is a public repository in pre-release development. There is no released app version or security-support lifetime to promise. The team handles findings in the current development baseline and assesses their effect on any affected branches. Review requirements in [CONTRIBUTING.md](CONTRIBUTING.md) also apply to security fixes.

## Reporting a vulnerability

GitHub Private vulnerability reporting is enabled for this public repository. Use [Report a vulnerability](https://github.com/RIOne1/HikingProject/security/advisories/new), or open the repository's Security → Advisories page and choose the private reporting action. Sign in to GitHub if required. The repository owner receives and triages reports; no response-time guarantee is promised.

**Verified on 12 November 2026:** the setting is enabled in GitHub and confirmed through its API. An end-to-end report from an external reporter and maintainer receipt have **not** been tested. Complete a coordinated, sanitized test before public app release; enabling the feature alone does not satisfy that release gate. The security policy becomes visible on GitHub's Security page after this file reaches `main`.

Keep vulnerability details, exploit material, tokens, exact personal locations and private GPX files out of public Issues, PRs and discussions. If the reporting link is unavailable, agree a private channel with the maintainer before sending details; do not substitute a public Issue.

Security work still needs a tracking Issue before repository edits under [CONTRIBUTING.md](CONTRIBUTING.md). Keep that Issue and its PR description sanitized, with non-sensitive scope and acceptance criteria; retain confidential details in the private report or agreed channel. A useful report identifies the affected revision/build, device/OS, impact, minimal reproduction and redacted evidence. Prefer synthetic reproductions; never include working credentials or another person's location data without authorization.

[GitHub's private reporting documentation](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) describes feature availability and setup.

## Repository security controls

The free public-repository controls verified on 12 November 2026 are dependency graph, Dependabot alerts, Dependabot security updates, secret scanning alerts, push protection and private vulnerability reporting. Secret detection covers supported patterns; it does not establish that all private data or credentials are absent. Settings were verified; no real secret was pushed to test them.

Dependabot can propose security-update PRs when supported dependency data exists. Bot-authored proposals are **not mergeable deliverables under this team's policy**: a human must create a sanitized tracking Issue, use a numbered task branch, review/adapt the update, and open a human-authored PR with normal checks and non-author approval. Preserve accurate attribution and link the proposal. Do not merge a bot PR or waive branch/Issue rules. Version-update scheduling and application dependency coverage are not established at this baseline.

No paid scanner, AI scan or agentic autofix was activated. CodeQL/app scanning is deferred until useful supported application code and a verified free workflow exist. Reassess feature eligibility and costs before changing repository visibility or automation. The settings described here are a dated observation, not a guarantee they cannot drift.

## Self-hosted CI

Repository checks use the Linux runner label `hikingproject-local-ci` with no fallback to GitHub-hosted runners. The owner controls the runner host and must keep its software updated. Use a dedicated unprivileged environment without personal files, SSH keys, cloud credentials, signing material or a mounted Docker socket. Restrict access to the host and private network; a persistent container is not equivalent to a fresh isolated machine for every job.

GitHub recommends avoiding self-hosted runners for public repositories because PR workflows can execute hostile code. This repository therefore requires approval for **all external contributors**, and maintainers MUST NOT approve fork-origin workflow runs on this runner. Review external changes before copying them onto a normal Issue-numbered branch in this repository. The workflow's same-repository condition is an additional filter, **not a security boundary**: a PR can modify workflow code. A skipped fork check is not evidence that the contribution passed validation. See [GitHub's self-hosted runner guidance](https://docs.github.com/en/actions/reference/security/secure-use#hardening-for-self-hosted-runners).

Keep the workflow token read-only and checkout credentials unpersisted. Do not expose runner registration tokens in Issues, PRs or logs. If the host is suspected to be compromised, stop its runner and have the owner rebuild the environment and rotate affected credentials before reconnecting it. Passing CI establishes the tested repository behaviour; it does not audit the PC's isolation, reboot recovery or continuous availability.

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

Do not disable validation or security checks just to make a build pass. Use free local tools and existing authorized checks; adding a scanner or CI service does not authorize payment. The free GitHub controls and private reporting channel listed above are configured; no paid scanner or third-party reporting service is included.

Security fixes still require a non-author human reviewer under [CONTRIBUTING.md](CONTRIBUTING.md) and the normal merge procedure; other contributors may review. When public detail would expose an unresolved vulnerability, coordinate the confidential review method with the maintainer before posting a normal public PR.
