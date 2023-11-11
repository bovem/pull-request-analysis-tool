import json
import glob
import pandas as pd
import os
from app.utils import write_to_file, read_file

def clean_pr_data(config, pr_data_file):
    pr_data = read_file(pr_data_file)

    cleaned_pr_data = []
    for pr in pr_data:
        if type(pr)==dict:
            cleaned_pr_data.append({
                "pr_url": pr.get("html_url", None),
                "pr_id": pr.get("id", None),
                "pr_number": pr.get("number", None),
                "pr_state": pr.get("state", None),
                "pr_title": pr.get("title", None),
                "pr_creator": pr.get("user", {}).get("login", None),
                "pr_creator_type": pr.get('user', {}).get('type', None),
                "pr_creation_time": pr.get("created_at", None),
                "pr_updation_time": pr.get("updated_at", None),
                "pr_closing_time": pr.get("closed_at", None),
                "pr_merging_time": pr.get("merged_at", None),
                "pr_merge_commit": pr.get("merge_commit_sha", None),
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
