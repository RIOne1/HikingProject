"""Regression cases for checks that will gate future contributions."""

import copy
import tempfile
import unittest
from pathlib import Path

from check_docs import anchors, check_document, check_mvp
from check_pr import primary_issue, valid_subject, validate


class ContributionTests(unittest.TestCase):
    def setUp(self):
        self.event = {
            "repository": {"full_name": "RIOne1/HikingProject"},
            "pull_request": {
                "number": 4, "title": "chore: prepare repository workflow",
                "created_at": "2026-11-12T09:00:00Z", "user": {"type": "User"},
                "head": {"ref": "chore/3-repository-development-setup"}, "base": {"ref": "main"},
                "body": "- Primary Issue (required): #3\n- Issue relationship: Closes #3\n",
            },
        }
        self.issue = {"number": 3, "state": "open", "created_at": "2026-11-12T08:00:00Z",
                      "html_url": "https://github.com/RIOne1/HikingProject/issues/3"}

    def test_valid_issue_and_branch(self):
        self.assertEqual(validate(self.event, self.issue), [])

    def test_wrong_branch_number_and_tool_namespaces(self):
        for branch in ["chore/4-setup", "chore/03-setup", "codex/3-setup", "feature/3-Uppercase", "docs/3-two--hyphens"]:
            with self.subTest(branch=branch):
                self.event["pull_request"]["head"]["ref"] = branch
                self.assertTrue(validate(self.event, self.issue))

    def test_issue_cannot_be_a_pr_closed_or_from_another_repository(self):
        for change in [{"pull_request": {}}, {"state": "closed"}, {"html_url": "https://github.com/other/repo/issues/3"}]:
            with self.subTest(change=change):
                self.assertTrue(validate(self.event, self.issue | change))

    def test_issue_must_predate_pr(self):
        self.assertTrue(validate(self.event, self.issue | {"created_at": "2026-11-13T00:00:00Z"}))

    def test_bot_and_wrong_target_do_not_pass(self):
        for change in [{"user": {"type": "Bot"}}, {"base": {"ref": "develop"}}]:
            event = copy.deepcopy(self.event)
            event["pull_request"].update(change)
            self.assertTrue(validate(event, self.issue))

    def test_placeholders_comments_and_examples_do_not_count(self):
        for body in ["- Primary Issue (required): N/A", "<!-- - Primary Issue (required): #3 -->",
                     "```text\n- Primary Issue (required): #3\n```",
                     "- Primary Issue (required): #3\n- Primary Issue (required): #3"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                primary_issue(body, "RIOne1/HikingProject")

    def test_relationship_must_be_visible_and_match(self):
        for relationship in ["Closes #4", "<!-- Closes #3 -->", "Closes other/repo#3"]:
            self.event["pull_request"]["body"] = f"- Primary Issue (required): #3\n- Issue relationship: {relationship}\n"
            self.assertTrue(validate(self.event, self.issue))

    def test_markdown_url_and_partial_work(self):
        self.event["pull_request"]["body"] = (
            "- Primary Issue (required): [#3 — setup](https://github.com/RIOne1/HikingProject/issues/3).\n"
            "- Issue relationship: Refs #3 — device validation remains\n"
        )
        self.assertEqual(validate(self.event, self.issue), [])

    def test_legacy_exception_cannot_be_reused(self):
        self.event["pull_request"]["head"]["ref"] = "docs/mvp-and-team-guidelines"
        self.assertTrue(validate(self.event, self.issue))
        self.event["pull_request"].update(number=1, body="- Primary Issue (required): #2\n- Issue relationship: Closes #2\n")
        self.issue.update(number=2, html_url="https://github.com/RIOne1/HikingProject/issues/2")
        self.assertEqual(validate(self.event, self.issue), [])

    def test_conventional_subjects(self):
        for subject in ["feat(gpx)!: reject unsupported formats", "ci: check repository documents"]:
            self.assertTrue(valid_subject(subject))
        for subject in ["Update readme", "docs: update", "fix: WIP", "docs: update links.", "ci: check\nmalicious line"]:
            self.assertFalse(valid_subject(subject))


class DocumentationTests(unittest.TestCase):
    def test_missing_link_and_anchor_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc = root / "README.md"
            doc.write_text("# Hello\n\n[Missing](absent.md)\n[Wrong anchor](#absent)\n", encoding="utf-8")
            self.assertEqual(len(check_document(doc, root)), 2)

    def test_unicode_and_encoded_links_ignore_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "中文 notes.md").write_text("# 验证 与证据\n", encoding="utf-8")
            doc = root / "README.md"
            doc.write_text("# Intro\n[Notes](%E4%B8%AD%E6%96%87%20notes.md#验证-与证据)\n"
                           "[Web](https://example.com)\n```md\n[Example](missing.md)\n```\n", encoding="utf-8")
            self.assertEqual(check_document(doc, root), [])

    def test_duplicate_heading_anchors(self):
        self.assertEqual(anchors("# Hello, world!\n## Hello, world!\n"), {"hello-world", "hello-world-1"})

    def test_bilingual_ids_and_acceptance_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/MVP.md").write_text("### MVP-01 — Test\n**Acceptance:** evidence\n", encoding="utf-8")
            mirror = root / "docs/MVP.zh-CN.md"
            mirror.write_text("### MVP-01 — 测试\n**验收：**证据\n", encoding="utf-8")
            self.assertEqual(check_mvp(root), [])
            mirror.write_text("### MVP-02 — 测试\n", encoding="utf-8")
            self.assertEqual(len(check_mvp(root)), 2)


if __name__ == "__main__":
    unittest.main()
