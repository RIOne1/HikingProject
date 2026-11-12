# HikingProject

A planned native iPhone app for beginner-to-intermediate half-day and full-day hiking in New Zealand. The current repository contains product specifications, team policies and research; the app implementation and acceptance evidence are pending.

## Start here

| Document | Purpose |
| --- | --- |
| [MVP](docs/MVP.md) | Authoritative English scope, requirement IDs, architecture and acceptance gates |
| [MVP 中文镜像](docs/MVP.zh-CN.md) | Matching Chinese version; update alongside meaningful English changes |
| [CONTRIBUTING](CONTRIBUTING.md) | Issue-first work, numbered branches, commits, PR evidence, non-author human review and merge rules |
| [AGENTS](AGENTS.md) | Instructions and task routing for AI-assisted development |
| [SECURITY](SECURITY.md) | Private data, tokens, imports, vulnerability reporting and release gates |
| [PR template](.github/pull_request_template.md) | A concise structure for reviewable changes and honest verification evidence |

Before starting repository changes, create or confirm the task's tracking Issue, then use a branch named `<type>/<issue-number>-<kebab-case-description>`. Every PR, including a draft, must link that same primary Issue. See [the workflow and its one-time adoption record](CONTRIBUTING.md#2-issues-and-branches).

## Agreed product baseline

The first release completes route selection/import, offline preparation, location and track recording, off-route warnings including lock-screen notifications, recorded-path display, local history and GPX export. Start with 20–30 routes whose sources are checked; field-test representative routes and record the two kinds of evidence separately. Imported GPX routes use the same core workflow within documented, tested limits.

No account is required. Full backup/restore, cloud backup, live location sharing, automatic route planning/rerouting, community features and Mapbox GL JS tools are later candidates. GPX export is not a full application backup. Expansion to multi-day/advanced hiking or global route coverage follows validation rather than being a first-release promise.

The team is planned as two to three people. The owner leads development with AI assistance and leads testing. Practical SQL learning is an explicit project goal; contributors remain responsible for understanding and explaining their changes.

## Confirmed technical direction

| Area | Baseline |
| --- | --- |
| Client | Swift + SwiftUI, iPhone, iOS 18+; UIKit where required |
| Maps | Mapbox Maps SDK for iOS, conditional on technical and production-cost verification |
| Recording and alerts | Core Location and local notifications, independent of map rendering |
| Business data | SQLite + GRDB, parameterized SQL, stable IDs and versioned migrations |
| Structure | One modular app, lightweight MVVM and Swift Concurrency |
| Content | Initially bundled GeoJSON + JSON catalogue; a versioned static-update path using URLSession |
| Exchange | GPX import/export using Foundation XML processing |
| Dependencies and checks | Swift Package Manager, Swift Testing, XCTest, Xcode diagnostics and real-device tests |
| Backend | No first-release application server, accounts service or cloud database |

Keep user data separate from Mapbox's managed cache. Future changes remain possible when requirements justify them; assess their migration and verification impact. See [MVP requirements and acceptance](docs/MVP.md) for the full conditions.

## Cost and implementation status

**Current development must remain free.** Do not activate paid services or upgrade trials automatically. Pause affected service use when a free quota or trial ends. The post-deployment service budget remains a hard NZ$50/month; Mapbox's lack of an automatic spending cap is an unresolved production-release condition. Apple Developer Program membership is a later, separately budgeted distribution expense. Validate demand before choosing monetization.

There is no iOS app project or application test suite yet. [Repository CI](.github/workflows/repository-checks.yml) checks documents and contribution conventions on a self-hosted Linux runner. The app-bootstrap PR must document actual verified targets, schemes and commands. Xcode 27.2 and Swift 6.4.2 were observed during planning. Those versions may change. No paid CI or cloud-build service is required for the current plan.

This is a public repository. The active [`protect-main` ruleset](https://github.com/RIOne1/HikingProject/settings/rules/27098958) requires a PR, one approving review, resolved review conversations and squash merging; it dismisses stale approvals and blocks force pushes and deletion, with no bypass actors. [Human review and merge duties](CONTRIBUTING.md#7-github-enforcement-setup) still apply. See [SECURITY.md](SECURITY.md#reporting-a-vulnerability) for confidential reporting and its verification limits.

## Team workflow and checks

Use the [Issue forms](.github/ISSUE_TEMPLATE/) for development tasks, bugs and technical validation, then track the Issue on the private [HikingProject MVP board](https://github.com/users/RIOne1/projects/1). The board is linked to this repository and shared with the current team; repository access does not automatically grant project access. See [CONTRIBUTING](CONTRIBUTING.md#8-project-board) for status meanings. Forms appear in the default Issue chooser after merging them into `main`.

From the repository root, using Python 3.10+ and Git:

```bash
python3 scripts/ci/check_docs.py
python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v
git diff --check
```

These checks use Python's standard library and need no package installation. CI also validates PR metadata and commit subjects. Read the [coverage and bootstrap limits](CONTRIBUTING.md#verification-evidence); green checks do not constitute human approval, proof of translation accuracy or app acceptance.

## Repository layout

```text
HikingProject/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .github/
│   ├── ISSUE_TEMPLATE/  # Task, bug and technical-validation forms
│   ├── workflows/repository-checks.yml
│   └── pull_request_template.md
├── docs/
│   ├── MVP.md
│   ├── MVP.zh-CN.md
│   └── research/
│       └── 2026-11-06-user-feedback/
│           ├── Hiking_App_User_Feedback_Research_ZH_2026-11-06.pdf
│           └── sources.json
├── scripts/
│   ├── ci/  # Dependency-free repository checks and regression cases
│   └── research/
│       └── build_user_feedback_report.py
├── output/  # Generated drafts and exports; ignored by Git
└── tmp/     # Temporary files and layout audits; ignored by Git
```

## Research documents

The [archived user-feedback PDF](docs/research/2026-11-06-user-feedback/Hiking_App_User_Feedback_Research_ZH_2026-11-06.pdf) and its [source catalogue](docs/research/2026-11-06-user-feedback/sources.json) belong together under a dated study folder. The study is research evidence, not proof of implemented functionality or completed user validation.

Keep final documents and provenance in `docs/`, reusable generation code in `scripts/`, and disposable output in `output/` or `tmp/`. To regenerate a review copy from the project root:

```bash
python3 scripts/research/build_user_feedback_report.py
```

The [generator](scripts/research/build_user_feedback_report.py) needs ReportLab and the macOS fonts named in the script. It writes a review PDF to `output/research/` and a layout audit to `tmp/research/`, creating the directories as needed. Review regenerated documents before promoting them into `docs/`; generation does not replace the archived PDF. This command is not an app build or test.
