import unittest
from unittest.mock import Mock, patch
import os
from app.utils import load_config
from app.fetcher import (
    request_github_api,
    get_pull_request_pages,
    repository_pr_data_fetch,
    update_pull_request_pages,
)

config = load_config(os.environ.get("PAT_CONFIG_FILE"))

class TestFetcherFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_request_github_api(self, mock_get):
        response_data = {"key": "value"}
        mock_get.return_value.json.return_value = response_data

        request_url = "https://api.github.com/"
        result = request_github_api(request_url, config)

        self.assertEqual(result, response_data)

        bearer_token = "Bearer {}".format(config["GITHUB_API_TOKEN"])
        mock_get.assert_called_with(
            request_url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": bearer_token,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def test_get_pull_request_pages(self):
        repo_details = config["REPO_DETAILS"][0]

        pr_pages = get_pull_request_pages(config, repo_details)

        self.assertIsInstance(pr_pages, list)
        self.assertGreater(len(pr_pages), 0)

        repo_url = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100&page=1"
        repo_url = repo_url.format(repo_details["REPO_OWNER"], repo_details["REPO_NAME"])

        self.assertIn(repo_url, pr_pages[0])

    def test_repository_pr_data_fetch(self):
        pass

    def test_update_pull_request_pages(self):
        pass

if __name__ == "__main__":
    unittest.main()
