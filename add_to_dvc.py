# NOTE: For windows user-
# This file must be created in the root of the project
# where Training and Prediction batch file as are present

import os
import argparse
from glob import glob


def add_data(folders):
    # data_dirs = ["Training_Batch_Files", "Prediction_Batch_files"]

    data_dirs = folders.split(',')
    for data_dir in data_dirs:
        files = glob(data_dir.strip() + r"/*.csv")
        for filePath in files:
            # print(f"dvc add {filePath}")
            os.system(f"dvc add {filePath}")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--folders")
    parsed_args = args.parse_args()
    add_data(parsed_args.folders)
    print("\n #### all files added to dvc ####")

