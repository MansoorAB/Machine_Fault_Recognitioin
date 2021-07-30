"""
    This module copies the data from source location to training raw folder.
"""

import yaml
import argparse
import os
import glob
import shutil
from application_logging import logger


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_data(config_path):
    config = read_params(config_path)
    source_data = config['data_source']['s3_source']
    raw_data = config['load_data']['raw_data']

    if os.path.isdir(raw_data):
        shutil.rmtree(raw_data)
        log_writer.log(file_object, "Deleted existing directory: {}".format(raw_data))

    os.makedirs(raw_data)
    log_writer.log(file_object, "Created new directory: {}".format(raw_data))

    csv_files = glob.glob(os.path.join(source_data, "*.csv"))
    for file in csv_files:
        shutil.copy(file, raw_data)
        log_writer.log(file_object, "copying file {} to {}".format(file, raw_data))


if __name__ == "__main__":

    if os.path.isdir('Training_Logs'):
        shutil.rmtree('Training_Logs')
    os.makedirs('Training_Logs')

    log_writer = logger.App_Logger()
    file_object = open("Training_Logs/loadDataLog.txt", "a")
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    log_writer.log(file_object, "Load data started with params file: {}".format(parsed_args.config))
    load_data(config_path=parsed_args.config)
    file_object.close()
    # eof223454545