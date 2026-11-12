# Contributing

These rules apply to every team member and every human-owned, AI-assisted contribution, including documentation and repository-policy changes. **MUST** is mandatory. **SHOULD** is the normal practice; explain a deviation in the PR. English is authoritative for governance files and PRs. [MVP.md](docs/MVP.md) is authoritative for product scope; its [Chinese mirror](docs/MVP.zh-CN.md) must be updated in the same PR when requirements change.

This file is the source of team workflow rules. [AGENTS.md](AGENTS.md) adds AI execution guidance; the [PR template](.github/pull_request_template.md) collects evidence and summarizes merge gates. Give AI tools the applicable instructions rather than assuming they load them automatically. Read [SECURITY.md](SECURITY.md) for tokens, tracks, imports, logs and vulnerabilities.

## 1. Human accountability and non-author approval

- Every change to `main`, including documentation and these rules, MUST go through a PR with **at least one eligible non-author human approval of its current revision**.
- The approver MUST have repository write access or higher and be someone other than the person who opened the PR. Commit authors/co-authors and the latest pusher MAY approve after reviewing the whole current diff and evidence, including their own changes; shared implementation does not require a third person.
- Every new commit requires fresh non-author human review and approval, including a reviewer's push, even if GitHub retains an earlier approval.
- AI/bot review, checklists and informal messages do not replace GitHub human approval. If no eligible approver is available, wait. There is no self-approval, administrator, emergency or documentation-only bypass.
- Only the human PR author may squash-merge after the [merge gates](#6-review-and-merge) pass. An enabled merge button does not establish compliance.

## 2. Issues and branches

Before creating a task branch or starting repository changes, contributors MUST create a tracking Issue in this repository, or use an existing open Issue that covers the assigned work. This includes code, documentation, configuration, tests and security fixes. Read-only investigation may inform the Issue; implementation and file edits must wait until the Issue exists. Record the problem, scope, acceptance criteria and verification approach. Follow [SECURITY.md](SECURITY.md) when an Issue concerns sensitive work.

Choose one primary Issue for each branch and PR. Its real GitHub Issue number MUST appear in the branch name and PR description; a PR number or `MVP-XX` requirement ID is not a substitute. Do not invent a number or open a duplicate Issue just to obtain one. Additional related Issues may be linked separately.

After the Issue exists, start a short-lived task branch from the latest `main`. If work depends on an unmerged PR, verify `main`, branch from the documented prerequisite, target `main` and provide both the dependency and an incremental comparison. The human author must resolve merge order and review the complete resulting diff. Keep one coherent purpose per branch/PR and do not reuse a merged branch. Inspect the working tree first; do not switch, reset, clean or stash someone else's changes to make the task convenient.

Required branch format:

```text
<type>/<issue-number>-<kebab-case-description>
```

Use the positive numeric Issue number without `#`, lowercase ASCII words and hyphens. The description MUST identify the work rather than the person or tool performing it. The following numbers illustrate the format; replace them with the actual primary Issue number before creating a branch.

| Branch type | Purpose | Example |
| --- | --- | --- |
| `feature` | New product behaviour | `feature/12-offline-map-download` |
| `fix` | Correct existing behaviour | `fix/13-gpx-time-parsing` |
| `docs` | Documentation | `docs/14-mvp-and-team-guidelines` |
| `refactor` | Restructure without an intended behaviour change | `refactor/15-location-session-boundaries` |
| `test` | Test coverage or fixtures | `test/16-track-migration-recovery` |
| `chore` | Routine maintenance | `chore/17-research-directory-cleanup` |
| `build` | Build/dependency configuration | `build/18-lock-mapbox-sdk-version` |
| `ci` | CI configuration within the cost policy | `ci/19-document-checks` |
| `perf` | Measured performance work | `perf/20-track-point-query-index` |
| `revert` | Revert a defined change | `revert/21-catalogue-import-regression` |

Do not use tool or person namespaces such as `codex/...`, `chatgpt/...`, `claude/...`, `ai/...` or a member's name as the prefix. A tool's default branch suggestion does not override this rule. Use `feature/` for a feature branch, not `feat/`; the commit type below remains `feat`.

Do not push directly to `main`, force-push `main`, or delete it. AI agents must not force-push any branch. Humans must coordinate before rewriting a shared branch; a rewrite also invalidates previous approval. Do not rewrite existing history just to adopt a new naming convention.

**One-time adoption record:** [PR #1](https://github.com/RIOne1/HikingProject/pull/1) and its `docs/mvp-and-team-guidelines` branch predate this requirement. At the owner's request to continue the same PR, that head was retained and linked to [Issue #2](https://github.com/RIOne1/HikingProject/issues/2), which was created before the follow-up policy edits. PR #1 has since been merged. Renaming an open PR's head [closes the PR](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/renaming-a-branch). This adoption record applies only to PR #1's original branch name and earlier work; all new tasks and branches must follow the Issue-first rule. It does not waive any review or merge requirement.

## 3. Commit messages and PR titles

Every new commit and PR title MUST use the project's Conventional Commits form:

```text
type(optional-scope)!: imperative description
```

The scope and `!` are optional. Allowed types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf` and `revert`. Use a meaningful optional scope such as `tracking`, `maps`, `gpx`, `storage` or `catalogue`.

```text
feat(tracking): persist recorded points locally
fix(gpx): reject invalid coordinates
docs(mvp): clarify offline acceptance criteria
```

- Use English, a specific imperative description and no trailing full stop. SHOULD keep the header within 72 characters.
- Do not use vague descriptions such as `update`, `changes`, `fix stuff`, `WIP` or `AI generated` as the whole description.
- Use a body when reviewers need the reason, behaviour change, verification or migration implications. Break up unrelated work rather than disguising it in a long message.
- Identify breaking changes with `!` or a `BREAKING CHANGE:` footer and explain the migration/compatibility impact. Normal use of `!` is not an exception to documenting that impact.
- Branch synchronization and revert commits also need a meaningful conforming message; edit generated default messages if needed.
- Use truthful authorship and co-author information. Add a human co-author only for a real contribution and with their agreement. AI assistance is disclosed in the PR; do not invent human or tool ownership.
- The final squash message MUST conform and accurately describe the final PR. Review its generated body to remove abandoned approaches, stale checklists and misleading attribution before merging.

## 4. Work and PR preparation

1. Follow the Issue/branch rules in section 2; identify affected `MVP-XX` requirements without inventing IDs for cross-cutting work. Read the current implementation, tests and applicable instructions.
2. Implement a focused change. Keep SQL parameterized, inspectable and explained; schema changes need versioned migrations and representative recovery/migration evidence. Apply the tests and verification guidance below.
3. Open a Draft PR early when useful. The human owner decides when it is ready for review; an agent may change that status only on the owner's explicit request. Ready status is not approval or permission to merge.
4. Use the [PR template](.github/pull_request_template.md) for the result, review focus, evidence, contributors, AI use and relevant impacts. Keep required fields; group inapplicable impact categories under one reasoned `N/A` instead of repeating boilerplate. Drafts may record planned work and unchecked items honestly.
5. Every PR MUST link its primary Issue and match the branch number. Fill `Primary Issue (required)` and `Issue relationship` once each, with values on the same line. Use `Closes #N` for completed Issue scope or `Refs #N` with remaining criteria explained; `Refs` does not auto-close an Issue. These fields cannot be `N/A`. List other related Issues separately.
6. Keep the title, description and evidence aligned with the final change; remove abandoned plans and stale claims before requesting review.

All commits to a PR remain reviewable. Keep PRs small enough for another member to understand, but do not split a necessary migration or other inseparable change into misleading partial work.

### Tests and CI belong with the change

- Changes with meaningful regression risk (such as business rules, SQL/migrations, imports or permissions) MUST include relevant automated tests in the same PR where reliable automation is practical. Bug fixes need an automated regression test when reproducible that way; otherwise explain the limitation and suitable verification. Test observable behaviour and failure cases, not a copy of the implementation.
- Applicable PR CI MUST execute new/changed automated checks. Existing discovery needs no workflow edit; otherwise update commands, filters, dependencies or runner configuration in the same PR. Reuse existing jobs where suitable and justify extra jobs or tooling with a concrete requirement or risk. Do not defer required CI integration to an unspecified later task.
- Identify the tests, covering CI job and results in the PR. If no automated test or CI change is appropriate, explain why; prose-only and other low-impact changes do not need artificial tests or a new workflow. Do not activate paid infrastructure or silently substitute runners.

### Verification evidence

For each meaningful check, give the exact command or manual scenario, relevant environment/device/OS, result and limitations. Distinguish **Passed**, **Failed**, **Not run** (reason) and **Not applicable** (justification). Never fabricate evidence, weaken assertions or hide failures to obtain a green status.

Identify the gate each check supports. Missing or failed checks required for the current PR block merge. Product-acceptance and public-release checks block those milestones; they are not automatically required for unrelated documentation or incremental PRs. Record unavailable checks and any follow-up Issue without claiming the associated feature or milestone is complete. This distinction does not waive MVP or SECURITY requirements, and a follow-up Issue is not a substitute for a required check.

UI changes SHOULD include sanitized screenshots or a short recording. Changes affecting location, offline-map, notification or long-running recording behaviour need relevant real-device evidence; CI, simulators and mocks alone cannot prove outdoor/background or battery claims. Use synthetic or authorized fixtures rather than private tracks or home locations.

**Application baseline:** the repository now contains a SwiftUI iOS project, portable Swift/GRDB tests and a React/TypeScript/Vite workspace. Use the [development guide](docs/guides/DEVELOPMENT.md) and its Mobile/Web/Data guides for actual commands and boundaries. For documentation-only changes, check meaning, bilingual parity, links and `git diff --check`; the research PDF generator is not an app test.

The [Repository checks workflow](.github/workflows/repository-checks.yml) uses the dedicated self-hosted Linux runner labeled `hikingproject-local-ci`. Actions are pinned to full commit SHAs, tokens are read-only, and no artifact uploads, GitHub caches or app secrets are used. The broader documentation/application job has a 20-minute limit; contribution checks have five minutes. The [CI runner guide](docs/guides/CI.md) records Node/Swift versions and native prerequisites. It runs on pushes to `main` and on creation, updates and relevant metadata edits for PRs from branches in this repository, and supports manual dispatch. Jobs wait for the local runner to reconnect when it is offline.

Keep [fork workflow approval](https://github.com/RIOne1/HikingProject/settings/actions) set to require approval for all external contributors. Do not approve fork-origin workflow runs on this self-hosted runner. To run CI on an external contribution, review the proposed changes before bringing them onto a numbered branch in this repository.

There is no automatic fallback to an official runner. Follow [SECURITY.md](SECURITY.md#self-hosted-ci) for host isolation and the limits of the fork filter. Linux checks test the portable Swift library but do not build the iPhone app: iOS builds/UI tests currently use a local [macOS/Xcode environment](https://developer.apple.com/xcode/system-requirements). The owner's self-hosting choice is not required to avoid a public-repository compute quota: [GitHub's billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions) states that standard hosted runners for public repositories and self-hosted runners are independently free; larger runners and storage have separate billing rules. Keep this workflow free of artifact uploads and caches.

- **Documentation integrity:** retains its existing required-check name and covers local inline Markdown links/heading anchors, trailing whitespace, matching bilingual MVP IDs/order, one acceptance block per requirement, validator regression cases and changed-file whitespace. It also runs `npm ci`, `npm run check:web` and locked portable Swift/GRDB tests; these are mandatory steps, not optional extra checks. Run `python3 scripts/ci/check_docs.py`, `python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v` and `git diff --check` locally with Python 3.10+ and Git. CI uses `git diff --check HEAD^ HEAD` to inspect committed changes against the checked-out commit's first parent.
- **Contribution policy:** checks Conventional Commit syntax for the PR title and included commit subjects, human account type, target `main`, numbered branch, matching visible primary Issue and `Closes #N`/`Refs #N` field, and that the number refers to an open Issue in this repository created before the PR. It reads the event JSON and GitHub API; metadata is not interpolated into shell commands. The specific PR #1 transition is the only branch/date exception. Its primary Issue and other checks still apply.
- **Human checks remain necessary:** CI cannot prove that local development began after Issue creation, that a user account is operated by its responsible human, that English text is imperative, that a translation preserves meaning, or that scope and fresh approval are correct. External URLs, full Markdown syntax and device behaviour are outside these checks. Keep inline link targets simple and URL-encode spaces/parentheses; the checker is not a general Markdown renderer.
- To reproduce the contribution check, save a real pull-request webhook-shaped JSON file and the GitHub Issue API response, then run `python3 scripts/ci/check_pr.py --event /path/to/event.json --issue-json /path/to/issue.json` in a checkout containing both base/head commits. Omit `--issue-json` to use a read-only API request. Do not commit credentials or local event captures.

Keep generated drafts, temporary files, local databases, tokens and build products out of commits. Curated research documents and their attribution sources under `docs/` are intentional project records. Follow [SECURITY.md](SECURITY.md) for exceptions involving authorized test data and for vulnerability reports.

## 5. AI-assisted development

Within an explicitly assigned task, AI tools may create its Issue and compliant branch, implement, validate, commit, push and open a Draft PR. They remain subject to sections 2–4 and must not expand scope or overwrite unrelated work.

PRs MUST use the responsible member's own GitHub user account. An authorized agent may open a draft under that account; if a tool only opens bot-authored PRs, prepare the content for the human to open.

Humans remain responsible for understanding and explaining the changes, including relevant SQL, imports, location and permission handling. Each PR MUST state whether AI was used; if so, name its tools/scope and what the human actually verified. Full prompts or chat transcripts are unnecessary; do not expose private information.

AI agents MUST NOT:

- Submit the required approval, impersonate a human reviewer, mark their own work approved, or merge a PR.
- Change repository visibility, collaborator permissions, protection/ruleset settings or approval requirements.
- Activate paid services or paid upgrades, change the free-development policy, or treat trial expiry as permission to pay.
- Force-push, perform destructive cleanup, remove unrelated work or rewrite shared history autonomously.
- Make baseline stack, scope or material data-contract changes silently. Explain them and obtain the necessary human scope decision and team review.
- Send secrets, private GPX tracks, local databases or unredacted logs to AI services or external tools without the relevant owner's explicit authorization.

Important dependencies, data migrations and architecture changes MUST be identified for human review. A task that legitimately implements an agreed dependency does not require repeated permission to perform routine local steps. A change to the agreed baseline does require an explicit decision.

## 6. Review and merge

The reviewer checks scope, correctness, evidence, maintainability, SQL/data changes, privacy and costs across the current diff, applying the eligibility and fresh-approval rules in section 1.

After feedback, the author updates the PR, reruns affected checks, explains any conflict resolution and requests fresh review of the new revision. All review conversations must be resolved and outstanding blocking change requests addressed by the appropriate human reviewers.

**The human PR author performs Squash and merge only after:**

- The PR links its primary Issue, the branch carries that Issue's number, and the diff matches the Issue's scope and declared completion status, subject only to the specific adoption record in section 2.
- At least one eligible non-author human has approved the current revision in GitHub.
- Checks required for the current PR pass and relevant local/manual evidence is recorded; no unresolved blocking limitation is disguised as `N/A`.
- Review conversations and blocking change requests are resolved.
- The branch is mergeable, the final diff is reviewed and the squash message is correct.

Delete the merged branch. Do not reuse it for the next task. Do not enable auto-merge as a way around the required human merge decision.

## 7. GitHub enforcement setup

**Verified on 12 November 2026:** this is a public personal repository. The active [`protect-main` ruleset](https://github.com/RIOne1/HikingProject/settings/rules/27098958) targets `main`, requires a PR and one approval, dismisses stale approvals on push, requires resolved review conversations, permits only squash merging, and blocks force pushes and deletion. It also requires `Documentation integrity` and `Contribution policy`, with GitHub Actions as their expected source, and requires branches to be up to date with `main`. Its bypass list is empty. Force-push and deletion settings were inspected, not destructively tested.

Maintain the following configuration. File-based policy does not configure GitHub, and settings can change independently of this document.

- Protect `main` with an active ruleset or equivalent branch protection; require a PR and at least one human approving review.
- Enable dismissal of stale approvals when changes are pushed. Team policy still requires a fresh approval after every new commit, even when GitHub retains an approval because the diff is unchanged.
- Leave `Require approval of the most recent reviewable push` disabled for this small-team policy. It excludes the latest pusher: if A opens the PR and B pushes the final changes, it can prevent B from supplying the approval while A cannot self-approve.
- Require resolution of review conversations and both repository checks named above from GitHub Actions. Keep **Require branches to be up to date before merging** enabled. If `main` advances, update the task branch and rerun checks; the new commit also needs fresh human approval.
- Keep required check names aligned with actual workflow jobs. Coordinate any job rename with the ruleset update so that a required check is not left permanently missing. An offline runner leaves checks queued and blocks merging; restore the runner rather than remove the requirement or substitute paid infrastructure.
- Block force pushes and deletion. Apply the requirements to administrators as supported, and do not grant bypass permissions that defeat non-author human review.
- Keep `protect-main`'s allowed merge methods set to squash only. Repository-wide merge-commit/rebase options are still enabled, but the ruleset disallows those methods for PRs targeting `main`.
- Keep auto-merge disabled. Delete merged task branches manually; automatic branch deletion is currently off.
- Recheck the configured behaviour after changing protection settings. Do not use destructive test pushes or deletions.

Settings and CI do not establish human identity, Issue-before-development order or complete review. The author and reviewer must still apply the human merge duties in section 6.

**CI enforcement record:** [PR #4](https://github.com/RIOne1/HikingProject/pull/4) is merged and the workflow is on `main`. Its [post-merge run](https://github.com/RIOne1/HikingProject/actions/runs/43195730432) passed documentation checks; the PR-only contribution check was correctly skipped on that push. Under [Issue #5](https://github.com/RIOne1/HikingProject/issues/5), ruleset readback and the effective `main` rules confirm both required check names, the observed GitHub Actions app ID `15368`, strict synchronization and unchanged prior protections.

Verification in [PR #6](https://github.com/RIOne1/HikingProject/pull/6) covered a real [failed contribution check](https://github.com/RIOne1/HikingProject/actions/runs/43197804348) caused by malformed Issue-link metadata, followed by [both checks passing](https://github.com/RIOne1/HikingProject/actions/runs/43197968521) after correction. At probe commit `a2b6efe`, temporarily removing the workflow from the Draft branch produced no check runs; GitHub displayed both checks as **Required — Expected**, waiting for results, and the API reported `BLOCKED`. The workflow was then restored byte-for-byte. The PR records current-head results and the remaining human approval gate. All probes kept the PR in Draft; no approval, merge attempt, main push or destructive protection test was performed. Passing CI does not replace the required non-author human approval.

Public repositories can use these protections on GitHub Free; private personal repositories need an eligible plan such as Pro. Verify existing entitlement first. Do not change visibility or buy a plan merely to bypass the free-development constraint. Resolve an unavailable enforcement path with the owner; do not claim the policy is technically enforced. Owners can still edit repository settings, so policy also prohibits weakening them to merge one's own work.

References: [Issue/PR linking](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue), [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [ruleset review settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [squash configuration](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests), [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## 8. Project board

Use the private [HikingProject MVP board](https://github.com/users/RIOne1/projects/1), linked from the repository's Projects tab. As configured on 12 November 2026, RIOne1 is the project admin and the owner authorized Write access for the existing member FakeReality666. Project access is separate from repository permissions; ask the owner to grant future members access rather than publishing private project content.

| Status | Meaning |
| --- | --- |
| Backlog | Captured; scope or priority still needs triage |
| Ready | Scope, acceptance, verification and dependencies are clear |
| In progress | Work is underway, including Draft PRs |
| In review | The human owner has requested review of the prepared implementation/evidence |
| Done | Acceptance is complete and any required human-approved PR is merged |

The board imports open HikingProject Issues and has a repository-scoped auto-add workflow. Create a real Issue before development; draft project cards do not supply an Issue number. Use one Issue card as the task record and link its PR to avoid duplicate tracking. Update status when work changes. Board labels and automatic state changes do not establish acceptance or approval: verify the linked evidence before treating an item as Done. The default automation that closes an Issue when a card moves to Done is disabled; changing a column must not silently close work.

The [Issue forms](.github/ISSUE_TEMPLATE/) are available in the default chooser and cover development tasks, bugs and technical validation. They request scope/reproduction, relevant MVP IDs, acceptance and verification; keep uncertain checks marked Not run. Disabling blank Issues is a UI aid, not enforcement against maintainers or API-created Issues; all tracking Issues must still carry the required information. Keep security reports in the private channel described by SECURITY.md.
