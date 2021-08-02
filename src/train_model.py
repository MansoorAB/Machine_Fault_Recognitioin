"""
    This module ...
"""

import argparse
from load_data import read_params
from application_logging import logger
from trainingModel import trainModel

def train_data(log_file,config_path):
    config = read_params(config_path)

    # Invoke the validation module
    trainModelObj = trainModel(config, log_file)
    trainModelObj.trainingModel()


if __name__ == "__main__":
    log_writer = logger.App_Logger()
    file_object = open("Training_Logs/Train_Model_Log.txt", "w")
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    log_writer.log(file_object, "Model training starts here with params file: {}".format(parsed_args.config))
    train_data(file_object, config_path=parsed_args.config)
    file_object.close()


