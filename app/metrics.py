import pandas as pd
from utils import write_to_file

def merge_status(merge_time):
    if merge_time==(-99):
        return False
    else:
        return True

def extract_operator_name(pr_title):
    if len(pr_title.split(" "))!=3:
        return None
    return pr_title.split(" ")[-2]

def extract_operator_version(pr_title):
    if len(pr_title.split(" "))!=3:
        return None
    return pr_title.split(" ")[-1].replace("(", "").replace(")", "")

def calculate_pr_metrics(config, cleaned_pr_data):
    df = pd.read_json(cleaned_pr_data)
    df["pr_creation_time"] = pd.to_datetime(df["pr_creation_time"])
    df["pr_updation_time"] = pd.to_datetime(df["pr_updation_time"])
    df["pr_closing_time"] = pd.to_datetime(df["pr_closing_time"])
    df["pr_merging_time"] = pd.to_datetime(df["pr_merging_time"])
    df["pr_merge"] = df["pr_merging_time"].fillna(-99).apply(merge_status)
    df["operator_name"] = df["pr_title"].apply(extract_operator_name)
    df["operator_version"] = df["pr_title"].apply(extract_operator_version)

    df["time_delta_updation_creation"] = (df["pr_updation_time"] - df["pr_creation_time"]).dt.total_seconds()
    df["time_delta_closing_creation"] = (df["pr_closing_time"] - df["pr_creation_time"]).dt.total_seconds()
    df["time_delta_merging_creation"] = (df["pr_merging_time"] - df["pr_creation_time"]).dt.total_seconds()

    return df

def convert_string_time(string_time):
    num_value = string_time.split(" ")[0]
    if num_value == "a" or num_value == "an":
        num_value = 1
    if "hour" in string_time:
        return int(num_value)*3600
    elif "minute" in string_time:
        return int(num_value)*60
    elif "second" in string_time:
        return int(num_value)
    else:
        print("Invalid string_time")

def extract_pipelinerun_statistics(pr_url, pr_comment):
    pr_comment = pr_comment.split("\n")
    pr_stat = {"pr_url":pr_url,
               "pipelinerun_comment":False,
               "pipelinerun_status":"Passed",
               "pipelinerun_duration":0,
               "failed_taskrun":[]}

    for line in pr_comment:
        if "Pipeline:" in line and pr_stat.get("pipeline_name")==None:
            pr_stat["pipeline_name"] = line.split(' ')[-1].replace("*","")

        if "PipelineRun:" in line and pr_stat.get("pipelinerun")==None:
            pr_stat["pipelinerun"] = line.split(' ')[-1].replace("*","")
            pr_stat["pipelinerun_comment"] = True
        
        if "Start Time" in line and pr_stat.get("pipelinerun_start_time")==None:
            pr_stat["pipelinerun_start_time"] = " ".join(line.split(' ')[-2:]).replace("*", "")

        if ":heavy_check_mark:" in line:
            taskrun_name = line.split("|")[2].strip()
            pr_stat["taskrun"]=taskrun_name
            pr_stat["taskrun_status"]="Passed"
            pr_stat["taskrun_duration"]=convert_string_time(
                    line.split("|")[-2].strip())
            pr_stat["pipelinerun_duration"]+=pr_stat["taskrun_duration"]

        if ":x:" in line:
            taskrun_name = line.split("|")[2].strip()
            pr_stat["taskrun"]=taskrun_name
            pr_stat["failed_taskrun"] = pr["failed_taskrun"].append(taskrun_name)
            pr_stat["taskrun_status"]="Failed"
            pr_stat["taskrun_duration"]=convert_string_time(
                    line.split("|")[-2].strip())
            pr_stat["pipelinerun_duration"]+=pr_stat["taskrun_duration"]
            pr_stat["pipelinerun_status"]="Failed"
    

    pr_stat["failed_taskrun"] = " ".join(pr_stat["failed_taskrun"])
    
    return pr_stat

def calculate_pr_comment_metrics(config, cleaned_pr_comments_data):
    comments_df = pd.read_json(cleaned_pr_comments_data)

    comments_df["hosted_pipeline_executed"] = comments_df["pr_comment_body"].str.contains("operator-hosted-pipeline")
    comments_df["release_pipeline_executed"] = comments_df["pr_comment_body"].str.contains("operator-release-pipeline")

    pipelinerun_stats_data = []

    for index, row in comments_df.iterrows():
        pr_stats = extract_pipelinerun_statistics(
            row["pr_url"],
            row["pr_comment_body"])
        pipelinerun_stats_data.append(pr_stats)
    
    comment_stats_df = pd.DataFrame(pipelinerun_stats_data)

    return comments_df, comment_stats_df
