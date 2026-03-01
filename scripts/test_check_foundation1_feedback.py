import unittest
from unittest.mock import patch

from check_foundation1_feedback import (
    find_missing_repositories,
    is_foundation1_feedback_markdown,
)


class Foundation1FeedbackFileMatchTests(unittest.TestCase):
    def test_match_foundation_1_feedback_variants(self) -> None:
        self.assertTrue(is_foundation1_feedback_markdown("Foundation_1_feedback.md"))
        self.assertTrue(is_foundation1_feedback_markdown("docs/foundation1-feedback.MD"))

    def test_non_matching_names(self) -> None:
        self.assertFalse(is_foundation1_feedback_markdown("foundation_2_feedback.md"))
        self.assertFalse(is_foundation1_feedback_markdown("foundation_1_notes.md"))
        self.assertFalse(is_foundation1_feedback_markdown("foundation_1_feedback.txt"))


class MissingRepoDetectionTests(unittest.TestCase):
    @patch("check_foundation1_feedback.repo_has_foundation1_feedback")
    @patch("check_foundation1_feedback.list_org_repositories")
    def test_returns_only_missing_repositories(
        self, mock_list_org_repositories, mock_repo_has_feedback
    ) -> None:
        mock_list_org_repositories.return_value = [
            {"name": "repo-b", "default_branch": "main"},
            {"name": "repo-a", "default_branch": "main"},
        ]
        mock_repo_has_feedback.side_effect = [True, False]

        missing = find_missing_repositories("WTAMU-CIDM6330", token=None)

        self.assertEqual(missing, ["repo-a"])

    @patch("check_foundation1_feedback.repo_has_foundation1_feedback")
    @patch("check_foundation1_feedback.list_org_repositories")
    def test_returns_missing_repositories_sorted(
        self, mock_list_org_repositories, mock_repo_has_feedback
    ) -> None:
        mock_list_org_repositories.return_value = [
            {"name": "z-repo", "default_branch": "main"},
            {"name": "a-repo", "default_branch": "main"},
        ]
        mock_repo_has_feedback.side_effect = [False, False]

        missing = find_missing_repositories("WTAMU-CIDM6330", token=None)

        self.assertEqual(missing, ["a-repo", "z-repo"])


if __name__ == "__main__":
    unittest.main()
