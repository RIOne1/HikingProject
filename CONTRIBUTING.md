# Contributing

These rules apply to every team member and every human-owned, AI-assisted contribution, including documentation and repository-policy changes. **MUST** is mandatory. **SHOULD** is the normal practice; explain a deviation in the PR. English is authoritative for governance files and PRs. [MVP.md](docs/MVP.md) is authoritative for product scope; its [Chinese mirror](docs/MVP.zh-CN.md) must be updated in the same PR when requirements change.

Read [AGENTS.md](AGENTS.md) before using an AI coding agent and [SECURITY.md](SECURITY.md) before handling tokens, tracks, logs, imports or vulnerabilities.

Every contributor MUST ensure their AI tool receives the applicable repository instructions; do not assume that every tool loads `AGENTS.md` automatically. Tool behaviour does not transfer the contributor's responsibility to the AI.

## 1. Human accountability and non-author approval

- Every change to `main` MUST go through a PR. This includes documentation, configuration, dependencies, data migrations and these rules.
- A PR MUST receive at least **one eligible non-author human approval of its current revision** before merge.
- An eligible approver is an authorized human reviewer with repository write access or higher who is not the PR author. Here, PR author means the person who opened the PR, not every commit author or contributor.
- Other contributors, including commit authors/co-authors and the latest pusher, MAY provide the required approval. They MUST review the whole current diff and verification evidence, including changes they contributed. Record contributions truthfully; shared implementation does not require a third reviewer.
- For example, if A opens a PR and both A and B contribute, B may review and approve the current revision, then A may squash-merge once all requirements are met. A cannot approve their own PR.
- AI review, bot approval, a checklist tick, an emoji or an informal message does not replace a GitHub human approval. If no eligible non-author human is available, wait for one.
- Any new commit after approval requires fresh non-author human review and approval, even if GitHub still displays an earlier approval. This also applies when the reviewer pushes the new commit. Resolve review conversations and blocking change requests before merge.
- These rules have no self-approval, administrator, emergency or documentation-only bypass. An available GitHub merge button does not establish policy compliance.
- Existing commit history is not rewritten just to conform to a newly adopted naming convention.

## 2. Issues and branches

Before creating a task branch or starting repository changes, contributors MUST create a tracking Issue in this repository, or use an existing open Issue that covers the assigned work. This includes code, documentation, configuration, tests and security fixes. Read-only investigation may inform the Issue; implementation and file edits must wait until the Issue exists. Record the problem, scope, acceptance criteria and verification approach. Follow [SECURITY.md](SECURITY.md) when an Issue concerns sensitive work.

Choose one primary Issue for each branch and PR. Its real GitHub Issue number MUST appear in the branch name and PR description; a PR number or `MVP-XX` requirement ID is not a substitute. Do not invent a number or open a duplicate Issue just to obtain one. Additional related Issues may be linked separately.

After the Issue exists, start the task from the latest `main` on a short-lived branch. If the assigned work requires an unmerged PR, first verify the latest `main`, then branch from that documented prerequisite. Keep the new PR targeted at `main`, disclose the inherited commits and provide an incremental comparison for reviewers. The human author must resolve the dependency/merge order and review the complete resulting diff before merge; this does not waive any Issue, naming, approval or verification rule. Inspect the working tree first; preserve unrelated work. Do not switch, reset, clean or stash someone else's changes to make a task convenient. Keep one coherent purpose per branch and PR. Do not reuse a branch after its PR is merged.

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

Do not push directly to `main`, force-push `main`, or delete it. AI agents must not force-push any branch. Humans must coordinate before rewriting a shared branch; a rewrite also invalidates previous approval.

