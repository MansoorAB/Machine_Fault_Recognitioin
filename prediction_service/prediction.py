import yaml
import os
import shutil
import json
from flask import Response
from datetime import datetime

from application_logging import logger
from prediction_Validation_Insertion import pred_validation
from predictFromModel import model_prediction
from s3_operations import s3_methods


class ModelPrediction:

    def __init__(self, log_file):
        self.log_file = log_file
        self.log_writer = logger.App_Logger()
        self.params_path = 'params.yaml'
        self.config = self.read_params()

    def read_params(self):
        with open(self.params_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config

    def get_s3_data(self, local):
        # This methods gets data from s3 bucket to local folder

        s3b = self.config['s3_info']['data_bucket']
        s3bp = self.config['s3_info']['pred_folder']

        s3m_object = s3_methods.S3Methods(self.log_file, self.log_writer)
        s3m_object.get_s3_folder_data_to_local(s3b, s3bp, local, True)

    def form_response(self, dict_request):

        path = dict_request['folderPath']
        self.log_writer.log(self.log_file, 'Processing prediction initiated via web form.'
                                           'Prediction folder given: %s' % path)

        # check the path provided is not blank, not an existing path
        if not path:
            message = 'Path is blank! Please provide a valid path and try again or go for Default File Predict.'
            self.log_writer.log(self.log_file, message)
            return Response(message)
        elif os.path.isdir(path):
            message = 'Path provided already exists! Please provide a different path or go for Default File Predict.'
            self.log_writer.log(self.log_file, message)
            return Response(message)
        else:
            # create a directory by name path (provided by user) and get s3 prediction data over there
            # print(datetime.now(), 'starting to fetch s3 data')
            self.get_s3_data(path)
            # print(datetime.now(), 'end of fetch s3 data')

            # Validate the Prediction Files given
            pred_val = pred_validation(path, self.config, self.log_file)
            pred_val.prediction_validation()

            # print(datetime.now(), 'End of validation')

            shutil.rmtree(path)  # removing prediction folder as consolidated file is prepared
            self.log_writer.log(self.log_file, 'Removed the local folder %s that held prediction input files' % path)

            # Make prediction on the consolidated prediction file
            make_pred = model_prediction(path, self.config, self.log_file)
            op_path, json_predictions = make_pred.predictionFromModel()

            print(datetime.now(), 'End of prediction')

            return Response("Prediction file is accessible at url: %s and some of the predictions are %s"
                            % (op_path, json.loads(json_predictions)))

    def api_response(self, dict_request):
        try:
            path = dict_request['folderPath']
            self.log_writer.log(self.log_file, 'Processing prediction initiated via api call. '
                                               'Prediction folder given: %s' % path)

            # check the path provided is not blank, not an existing path
            if not path:
                message = 'Path is blank! Please provide a valid path and try again or go for Default File Predict.'
                self.log_writer.log(self.log_file, message)
                return Response(message)
            elif os.path.isdir(path):
                message = 'Path provided already exists! Please provide a different path or go for Default File Predict.'
                self.log_writer.log(self.log_file, message)
                return Response(message)
            else:
                # create a directory by name path (provided by user) and get s3 prediction data over there
                self.get_s3_data(path)

                # Validate the Prediction Files given
                pred_val = pred_validation(path, self.config, self.log_file)
                pred_val.prediction_validation()

                shutil.rmtree(path)  # removing prediction folder as consolidated file is prepared
                self.log_writer.log(self.file_object, 'Removed the local folder %s that held prediction input files' % path)

                # Make prediction on the consolidated prediction file
                make_pred = model_prediction(path, self.config, self.log_file)
                op_path, json_predictions = make_pred.predictionFromModel()

                return {'Output File': op_path, 'Sample Predictions': json.loads(json_predictions)}

        except Exception as e:
            return {'response': str(e)}


