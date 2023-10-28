import os
from sqlalchemy import create_engine
import trio

from utils import load_config
from fetcher import repository_pr_data_fetch, repository_comment_data_fetch
from cleaner import clean_pr_data, clean_pr_comments_data
from metrics import calculate_pr_metrics, calculate_pr_comment_metrics 
from db_loader import load_to_db

async def update_data(config, repo_details):
    pr_data_file = await repository_pr_data_fetch(config, repo_details)
    pr_data_cleaned_file = clean_pr_data(config, pr_data_file)

    pr_comments_data_file = await repository_comment_data_fetch(config, pr_data_cleaned_file)
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

async def main():
    async with trio.open_nursery() as nursery:
        config = load_config(os.environ.get("PAT_CONFIG_FILE"))
        for repo_details in config["REPO_DETAILS"]:
            nursery.start_soon(update_data, config, repo_details)

if __name__ == "__main__":
    trio.run(main)