**One-time adoption record:** [PR #1](https://github.com/RIOne1/HikingProject/pull/1) and its `docs/mvp-and-team-guidelines` branch predate this requirement. At the owner's request to continue the same PR, that existing head is retained and linked to [Issue #2](https://github.com/RIOne1/HikingProject/issues/2), which was created before the follow-up policy edits. Renaming an open PR's head [closes the PR](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/renaming-a-branch). This adoption record applies only to PR #1's original branch name and earlier work; all new tasks and branches must follow the Issue-first rule. It does not waive any review or merge requirement.

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

1. Create or confirm the primary tracking Issue before edits, with scope, acceptance criteria and verification approach. Identify affected `MVP-XX` requirements where applicable; cross-cutting work still needs an Issue but must not invent an MVP ID.
2. Read the current implementation, tests and nearest applicable instructions. Create or confirm the branch with that Issue's number and preserve existing work.
3. Implement a focused change. Keep important SQL parameterized, inspectable and explained. Schema changes need versioned migrations and representative recovery/migration evidence.
4. Run relevant available checks, inspect the whole diff and report limitations. Do not fabricate commands, outputs, screenshots or completed tests.
5. Open a Draft PR early when useful. An AI agent may prepare the draft under the assigned task. The human owner decides when it is ready for review; an agent may perform that transition only on the owner's explicit request. Ready status does not establish human inspection, approval or permission to merge.
6. Use the [PR template](.github/pull_request_template.md). State the problem and resulting behaviour, primary Issue, review focus, testing evidence, contributors, AI use and relevant risk/impact. Link the primary Issue in every PR, including drafts, and confirm its number matches the branch. Use `Closes #N` in the PR description when the PR fully addresses the Issue; for partial work, use `Refs #N` and identify remaining acceptance criteria. `Refs` is a reference, not an automatic-closing keyword. Other inapplicable sections may use `N/A` with a short reason; the primary Issue may not.
7. Keep the title and description aligned with the final implementation. Remove abandoned plans and misleading statements as the PR evolves.

All commits to a PR remain reviewable. Keep PRs small enough for another member to understand, but do not split a necessary migration or other inseparable change into misleading partial work.

### Verification evidence

For each meaningful check, give the exact command or manual scenario, environment/device/OS where relevant, result and remaining limitation. Distinguish **Passed**, **Failed**, **Not run** and **Not applicable**. A required check that was not run is not a pass. Fix relevant failures; do not weaken assertions or hide results to obtain a green status.

UI changes SHOULD include sanitized screenshots or a short recording. Location, offline-map, notification and long-running recording changes need relevant real-device evidence when applicable; a simulator or mocked service alone cannot prove outdoor/background reliability. Use synthetic or authorized fixtures rather than private tracks or home locations.

**Current bootstrap state:** the repository has no iOS project or application test suite yet. Repository CI exists for documentation and contribution checks only. Do not invent a scheme, target, `xcodebuild` command or `swift test` result. The app-bootstrap PR MUST add verified build/test instructions for the project it actually creates. For documentation-only changes, check meaning, bilingual parity, links and formatting; `git diff --check` is an existing formatting check. The research PDF generator is not an app test.

The [Repository checks workflow](.github/workflows/repository-checks.yml) uses the dedicated self-hosted Linux runner labeled `hikingproject-local-ci`. It pins the checkout action to a full commit SHA, uses read-only permissions and limits each job to five minutes. It needs only Git and Python 3.10+ and uses no artifact uploads, caches or app secrets. It runs on pushes to `main` and on creation, updates and relevant metadata edits for PRs from branches in this repository. Manual dispatch becomes available after the workflow reaches `main`. Jobs wait for the local runner to reconnect when it is offline.

Keep [fork workflow approval](https://github.com/RIOne1/HikingProject/settings/actions) set to require approval for all external contributors. Do not approve fork-origin workflow runs on this self-hosted runner. To run CI on an external contribution, review the proposed changes before bringing them onto a numbered branch in this repository.

- **Documentation integrity:** checks local inline Markdown links/heading anchors, trailing whitespace, matching bilingual MVP requirement IDs/order, one acceptance block per requirement, validator regression cases and changed-file whitespace. Run `python3 scripts/ci/check_docs.py`, `python3 -m unittest discover -s scripts/ci -p 'test_*.py' -v` and `git diff --check` locally with Python 3.10+ and Git. CI uses `git diff --check HEAD^ HEAD` to inspect committed changes against the checked-out commit's first parent.
- **Contribution policy:** checks Conventional Commit syntax for the PR title and included commit subjects, human account type, target `main`, numbered branch, matching visible primary Issue and `Closes #N`/`Refs #N` field, and that the number refers to an open Issue in this repository created before the PR. It reads the event JSON and GitHub API; metadata is not interpolated into shell commands. The specific PR #1 transition is the only branch/date exception. Its primary Issue and other checks still apply.
- **Human checks remain necessary:** CI cannot prove that local development began after Issue creation, that a user account is operated by its responsible human, that English text is imperative, that a translation preserves meaning, or that scope and fresh approval are correct. External URLs, full Markdown syntax and device behaviour are outside these checks. Keep inline link targets simple and URL-encode spaces/parentheses; the checker is not a general Markdown renderer.
- To reproduce the contribution check, save a real pull-request webhook-shaped JSON file and the GitHub Issue API response, then run `python3 scripts/ci/check_pr.py --event /path/to/event.json --issue-json /path/to/issue.json` in a checkout containing both base/head commits. Omit `--issue-json` to use a read-only API request. Do not commit credentials or local event captures.

Keep generated drafts, temporary files, local databases, tokens and build products out of commits. Curated research documents and their attribution sources under `docs/` are intentional project records. Follow [SECURITY.md](SECURITY.md) for exceptions involving authorized test data and for vulnerability reports.

## 5. AI-assisted development

AI tools may read, create the assigned task's tracking Issue, implement, validate, create a compliant Issue-numbered task branch, commit, push that task branch and open a Draft PR **within an explicitly assigned task**. They must create or verify the Issue before edits and include its number in the branch and PR. That autonomy is not authority to take unrelated work, overwrite existing changes or expand the agreed product.

PRs MUST be opened under the responsible member's own GitHub user account, not a shared or bot account. An authorized agent may open the draft using that member's account. If a tool can only open bot-authored PRs, it must prepare the draft and hand it to the human to open instead; this workflow does not assign an alternative merger to a bot-authored PR.

Humans remain responsible for understanding, reviewing and explaining the resulting changes, especially SQL, migrations, imported-file processing, location behaviour and permission handling. Each PR MUST state whether AI was used; if used, identify the tool(s), purposes/scope and what the submitting human checked. Full prompts or chat transcripts are not required and must not expose private information.

AI agents MUST NOT:

- Submit the required approval, impersonate a human reviewer, mark their own work approved, or merge a PR.
- Change repository visibility, collaborator permissions, protection/ruleset settings or approval requirements.
- Activate paid services or paid upgrades, change the free-development policy, or treat trial expiry as permission to pay.
- Force-push, perform destructive cleanup, remove unrelated work or rewrite shared history autonomously.
- Make baseline stack, scope or material data-contract changes silently. Explain them and obtain the necessary human scope decision and team review.
- Send secrets, private GPX tracks, local databases or unredacted logs to AI services or external tools without the relevant owner's explicit authorization.

Important dependencies, data migrations and architecture changes MUST be identified for human review. A task that legitimately implements an agreed dependency does not require repeated permission to perform routine local steps. A change to the agreed baseline does require an explicit decision.

## 6. Review and merge

The reviewer checks scope, correctness, actual evidence, SQL/data changes, privacy, cost implications and clarity across the whole current diff. They verify that they are eligible under section 1. Contributing implementation changes does not disqualify a non-author reviewer, but they must review and approve the resulting revision after the final commit.

After feedback, the author updates the PR, reruns affected checks, explains any conflict resolution and requests fresh review of the new revision. All review conversations must be resolved and outstanding blocking change requests addressed by the appropriate human reviewers.

**The human PR author performs Squash and merge only after:**

- The PR links its primary Issue, the branch carries that Issue's number, and the diff matches the Issue's scope and declared completion status, subject only to the specific adoption record in section 2.
- At least one eligible non-author human has approved the current revision in GitHub.
- All applicable required checks pass and the relevant local/manual evidence is recorded; no unresolved blocking limitation is disguised as `N/A`.
- Review conversations and blocking change requests are resolved.
- The branch is mergeable, the final diff is reviewed and the squash message is correct.

Delete the merged branch. Do not reuse it for the next task. Do not enable auto-merge as a way around the required human merge decision.

## 7. GitHub enforcement setup

**Verified on 12 November 2026:** this is a public personal repository. The active [`protect-main` ruleset](https://github.com/RIOne1/HikingProject/settings/rules/27098958) targets `main`, requires a PR and one approval, dismisses stale approvals on push, requires resolved review conversations, permits only squash merging, and blocks force pushes and deletion. Its bypass list is empty. PR #1 visibly requires approval and cannot merge without it. Force-push and deletion settings were inspected, not destructively tested.

Maintain the following configuration. File-based policy does not configure GitHub, and settings can change independently of this document.

- Protect `main` with an active ruleset or equivalent branch protection; require a PR and at least one human approving review.
- Enable dismissal of stale approvals when changes are pushed. Team policy still requires a fresh approval after every new commit, even when GitHub retains an approval because the diff is unchanged.
- Leave `Require approval of the most recent reviewable push` disabled for this small-team policy. It excludes the latest pusher: if A opens the PR and B pushes the final changes, it can prevent B from supplying the approval while A cannot self-approve.
- Require resolution of review conversations. Add required status checks only when the actual, documented workflows exist; do not invent check names.
- Block force pushes and deletion. Apply the requirements to administrators as supported, and do not grant bypass permissions that defeat non-author human review.
- Permit squash merging and disable merge-commit/rebase merging for PRs. Linear-history protection alone does not mean squash-only.
- Keep automated merging disabled and delete merged task branches.
- Recheck the configured behaviour after changing protection settings. Do not use destructive test pushes or deletions.

The required separation is between the PR author and the human approver; this policy does not exclude other contributors or commit co-authors. Before merging, the human author must verify the approver's eligibility and that approval covers the current revision. CI checks branch numbering and the visible Issue relationship as described above. Humans must still verify the Issue existed before development, review scope and check approval freshness. A green merge button or checklist is not a substitute for these checks.

**CI rollout boundary:** `Documentation integrity` and `Contribution policy` are the new workflow's actual job names. They are not yet registered as required ruleset checks. PR #1 and the CI bootstrap PR remain unmerged, so `main` does not yet contain this workflow. Requiring these checks now would leave PR #1 waiting for jobs its branch does not define. After the human-approved bootstrap merge, verify runs on `main` and a subsequent PR, then add those exact GitHub Actions checks to `protect-main` without weakening the existing approval requirements. This is an explicit pending setup step, not a claim of complete CI enforcement. Team policy already requires all applicable checks to pass.

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

The [Issue forms](.github/ISSUE_TEMPLATE/) cover development tasks, bugs and technical validation. They request scope/reproduction, relevant MVP IDs, acceptance and verification; keep uncertain checks marked Not run. The default chooser uses them after merge to `main`. Disabling blank Issues is a UI aid, not enforcement against maintainers or API-created Issues; all tracking Issues must still carry the required information. Keep security reports in the private channel described by SECURITY.md.
