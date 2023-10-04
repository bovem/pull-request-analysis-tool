import os
from sqlalchemy import create_engine
from multiprocessing.pool import ThreadPool

from utils import load_config
from fetcher import repository_pr_data_fetch, repository_comment_data_fetch
from cleaner import clean_pr_data, clean_pr_comments_data
from metrics import calculate_pr_metrics, calculate_pr_comment_metrics 
from db_loader import load_to_db

def update_data(repo_details):
    config = load_config(os.environ.get("PAT_CONFIG_FILE"))
    pr_data_file = repository_pr_data_fetch(config, repo_details)
    pr_data_cleaned_file = clean_pr_data(config, pr_data_file)

    pr_comments_data_file = repository_comment_data_fetch(config, pr_data_cleaned_file)
    pr_comments_data_cleaned_file = clean_pr_comments_data(config, pr_comments_data_file)
    #pr_comments_data_cleaned_file = clean_pr_comments_data(config, "./raw_data/comments_data_20231001_141257.json")

    pr_metrics_data_file = calculate_pr_metrics(config, pr_data_cleaned_file)
    pr_comment_metrics_data_file, pr_comment_stats_data_file = calculate_pr_comment_metrics(config, pr_comments_data_cleaned_file) 

    postgredb_user = config.get("DB_USERNAME")
    postgredb_password = config.get("DB_PASSWD")
    postgresdb_name = config.get("DB_NAME")
    postgresdb_network = config.get("DB_NETWORK")
    engine_url = "postgresql://{}:{}@{}:5432/{}".format(postgredb_user,
                                                    postgredb_password,
                                                    postgresdb_network,
                                                    postgresdb_name)
    engine = create_engine(engine_url)

    #table_name = "{}/{}".format(repo_details.get("REPO_OWNER"),
    #                            repo_details.get("REPO_NAME"))

    load_to_db(pr_metrics_data_file, engine, "{}_pr_data".format(repo_details.get("REPO_NAME")))
    load_to_db(pr_comment_metrics_data_file, 
               engine,
               "{}_pr_comments_data".format(repo_details.get("REPO_NAME")))
    load_to_db(pr_comment_stats_data_file,
               engine, 
               "{}_pr_comments_stats".format(repo_details.get("REPO_NAME")))

if __name__ == "__main__":
    pool = ThreadPool()
    config = load_config(os.environ.get("PAT_CONFIG_FILE"))
    repo_details = [x for x in config["REPO_DETAILS"]]
    results = pool.map(update_data, repo_details)
