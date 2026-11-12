<!-- Use an English Conventional Commit title, e.g. feat(tracking): persist recorded points locally. -->
<!-- Keep the description current. Never include secrets, personal tracks or unredacted logs. -->

## Problem and result

<!-- What concrete problem does this fix, and what will a user or contributor observe afterward? -->

## Scope and review focus

- MVP requirement(s): <!-- MVP-XX, or explain cross-cutting/documentation scope. -->
- Primary Issue (required): <!-- Use #N or [#N](https://github.com/RIOne1/HikingProject/issues/N). Match the branch number; N/A is not allowed. -->
- Issue relationship: <!-- Fill this field once, on this line: Closes #N for completed scope, or Refs #N and explain remaining work. Put additional related Issues elsewhere. -->
- Changes and files to focus on:
- Dependencies on open PRs: <!-- N/A, or link the prerequisite PR and identify the incremental diff; target main and explain merge order. -->
- Contributors to this PR: <!-- Human contributions; disclose AI separately below. -->

## Verification evidence

- Tests and CI coverage: <!-- Tests added/updated and covering CI job, or justified N/A. Existing discovery may need no workflow edit. Identify current PR blockers separately from later acceptance/release checks and link any follow-up Issue. -->

<!-- Give exact commands or manual scenarios. Do not invent commands for an app project that does not exist yet. -->
<!-- Result: Passed / Failed / Not run (reason) / Not applicable (reason). Add rows only as needed. -->

| Command or scenario | Environment / device / OS | Result and evidence |
| --- | --- | --- |
| | | |

## Relevant impacts

<!-- Keep relevant fields. Group inapplicable impacts under one N/A explanation. -->

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

<!-- Complete before merge; Draft PRs may honestly leave items unchecked. Approval belongs in GitHub review, not this checklist. -->

- [ ] The Issue predates the work, the purpose-named branch contains its number, this PR links it, the title follows Conventional Commits and the target is `main`.
- [ ] The submitting human has inspected the whole diff, scope, relevant risks and absence of secrets or unauthorized data/artifacts.
- [ ] Required tests/CI integration and relevant manual evidence are included; checks required for this PR pass, and limitations or N/A are explained above.
- [ ] Relevant documentation is updated, including both MVP versions when requirements change; contributor and AI disclosures are accurate.

## Merge requirements

- **Current revision approved:** at least one non-author human with write access or higher must approve in GitHub after reviewing the whole diff and evidence. Contributors/co-authors and the latest pusher are eligible; the PR author cannot self-approve.
- **New commit means new review:** after every new commit, obtain fresh non-author human review and approval, including when the reviewer pushed it. An earlier approval does not cover the new revision.
- **Checks and feedback complete:** checks required for this PR pass, evidence is recorded, dependencies/merge order are resolved, and no blocking review feedback or unresolved conversation remains.
- **Human author merges:** only the human PR author may squash-merge after all requirements are met and the branch is mergeable. AI review, bot approval and checklist ticks do not count as the required approval.

See `CONTRIBUTING.md` for the full policy.
