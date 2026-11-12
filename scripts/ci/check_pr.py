"""Validate contribution metadata. No writes, approvals or shell interpolation."""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

from check_docs import prose

BRANCH = re.compile(r"(?:feature|fix|docs|refactor|test|chore|build|ci|perf|revert)/([1-9][0-9]*)-[a-z0-9]+(?:-[a-z0-9]+)*")
SUBJECT = re.compile(r"(?:feat|fix|docs|refactor|test|chore|build|ci|perf|revert)(?:\([a-z0-9-]+\))?!?: ([A-Za-z].*)")


def valid_subject(subject):
    match = SUBJECT.fullmatch(subject)
    return bool(match and not subject.endswith(".") and match[1].lower() not in {
        "update", "changes", "fix stuff", "wip", "ai generated"
    })


def primary_issue(body, repository):
    fields = re.findall(r"^- Primary Issue \(required\):[ \t]*([^\n]*)$", prose(body), re.M)
    if len(fields) != 1:
        raise ValueError("Use exactly one visible '- Primary Issue (required): #N' field.")
    value = fields[0].strip().removesuffix(".")
    url = rf"https://github\.com/{re.escape(repository)}/issues/([1-9][0-9]*)"
    for pattern in [r"#([1-9][0-9]*)", url, rf"\[[^]]+\]\({url}\)"]:
        match = re.fullmatch(pattern, value)
        if match:
            return int(match[1])
    raise ValueError("Primary Issue must be #N or a link to an Issue in this repository.")


def validate(event, issue):
    pr = event["pull_request"]
    repository = event["repository"]["full_name"]
    errors = []
    if not valid_subject(pr["title"]):
        errors.append("PR title must follow the Conventional Commits format.")
    if pr["base"]["ref"] != "main":
        errors.append("PR must target main.")
    if pr["user"]["type"] != "User":
        errors.append("Open the mergeable PR under the responsible human account; bot PRs are proposals only.")
    number = primary_issue(pr.get("body") or "", repository)
    branch = pr["head"]["ref"]
    # The recorded transition applies only to the original PR #1, not new work.
    legacy = repository == "RIOne1/HikingProject" and pr["number"] == 1 and branch == "docs/mvp-and-team-guidelines" and number == 2
    match = BRANCH.fullmatch(branch)
    if not legacy and (not match or int(match[1]) != number):
        errors.append("Branch must use an allowed type and the same primary Issue number.")
    # Count every field, including empty/invalid ones. Whitespace must not consume
    # the next line and hide a second, conflicting Issue relationship.
    relationships = re.findall(r"^- Issue relationship:[ \t]*([^\n]*)$", prose(pr.get("body") or ""), re.M)
    relationship = re.fullmatch(r"(Closes|Refs) #([1-9][0-9]*)(?:[ \t]+.*)?", relationships[0].strip()) if len(relationships) == 1 else None
    if not relationship or int(relationship[2]) != number:
        errors.append("Use one visible '- Issue relationship: Closes #N' or 'Refs #N' matching the primary Issue.")
    if issue.get("number") != number or "pull_request" in issue:
        errors.append("The primary number must identify an Issue, not a pull request.")
    if issue.get("html_url") != f"https://github.com/{repository}/issues/{number}":
        errors.append("The Issue must belong to this repository.")
    if issue.get("state") != "open":
        errors.append("The tracking Issue must be open while work is reviewed.")
    if not legacy and datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00")) > datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00")):
        errors.append("The tracking Issue must exist before the PR is opened.")
    return errors


def fetch_issue(repository, number):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid repository name.")
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    request = Request(f"https://api.github.com/repos/{repository}/issues/{number}", headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def commit_errors(pr):
    base, head = pr["base"]["sha"], pr["head"]["sha"]
    if not all(re.fullmatch(r"[0-9a-f]{40}", sha) for sha in (base, head)):
        raise ValueError("Invalid commit SHA.")
    subjects = subprocess.check_output(["git", "log", "--format=%s", f"{base}..{head}"], text=True).splitlines()
    return [f"Non-conforming commit subject: {json.dumps(subject)}" for subject in subjects if not valid_subject(subject)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_PATH"), required=not os.environ.get("GITHUB_EVENT_PATH"))
    parser.add_argument("--issue-json", help="Use a saved GitHub Issue response for a local check, without API access.")
    args = parser.parse_args()
    try:
        event = json.loads(Path(args.event).read_text())
        number = primary_issue(event["pull_request"].get("body") or "", event["repository"]["full_name"])
        issue = json.loads(Path(args.issue_json).read_text()) if args.issue_json else fetch_issue(event["repository"]["full_name"], number)
        errors = validate(event, issue) + commit_errors(event["pull_request"])
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"Contribution check could not complete: {error}", file=sys.stderr)
        return 1
    print(f"Passed: PR title, human-account type, branch, open Issue #{number}, relationship and commit subjects.")
    print("Human review must still verify Issue-before-development order, scope, authorship and fresh approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
