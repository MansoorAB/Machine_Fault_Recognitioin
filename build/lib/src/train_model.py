"""
    This module gets the preprocessed data from InputFile.csv and
    1. removes columns - Wafer
    2. checks for null values and if present, imputes null values using KNNImputer
    3. removes the columns with zero std. dev i.e. where all values are same or all different
    4. Uses Kmeans algorithm to cluster data into optimum clusters
    5. For each cluster
        a. gets the best XGBoost model
        b. gets the best RandomForest model
        c. compares the roc_auc_score/accuracy scores for XGBoost and RandomForest models
        d. saves the model that gives the highest score to model directory
    6. Captures metrics related to best parameters and scores for each cluster
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


