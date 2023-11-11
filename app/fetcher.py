import os
import glob
import requests
import math
import time
import json
from app.utils import write_to_file, read_file

def request_github_api(request_url, config):
    bearer_token = "Bearer {}".format(config["GITHUB_API_TOKEN"])

    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": bearer_token,
    "X-GitHub-Api-Version": "2022-11-28"
    }

    print("Requesting URL: {}".format(request_url))
    response = requests.get(request_url, headers=headers)
    response_data = response.json()
    return response_data

def get_pull_request_pages(config, repo_details):
    pr_page_link = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100"
    pr_page_link = pr_page_link.format(repo_details["REPO_OWNER"], repo_details["REPO_NAME"])

    first_pr_page = pr_page_link + "&page=1"
    response = request_github_api(first_pr_page, config)
    num_pages = math.ceil(response[0]["number"]/100)

    pr_pages = []
    for page_num in range(1, num_pages+1):
        pr_pages.append(pr_page_link+"&page={}".format(page_num))
    return pr_pages

def repository_pr_data_fetch(config, repo_details):
    pr_pages = get_pull_request_pages(config, repo_details)

    pr_data = []
    for pr_page in pr_pages:
        pr_data += request_github_api(pr_page, config)
        time.sleep(int(config["REQUEST_TIME_INTERVAL"]))

    print("Number of PRs: {}".format(len(pr_data)))
    pr_data_file_path = write_to_file(pr_data, config["RAW_DATA_PATH"], "pr_data", "json")
    return pr_data_file_path

def update_pull_request_pages(config, repo_details):
    pr_page_link = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100&sort=updated&direction=desc"
    pr_page_link = pr_page_link.format(repo_details["REPO_OWNER"], repo_details["REPO_NAME"])

    first_pr_page = pr_page_link + "&page=1"
    response = request_github_api(first_pr_page, config)

    print("Number of PRs: {}".format(len(response)))
    pr_data_file_path = write_to_file(response, config["RAW_DATA_PATH"], "updated_pr_data", "json")
    return pr_data_file_path
