import json
import glob
import pandas as pd
import os
from utils import write_to_file, read_file

def clean_pr_data(config, pr_data_file):
    pr_data = read_file(pr_data_file)

    cleaned_pr_data = []
    for pr in pr_data:
        #pr_labels = [x["name"] for x in pr["labels"]]
        if type(pr)==dict:
            cleaned_pr_data.append({
                "pr_url": pr.get("html_url", None),
                "pr_id": pr.get("id", None),
                "pr_number": pr.get("number", None),
                "pr_state": pr.get("state", None),
                "pr_title": pr.get("title", None),
                "pr_creator": pr.get("user", {}).get("login", None),
                #"pr_forked_repository": pr.get("head", {}).get("repo", {}).get("full_name", None),
                #"pr_forked_repository_url": pr.get("head", {}).get("repo", {}).get("html_url", None),
                "pr_creator_type": pr.get('user', {}).get('type', None),
                "pr_creation_time": pr.get("created_at", None),
                "pr_updation_time": pr.get("updated_at", None),
                "pr_closing_time": pr.get("closed_at", None),
                "pr_merging_time": pr.get("merged_at", None),
                "pr_merge_commit": pr.get("merge_commit_sha", None),
                #"PR Labels": pr_labels,
                "pr_comments_url": pr.get("comments_url", None),
                "pr_merge_branch_from": pr.get("head", {}).get("label", None),
                "pr_merge_branch_to": pr.get("base", {}).get("label"),
                "pr_author_association": pr.get("author_association", None)
            }) 
    
    cleaned_pr_data_file_path = write_to_file(cleaned_pr_data, 
                                              config["CLEANED_DATA_PATH"], 
                                              "cleaned_pr_data", 
                                              "json")
    return cleaned_pr_data_file_path

def update_cleaned_pr_data(config):
    fetched_data_path = "{}/pr_data*".format(config["RAW_DATA_PATH"])
    list_of_files = glob.glob(fetched_data_path)
    latest_fetched_data_file = read_file(max(list_of_files, key=os.path.getctime))

    df_fetched = pd.DataFrame(latest_fetched_data_file)
    print(df_fetched.info())

    updated_data_path = "{}/updated_pr_data*".format(config["RAW_DATA_PATH"])
    list_of_files = glob.glob(updated_data_path)
    latest_updated_file = read_file(max(list_of_files, key=os.path.getctime))

    df_updated = pd.DataFrame(latest_updated_file)
    print(df_updated.info())

