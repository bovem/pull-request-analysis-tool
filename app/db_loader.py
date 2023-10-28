import os
import time
import pandas as pd
from sqlalchemy import inspect

def load_to_db(df, engine, table_name):
    df.to_sql(table_name, engine, if_exists="replace")   

    print("Data written to PostgreSQL table: {}".format(table_name))
    return True

def clean_files_older_than_one_day(dir_location):
    num_days = 1

    absolute_dir_location = os.path.join(os.getcwd(), dir_location)
    list_of_files = os.listdir(absolute_dir_location) 
    current_time = time.time() 
    day = 86400

    for i in list_of_files: 
        file_location = os.path.join(absolute_dir_location, i) 
        file_time = os.stat(file_location).st_mtime 
        if(file_time < current_time - day*num_days): 
            print(f" Delete : {i}") 
            os.remove(file_location)
