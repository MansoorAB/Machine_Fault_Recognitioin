import os


dirs = [
    "src",
    "Training_Batch_Files",
    "Training_Database",
    "Prediction_Batch_Files",
    "Prediction_Database",
    "Prediction_Output_File",
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass


files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src", "__init__.py")
]

for file_ in files:
    with open(file_, "a") as f:
        pass