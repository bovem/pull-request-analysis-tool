import json
import time
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

def write_to_file(data, write_file_path, filename, file_extension="json"):
    if not os.path.exists(write_file_path):
        os.makedirs(write_file_path)

    write_file = "{}_{}.{}".format(filename, time.strftime("%Y%m%d_%H%M%S"), file_extension)
    write_file_full_path = os.path.join(write_file_path, write_file)

    if file_extension=="json":
        with open(write_file_full_path, "w") as f:
            json.dump(data, f, indent=4)

    print("Data written to file: {}".format(write_file_full_path))
    return write_file_full_path

def read_file(read_file_path, file_extension="json"):
    if os.path.isfile(read_file_path):
        try:
            read_file = open(read_file_path)
            if file_extension=="json":
                read_file = json.load(read_file)
        except Exception as e:
            raise Exception("Invalid file: {}\nError:\n{}".format(read_file_path, e))
    else:
        raise Exception("File not found at location: {}".format(read_file_path))
    return read_file