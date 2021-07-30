"""
    This module validates training raw files and moves them to
    good data or bad data folder inside training raw files validated folder
"""

import argparse
from load_data import read_params
from application_logging import logger
from training_Validation import train_validation


def validate_data(log_file,config_path):
    config = read_params(config_path)

    # Invoke the validation module
    train_valObj = train_validation(config, log_file)
    train_valObj.train_validation()


if __name__ == "__main__":
    log_writer = logger.App_Logger()
    file_object = open("Training_Logs/validateDataLog.txt", "w")
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    log_writer.log(file_object, "Validate data started with params file: {}".format(parsed_args.config))
    validate_data(file_object, config_path=parsed_args.config)
    file_object.close()


