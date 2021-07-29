import os


dirs = [
    "src",
    "Training_Batch_Files",
    "Training_Raw_Files",
    "Training_Raw_Files_Validated",
    os.path.join("Training_Raw_Files_Validated", "Good_Raw"),
    os.path.join("Training_Raw_Files_Validated", "Bad_Raw"),
    "Training_Database",
    "Training_Logs",
    "Prediction_Batch_Files",
    "Prediction_Raw_Files",
    "Prediction_Raw_Files_Validated",
    os.path.join("Prediction_Raw_Files_Validated", "Good_Raw"),
    os.path.join("Prediction_Raw_Files_Validated", "Bad_Raw"),
    "Prediction_Database",
    "Prediction_Logs",
    "Prediction_Output_File",
    "models"
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass


files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
]

for file_ in files:
    with open(file_, "a") as f:
        pass