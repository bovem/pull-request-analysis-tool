import unittest
from unittest.mock import patch, mock_open
from app.utils import load_config, read_file, write_to_file
from app.cleaner import clean_pr_data
import os

class TestCleanerFunctions(unittest.TestCase):
    @patch('app.utils.read_file')
    @patch('app.utils.write_to_file')
    def test_clean_pr_data(self, mock_read_file, mock_write_to_file):
        pr_data_file = "./mock_data/pr_data.json"
        pr_data = [
            {
                "html_url": "https://github.com/repo1/pull/1",
                "id": 1,
                "number": 1,
                "state": "open",
                "title": "PR Title",
                "user": {
                    "login": "user1",
                    "type": "user",
                },
                "created_at": "2022-01-01T00:00:00Z",
                "updated_at": "2022-01-02T00:00:00Z",
                "closed_at": "2022-01-03T00:00:00Z",
                "merged_at": "2022-01-04T00:00:00Z",
                "merge_commit_sha": "abcd1234",
                "comments_url": "https://github.com/repo1/pull/1/comments",
                "head": {
                    "label": "branch1",
                },
                "base": {
                    "label": "main",
                },
                "author_association": "COLLABORATOR",
            },
        ]

        mock_read_file.return_value = pr_data

        cleaned_pr_data_file_path = clean_pr_data(config, pr_data_file)

        self.assertIn("cleaned_pr_data", cleaned_pr_data_file_path)
        expected_cleaned_data = [
            {
                "pr_url": "https://github.com/repo1/pull/1",
                "pr_id": 1,
                "pr_number": 1,
                "pr_state": "open",
                "pr_title": "PR Title",
                "pr_creator": "user1",
                "pr_creator_type": "user",
                "pr_creation_time": "2022-01-01T00:00:00Z",
                "pr_updation_time": "2022-01-02T00:00:00Z",
                "pr_closing_time": "2022-01-03T00:00:00Z",
                "pr_merging_time": "2022-01-04T00:00:00Z",
                "pr_merge_commit": "abcd1234",
                "pr_comments_url": "https://github.com/repo1/pull/1/comments",
                "pr_merge_branch_from": "branch1",
                "pr_merge_branch_to": "main",
                "pr_author_association": "COLLABORATOR",
            },
        ]
        mock_write_to_file.assert_called_with(
            expected_cleaned_data,
            "./mock_data",
            "cleaned_pr_data",
            "json",
        )

if __name__ == "__main__":
    unittest.main()
