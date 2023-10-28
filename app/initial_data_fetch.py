import os
from sqlalchemy import create_engine
from multiprocessing.pool import ThreadPool

from utils import load_config
from fetcher import repository_pr_data_fetch 
from cleaner import clean_pr_data 
from metrics import calculate_pr_metrics 
from db_loader import load_to_db, clean_files_older_than_one_day

def fetch_initial_data(repo_details):
    config = load_config(os.environ.get("PAT_CONFIG_FILE"))
    pr_data_file = repository_pr_data_fetch(config, repo_details)
    pr_data_cleaned_file = clean_pr_data(config, pr_data_file)

    pr_metrics_df = calculate_pr_metrics(config, pr_data_cleaned_file)

    postgredb_user = config.get("DB_USERNAME")
    postgredb_password = config.get("DB_PASSWD")
    postgresdb_name = config.get("DB_NAME")
    postgresdb_network = config.get("DB_NETWORK")
    engine_url = "postgresql://{}:{}@{}:5432/{}".format(postgredb_user,
                                                    postgredb_password,
                                                    postgresdb_network,
                                                    postgresdb_name)
    engine = create_engine(engine_url)
    
    table_name = "{}_pr_data".format(repo_details.get("REPO_NAME"))
    load_to_db(pr_metrics_df, engine, table_name)

    clean_files_older_than_one_day(config["RAW_DATA_PATH"])
    clean_files_older_than_one_day(config["CLEANED_DATA_PATH"])
    clean_files_older_than_one_day(config["METRICS_DATA_PATH"])

if __name__ == "__main__":
    pool = ThreadPool()
    config = load_config(os.environ.get("PAT_CONFIG_FILE"))
    repo_details = [x for x in config["REPO_DETAILS"]]
    results = pool.map(fetch_initial_data, repo_details)
