# Copy the data from the source and save it in the raw files folder
# Takes arguments

import yaml
import argparse
import os
import glob
import shutil
from os import listdir


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_data(config_path):
    config = read_params(config_path)
    source_data = config['data_source']['s3_source']
    raw_data = config['load_data']['raw_data']

    csv_files = glob.glob(os.path.join(source_data, "*.csv"))
    for file in csv_files:
        shutil.copy(file, raw_data)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_data(config_path=parsed_args.config)