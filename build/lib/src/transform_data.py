"""
    This module checks the validated good files for missing values and
    replaces them with null. Also removes the text 'wafer' from first column and keeps
    only the wafer no. instead.
"""

import argparse
from load_data import read_params
from application_logging import logger
from training_Transformation import train_transformation


def transform_data(log_file, config_path):
    config = read_params(config_path)

    # Invoke the validation module
    train_transObj = train_transformation(config, log_file)
    train_transObj.train_transformation()


if __name__ == "__main__":
    log_writer = logger.App_Logger()
    file_object = open("Training_Logs/Transform_Data_Log.txt", "w")
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    log_writer.log(file_object, "Data Transformation started with params file: {}".format(parsed_args.config))
    transform_data(file_object, config_path=parsed_args.config)
    file_object.close()


