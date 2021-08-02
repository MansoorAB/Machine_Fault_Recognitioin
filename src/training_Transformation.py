from datetime import datetime
from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from DataTransform_Training.DataTransformation import dataTransform
from application_logging import logger

class train_transformation:
    def __init__(self,config, log_file):
        self.dataTransform = dataTransform(config, log_file)
        self.file_object = log_file
        self.log_writer = logger.App_Logger()

    def train_transformation(self):
        try:
            self.log_writer.log(self.file_object, "Starting Data Transformation for Validated Good files!!")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replaceMissingWithNull()

            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")

        except Exception as e:
            raise e









