<!-- Use an English Conventional Commit title, e.g. feat(tracking): persist recorded points locally. -->
<!-- Keep the description current. Never include secrets, personal tracks or unredacted logs. -->

## Problem and result

<!-- What concrete problem does this fix, and what will a user or contributor observe afterward? -->

## Scope and review focus

- MVP requirement(s): <!-- MVP-XX, or explain cross-cutting/documentation scope. -->
- Related Issue: <!-- Link if one exists; otherwise N/A. -->
- Changes and files to focus on:
- Contributors to this PR: <!-- All human authors/co-authors/contributors, not only the person who pushed. -->

## Verification evidence

<!-- Give exact commands or manual scenarios. Do not invent commands for an app project that does not exist yet. -->
<!-- Result: Passed / Failed / Not run (reason) / Not applicable (reason). Add rows only as needed. -->

| Command or scenario | Environment / device / OS | Result and evidence |
| --- | --- | --- |
| | | |

## Relevant impacts

<!-- Keep relevant details; use N/A with a short reason for the other items. -->

- UI / offline / location changes: <!-- Sanitized visual or real-device evidence and relevant limitations. -->
- SQL / data / GPX changes: <!-- Important queries, schema/migration effects, compatibility and recovery evidence. -->
- Dependencies / permissions / privacy / costs: <!-- Explain changes; current development must remain free. -->
- Risks and recovery: <!-- Remaining limitations and a practical rollback/recovery path, especially for data changes. -->
- Documentation: <!-- Changed files; keep English and Chinese MVP versions aligned if meaning changes. -->

## AI assistance and human review

- AI used: <!-- Yes / No. -->
- Tools and scope: <!-- Tool(s) and what they assisted with; no full chat transcript is needed. -->
- Human verification: <!-- What the submitting human inspected, tested and can explain; include relevant SQL. -->

## Author checklist

- [ ] The branch describes the work, the title follows the commit convention, and the PR targets `main`.
- [ ] The submitting human has inspected the entire diff and the scope matches the linked requirements.
- [ ] Verification and limitations above are accurate; missing required checks are not presented as passed.
- [ ] Relevant documentation and both MVP versions are aligned, or the reason for N/A is stated.
- [ ] The change contains no live credentials, unauthorized private data, local databases or accidental generated artifacts.
- [ ] Contributors and AI assistance are recorded truthfully; non-author human review has been requested.

## Merge requirements

- **Current revision approved:** at least one authorized human with repository write access or higher, other than the PR author, must approve the current revision in GitHub.
- **Contributors may review:** another member may approve even if they authored/co-authored commits or pushed the latest changes. They must review the whole current diff and verification evidence. The PR author cannot self-approve.
- **New commit means new review:** after every new commit, obtain fresh non-author human review and approval, including when the reviewer pushed it. An earlier approval does not cover the new revision.
- **Checks and feedback complete:** all applicable required checks pass, relevant verification evidence is recorded, and review conversations and blocking change requests are resolved.
- **Human author merges:** only the human PR author may squash-merge after all requirements are met and the branch is mergeable. AI review, bot approval and checklist ticks do not count as the required approval.

See `CONTRIBUTING.md` for the full policy.
