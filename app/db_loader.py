import pandas as pd
from sqlalchemy import inspect

def load_to_db(df, engine, table_name):
    df.to_sql(table_name, engine, if_exists="replace")   

    print("Data written to PostgreSQL table: {}".format(table_name))
    return True

