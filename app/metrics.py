import pandas as pd
from utils import write_to_file

def merge_status(merge_time):
    if merge_time==(-99):
        return "Unmerged"
    else:
        return "Merged"

def capitalize(input_string):
    return input_string.capitalize()

def calculate_pr_metrics(config, cleaned_pr_data):
    df = pd.read_json(cleaned_pr_data)
    df["pr_creation_time"] = pd.to_datetime(df["pr_creation_time"])
    df["pr_updation_time"] = pd.to_datetime(df["pr_updation_time"])
    df["pr_closing_time"] = pd.to_datetime(df["pr_closing_time"])
    df["pr_merging_time"] = pd.to_datetime(df["pr_merging_time"])
    df["pr_merge"] = df["pr_merging_time"].fillna(-99).apply(merge_status)
    df["pr_state"] = df["pr_state"].apply(capitalize)

    df["time_delta_updation_creation"] = (df["pr_updation_time"] - df["pr_creation_time"]).dt.total_seconds()
    df["time_delta_closing_creation"] = (df["pr_closing_time"] - df["pr_creation_time"]).dt.total_seconds()
    df["time_delta_merging_creation"] = (df["pr_merging_time"] - df["pr_creation_time"]).dt.total_seconds()

    return df.set_index("pr_id")

def update_metrics(engine, existing_data_table, new_metrics_df):
   existing_data_df = pd.read_sql_table(existing_data_table, engine)
   existing_data_df.set_index("pr_id", inplace=True)
   existing_data_df.update(new_metrics_df.set_index("pr_url"))
   return existing_data_df
