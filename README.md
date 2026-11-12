# HikingProject

A planned iPhone app and Web planner for beginner-to-intermediate half-day and full-day hiking in New Zealand, with an administrator console for users, route content and publication review. The repository currently contains iOS and internal React catalogue foundations, synthetic data and tests. The expanded MVP below is an approved specification, not implemented functionality.

## Start here

| Document | Purpose |
| --- | --- |
| [Development guide](docs/guides/DEVELOPMENT.md) | Mobile/Web setup, ownership, shared data and executable checks |
| [MVP](docs/MVP.md) | Authoritative English scope, requirement IDs, architecture and acceptance gates |
| [MVP 中文镜像](docs/MVP.zh-CN.md) | Matching Chinese version; update alongside meaningful English changes |
| [CONTRIBUTING](CONTRIBUTING.md) | Issue-first work, numbered branches, commits, PR evidence, non-author human review and merge rules |
| [AGENTS](AGENTS.md) | Instructions and task routing for AI-assisted development |
| [SECURITY](SECURITY.md) | Private data, tokens, imports, vulnerability reporting and release gates |
| [PR template](.github/pull_request_template.md) | A concise structure for reviewable changes and honest verification evidence |

Before starting repository changes, create or confirm the task's tracking Issue, then use a branch named `<type>/<issue-number>-<kebab-case-description>`. Every PR, including a draft, must link that same primary Issue. See [the workflow and its one-time adoption record](CONTRIBUTING.md#2-issues-and-branches).

## Agreed product baseline

The core workflow is Web selection of whole trails, junction segments or partial segments with snapping/via points, or simpler online route combination on mobile; save a private plan, sync it to iPhone, download it, walk and record, then deliberately submit feedback and App-recorded completion evidence for administrator approval before publication. Preserve chosen segments and confirm connectors; reject disconnected or confirmed-closed selections. Start with one connected, field-testable pilot network whose location is still undecided. Scenario coverage replaces the initial route-count gate; 20–30 curated routes remain a later content target.

Guests retain browsing, local recording and downloaded-route use. Private GPX import/navigation, lock-screen off-route alerts, local history and GPX export remain in scope. Login is required for private-plan sync, condition reports and publication submissions. An incomplete hike can still produce a report; imported GPX alone cannot establish publication eligibility. Expired login must not block an existing offline hike. Confirmed closures block new planning, publication and starting planned navigation, while preserving map access, independent recording and ongoing hikes.

Raw tracks remain private by default; review receives only deliberately submitted route-relevant evidence. Public geometry changes require a new revision and review. Withdrawal/account deletion and reconnect cleanup must be verified before external release. Full backup/restore, automatic raw-history cloud backup, live sharing, offline/mid-hike replanning, automatic rerouting, voice turn-by-turn guidance and broader social features remain deferred. GPX export is not a full backup.

The team is planned as two to three people. The owner leads development with AI assistance and leads testing. Practical SQL learning is an explicit project goal; contributors remain responsible for understanding and explaining their changes.

## Confirmed technical direction

| Area | Baseline |
| --- | --- |
| Mobile | Swift + SwiftUI, iPhone, iOS 18+; UIKit where required |
| Web | React + TypeScript + Vite; public planner/reports and administrator console |
| Maps | Mapbox iOS SDK + Mapbox GL JS, conditional on technical and cost verification |
| Planning | Checked connected network, ordered segments and confirmed connectors; data source and graph/routing implementation still need validation |
| Recording and alerts | Core Location and local notifications, independent of map rendering |
| Local business data | SQLite + GRDB, parameterized SQL, stable IDs and versioned migrations |
| Structure | One modular app, lightweight MVVM and Swift Concurrency |
| Content | Versioned GeoJSON + JSON, network topology, immutable route revisions and offline snapshots; current metadata-only v1 remains a prototype |
| Exchange | GPX import/export using Foundation XML processing |
| Dependencies and checks | Swift Package Manager, Swift Testing, XCTest, Xcode diagnostics and real-device tests |
| Backend | Local Supabase: PostgreSQL + PostGIS + Auth + RLS; Supabase SDKs, explicit SQL and SQL migrations; no Prisma |
| Login and mail | Email/password with stable user IDs; captured local mail for team development, Resend later; real confirmation/recovery/deletion before external testing |

Keep user data separate from Mapbox's managed cache. Future changes remain possible when requirements justify them; assess their migration and verification impact. See [MVP requirements and acceptance](docs/MVP.md) for the full conditions.

## Cost and implementation status

**Current development must remain free.** Do not activate paid services or upgrade trials automatically. Pause affected service use when a free quota or trial ends. The post-deployment service budget remains a hard NZ$50/month; Mapbox's lack of an automatic spending cap is an unresolved production-release condition. Apple Developer Program membership is a later, separately budgeted distribution expense. Validate demand before choosing monetization.

The foundation includes `apps/mobile/HikingProject.xcodeproj`, a portable Swift/GRDB package and `apps/web/`. No planner, GL JS, backend/Auth/RLS, sync or publication system is installed or implemented. [Repository CI](.github/workflows/repository-checks.yml) checks documents, contribution conventions, React and portable Swift on the self-hosted Linux runner. It does not yet test backend permissions or migrations. iOS builds/UI tests run locally on Mac/Xcode. Follow the [development guide](docs/guides/DEVELOPMENT.md) and [actual validation evidence](docs/guides/FOUNDATION-VALIDATION.md); a tokenless sample build does not prove offline maps, recording or App Store readiness.

This is a public repository. The active [`protect-main` ruleset](https://github.com/RIOne1/HikingProject/settings/rules/27098958) requires a PR, one approving review, resolved review conversations and squash merging; it dismisses stale approvals and blocks force pushes and deletion, with no bypass actors. Both `Documentation integrity` and `Contribution policy` are required GitHub Actions checks, and the task branch must be up to date with `main`. See the [verified configuration and human merge duties](CONTRIBUTING.md#7-github-enforcement-setup); passing CI does not replace human approval. See [SECURITY.md](SECURITY.md#reporting-a-vulnerability) for confidential reporting and its verification limits.

## Team workflow and checks

Use the [Issue forms](.github/ISSUE_TEMPLATE/), now available in the default Issue chooser, for development tasks, bugs and technical validation, then track the Issue on the private [HikingProject MVP board](https://github.com/users/RIOne1/projects/1). The board is linked to this repository and shared with the current team; repository access does not automatically grant project access. See [CONTRIBUTING](CONTRIBUTING.md#8-project-board) for status meanings.

From the repository root, using Python 3.10+ and Git:

```bash
python3 scripts/ci/check_docs.py
python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v
git diff --check
```

These checks use Python's standard library and need no package installation. CI also validates PR metadata and commit subjects. Read the [coverage and verification limits](CONTRIBUTING.md#verification-evidence); green checks do not constitute human approval, proof of translation accuracy or app acceptance.

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
├── apps/
│   ├── mobile/  # SwiftUI app, Xcode project, portable core and tests
│   └── web/     # React catalogue foundation; planner/console are planned
├── shared/      # Synthetic catalogue fixture, JSON Schema and Swift resource
├── Package.swift / Package.resolved
├── package.json / package-lock.json
├── docs/
│   ├── MVP.md
│   ├── MVP.zh-CN.md
│   ├── guides/  # Development, mobile, web, data, CI and validation
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
