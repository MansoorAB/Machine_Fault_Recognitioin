"""
    This module copies the data from source location to training raw folder.
"""

import yaml
import argparse
import os
import shutil
from application_logging import logger
from s3_operations import s3_methods


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_data(config_path):
    config = read_params(config_path)
    s3b = config['s3_info']['data_bucket']
    s3bf = config['s3_info']['train_folder']
    raw_data = config['load_data']['raw_data']

    s3m_object = s3_methods.S3Methods(file_object, log_writer)
    s3m_object.get_s3_folder_data_to_local(s3b, s3bf, raw_data, True)


if __name__ == "__main__":

    if os.path.isdir('Training_Logs'):
        shutil.rmtree('Training_Logs')
    os.makedirs('Training_Logs')

    log_writer = logger.App_Logger()
    file_object = open("Training_Logs/Load_Data_Log.txt", "w")
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    # set AWS S3 environment variables (for windows)
    # @ "C:\Users\<UserName>\.aws\credentials"
    # & "C:\Users\<UserName>\.aws\config"

    log_writer.log(file_object, "Load data started with params file: {}".format(parsed_args.config))
    load_data(config_path=parsed_args.config)
    file_object.close()