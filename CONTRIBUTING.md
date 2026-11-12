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

## 2. Branches

Start each task from the latest `main` on a short-lived branch. Inspect the working tree first; preserve unrelated work. Do not switch, reset, clean or stash someone else's changes to make a task convenient. Keep one coherent purpose per branch and PR. Do not reuse a branch after its PR is merged.

Branch format:

```text
<type>/<kebab-case-description>
<type>/<issue-number>-<kebab-case-description>
```

Use lowercase ASCII words and hyphens. An Issue number is optional; link an existing Issue when relevant. The description MUST identify the work rather than the person or tool performing it.

| Branch type | Purpose | Example |
| --- | --- | --- |
| `feature` | New product behaviour | `feature/12-offline-map-download` |
| `fix` | Correct existing behaviour | `fix/gpx-time-parsing` |
| `docs` | Documentation | `docs/mvp-and-team-guidelines` |
| `refactor` | Restructure without an intended behaviour change | `refactor/location-session-boundaries` |
| `test` | Test coverage or fixtures | `test/track-migration-recovery` |
| `chore` | Routine maintenance | `chore/research-directory-cleanup` |
| `build` | Build/dependency configuration | `build/lock-mapbox-sdk-version` |
| `ci` | CI configuration within the cost policy | `ci/document-checks` |
| `perf` | Measured performance work | `perf/track-point-query-index` |
| `revert` | Revert a defined change | `revert/catalogue-import-regression` |

Do not use tool or person namespaces such as `codex/...`, `chatgpt/...`, `claude/...`, `ai/...` or a member's name as the prefix. A tool's default branch suggestion does not override this rule. Use `feature/` for a feature branch, not `feat/`; the commit type below remains `feat`.

Do not push directly to `main`, force-push `main`, or delete it. AI agents must not force-push any branch. Humans must coordinate before rewriting a shared branch; a rewrite also invalidates previous approval.

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

1. Identify the task, its affected `MVP-XX` requirements and relevant contracts. For cross-cutting work, explain the purpose rather than inventing an MVP ID or Issue.
2. Read the current implementation, tests and nearest applicable instructions. Confirm the branch and preserve existing work.
3. Implement a focused change. Keep important SQL parameterized, inspectable and explained. Schema changes need versioned migrations and representative recovery/migration evidence.
4. Run relevant available checks, inspect the whole diff and report limitations. Do not fabricate commands, outputs, screenshots or completed tests.
5. Open a Draft PR early when useful. An AI agent may prepare the draft under the assigned task; a human owner checks it and makes it ready for review.
6. Use the [PR template](.github/pull_request_template.md). State the problem and resulting behaviour, review focus, testing evidence, contributors, AI use and relevant risk/impact. Mark inapplicable sections `N/A` with a short reason.
7. Keep the title and description aligned with the final implementation. Remove abandoned plans and misleading statements as the PR evolves.

All commits to a PR remain reviewable. Keep PRs small enough for another member to understand, but do not split a necessary migration or other inseparable change into misleading partial work.

### Verification evidence

For each meaningful check, give the exact command or manual scenario, environment/device/OS where relevant, result and remaining limitation. Distinguish **Passed**, **Failed**, **Not run** and **Not applicable**. A required check that was not run is not a pass. Fix relevant failures; do not weaken assertions or hide results to obtain a green status.

UI changes SHOULD include sanitized screenshots or a short recording. Location, offline-map, notification and long-running recording changes need relevant real-device evidence when applicable; a simulator or mocked service alone cannot prove outdoor/background reliability. Use synthetic or authorized fixtures rather than private tracks or home locations.

**Current bootstrap state:** the repository has no iOS project, application test suite or CI workflow yet. Do not invent a scheme, target, `xcodebuild` command or `swift test` result. The app-bootstrap PR MUST add verified build/test instructions for the project it actually creates. For documentation-only changes, check meaning, bilingual parity, links and formatting; `git diff --check` is an existing formatting check. The research PDF generator is not an app test.

Keep generated drafts, temporary files, local databases, tokens and build products out of commits. Curated research documents and their attribution sources under `docs/` are intentional project records. Follow [SECURITY.md](SECURITY.md) for exceptions involving authorized test data and for vulnerability reports.

## 5. AI-assisted development

AI tools may read, implement, validate, create a purpose-named task branch, commit, push that task branch and open a Draft PR **within an explicitly assigned task**. That autonomy is not authority to take unrelated work, overwrite existing changes or expand the agreed product.

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

- At least one eligible non-author human has approved the current revision in GitHub.
- All applicable required checks pass and the relevant local/manual evidence is recorded; no unresolved blocking limitation is disguised as `N/A`.
- Review conversations and blocking change requests are resolved.
- The branch is mergeable, the final diff is reviewed and the squash message is correct.

Delete the merged branch. Do not reuse it for the next task. Do not enable auto-merge as a way around the required human merge decision.

## 7. GitHub enforcement setup

**Observed on 12 November 2026:** this is a private personal repository; `main` returned `Branch not protected`; repository rulesets were empty. All three merge methods were enabled and auto-merge was disabled. The account plan was not established. These files do not change those settings.

The repository owner must configure and verify the following before declaring the workflow technically enforced. Until then, the team still MUST obey the rules manually; the current gap is not a waiver.

- Protect `main` with an active ruleset or equivalent branch protection; require a PR and at least one human approving review.
- Enable dismissal of stale approvals when changes are pushed. Team policy still requires a fresh approval after every new commit, even when GitHub retains an approval because the diff is unchanged.
- Leave `Require approval of the most recent reviewable push` disabled for this small-team policy. It excludes the latest pusher: if A opens the PR and B pushes the final changes, it can prevent B from supplying the approval while A cannot self-approve.
- Require resolution of review conversations. Add required status checks only when the actual, documented workflows exist; do not invent check names.
- Block force pushes and deletion. Apply the requirements to administrators as supported, and do not grant bypass permissions that defeat non-author human review.
- Permit squash merging and disable merge-commit/rebase merging for PRs. Linear-history protection alone does not mean squash-only.
- Keep automated merging disabled and delete merged task branches.
- Verify the configured behaviour using a harmless test PR before marking this setup complete.

The required separation is between the PR author and the human approver; this policy does not exclude other contributors or commit co-authors. Before merging, the human author must verify the approver's eligibility and that approval covers the current revision. A green merge button or checklist is not a substitute for these checks.

Public repositories can use these protections on GitHub Free; private personal repositories need an eligible plan such as Pro. Verify existing entitlement first. Do not change visibility or buy a plan merely to bypass the free-development constraint. Resolve an unavailable enforcement path with the owner; do not claim the policy is technically enforced. Owners can still edit repository settings, so policy also prohibits weakening them to merge one's own work.

References: [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [ruleset review settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [squash configuration](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests), [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
