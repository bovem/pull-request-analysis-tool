import json
import os
from utils import write_to_file, read_file

def clean_pr_data(config, pr_data_file):
    pr_data = read_file(pr_data_file)

    cleaned_pr_data = []
    for pr in pr_data:
        pr_labels = [x["name"] for x in pr["labels"]]
        cleaned_pr_data.append({
            "PR URL": pr.get("html_url", None),
            "PR ID": pr.get("id", None),
            "PR Number": pr.get("number", None),
            "PR State": pr.get("state", None),
            "PR Title": pr.get("title", None),
            "PR Creator": pr.get("user", {}).get("login", None),
            "PR Forked Repsitory Name": pr.get("head", {}).get("repo", {}).get("full_name", None),
            "PR Forked Repsitory URL": pr.get("head", {}).get("repo", {}).get("html_url", None),
            "PR Creator Type": pr.get('user', {}).get('type', None),
            "PR Creation Time": pr.get("created_at", None),
            "PR Updation Time": pr.get("updated_at", None),
            "PR Closing Time": pr.get("closed_at", None),
            "PR Merging Time": pr.get("merged_at", None),
            "PR Merging Commit": pr.get("merge_commit_sha", None),
            "PR Labels": pr_labels,
            "PR Comments URL": pr.get("comments_url", None),
            "PR Merge Branch From": pr.get("head", {}).get("label", None),
            "PR Merge Brach To": pr.get("base", {}).get("label"),
            "PR Author Association": pr.get("author_association", None)
        }) 
    
    cleaned_pr_data_file_path = write_to_file(cleaned_pr_data, 
                                              config["CLEANED_DATA_PATH"], 
                                              "cleaned_pr_data", 
                                              "json")
    return cleaned_pr_data_file_path

def clean_pr_comments_data(config, pr_comments_file):
    pr_comments_data = read_file(pr_comments_file)

    cleaned_pr_comments_data = []
    for pr_comment in pr_comments_data:
        cleaned_pr_comments_data.append({
            "PR Comment URL": pr_comment.get("html_url", None),
            "PR URL": pr_comment.get("html_url", None).split("#issuecomment")[0],
            "PR Comment User": pr_comment.get("user", {}).get("login", None),
            "PR Comment User Type": pr_comment.get("user", {}).get("type", None),
            "PR Comment Created At": pr_comment.get("created_at", None),
            "PR Comment Updated At": pr_comment.get("updated_at", None),
            "PR Comment Author Association": pr_comment.get("author_association", None),
            "PR Comment Body": pr_comment.get("body", None)
        }) 
    
    cleaned_pr_comment_data_file_path = write_to_file(cleaned_pr_comments_data, 
                                              config["CLEANED_DATA_PATH"], 
                                              "cleaned_pr_comments_data", 
                                              "json")
    return cleaned_pr_comment_data_file_path