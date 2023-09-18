import json
import os
from utils import load_config, write_to_file, read_file

config = load_config(os.environ.get("PAT_CONFIG_FILE"))

def clean_pr_data(config, pr_data_file):
    pr_data = read_file(pr_data_file)

    cleaned_pr_data = []
    for pr in pr_data:
        pr_labels = [x["name"] for x in pr["labels"]]
        cleaned_pr_data.append({
            "PR URL": pr["html_url"],
            "PR ID": pr["id"],
            "PR Number": pr["number"],
            "PR State": pr["state"],
            "PR Title": pr["title"],
            "PR Creator": pr["user"]["login"],
            "PR Forked Repsitory Name": pr["head"]["repo"]["full_name"],
            "PR Forked Repsitory URL": pr["head"]["repo"]["html_url"],
            "PR Creator Type": pr["user"]["type"],
            "PR Creation Time": pr["created_at"],
            "PR Updation Time": pr["updated_at"],
            "PR Closing Time": pr["closed_at"],
            "PR Merging Time": pr["merged_at"],
            "PR Merging Commit": pr["merge_commit_sha"],
            "PR Labels": pr_labels,
            "PR Comments URL": pr["comments_url"],
            "PR Merge Branch From": pr["head"]["label"],
            "PR Merge Brach To": pr["base"]["label"],
            "PR Author Association": pr["author_association"]
        }) 
    
    write_to_file(cleaned_pr_data, 
                  config["CLEANED_DATA_PATH"], 
                  "cleaned_pr_data", 
                  "json")

def clean_pr_comments_data(config, pr_comments_file):
    pr_comments_data = read_file(pr_comments_file)

    cleaned_pr_comments_data = []
    for pr_comment in pr_comments_data:
        cleaned_pr_comments_data.append({
            "PR Comment URL": pr_comment["html_url"],
            "PR URL": pr_comment["html_url"].split("#issuecomment")[0],
            "PR Comment User": pr_comment["user"]["login"],
            "PR Comment User Type": pr_comment["user"]["type"],
            "PR Comment Created At": pr_comment["created_at"],
            "PR Comment Updated At": pr_comment["updated_at"],
            "PR Comment Author Association": pr_comment["author_association"],
            "PR Comment Body": pr_comment["body"]
        }) 
    
    write_to_file(cleaned_pr_comments_data, 
                  config["CLEANED_DATA_PATH"], 
                  "cleaned_pr_comments_data", 
                  "json")

clean_pr_data(config, "./raw_data/pr_data_20230918_132543.json")
# clean_pr_comments_data(config, "./raw_data/comments_data_20230918_151849.json")