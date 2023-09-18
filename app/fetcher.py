import os
import requests
import math
import time
import json
from utils import load_config

config = load_config(os.environ.get("PAT_CONFIG_FILE"))

def request_github_api(request_url, config):
    bearer_token = "Bearer {}".format(config["GITHUB_API_TOKEN"])

    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": bearer_token,
    "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(request_url, headers=headers)
    response_data = response.json()
    return response_data

def get_pull_request_pages(config):
    pr_page_link = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100".format(config["REPO_OWNER"], config["REPO_NAME"])

    first_pr_page = pr_page_link + "&page=1"
    response = request_github_api(first_pr_page, config)
    num_pages = math.ceil(response[0]["number"]/100)

    pr_pages = []
    for page_num in range(1, num_pages+1):
        pr_pages.append(pr_page_link+"&page={}".format(page_num))
    return pr_pages

def repository_data_fetch(config):
    pr_pages = get_pull_request_pages(config)

    pr_data = []
    for pr_page in pr_pages[:3]:
        print("Requesting URL: {}".format(pr_page))
        pr_data += request_github_api(pr_page, config)
        time.sleep(int(config["REQUEST_TIME_INTERVAL"]))
    
    if not os.path.exists(config["RAW_DATA_PATH"]):
        os.makedirs(config["RAW_DATA_PATH"])
    
    pr_data_file = "pr_data_{}.json".format(time.strftime("%Y%m%d_%H%M%S"))

    with open(os.path.join(config["RAW_DATA_PATH"], pr_data_file), "w") as f:
        json.dump(pr_data, f, indent=4)
    
    print("Number of PRs: {}".format(len(pr_data)))