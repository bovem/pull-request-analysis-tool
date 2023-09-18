import json
import os

def load_config(config_file_path):
    if os.path.isfile(config_file_path):
        try:
            config_file = open(config_file_path)
            config = json.load(config_file)
        except Exception as e:
            raise Exception("Invalid configuration file: {}\nError:\n{}".format(config_file_path, e))
    else:
        raise Exception("Configuration file not found at location: {}".format(config_file_path))
    return config