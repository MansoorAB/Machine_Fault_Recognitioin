import yaml
import os
import json
from flask import Response

from application_logging import logger
from prediction_Validation_Insertion import pred_validation
from predictFromModel import model_prediction


class ModelPrediction:

    def __init__(self, log_file):
        self.log_file = log_file
        self.log_writer = logger.App_Logger()
        self.params_path = 'params.yaml'

    def read_params(self):
        with open(self.params_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config

    def form_response(self, dict_request):

        path = dict_request['folderPath']
        self.log_writer.log(self.log_file, 'Processing prediction initiated via web form.'
                                           'Prediction folder given: %s' % path)

        # check if the path exists and throw error if not
        if os.path.exists(path):
            config = self.read_params()

            # Validate the Prediction Files given
            pred_val = pred_validation(path, config, self.log_file)
            pred_val.prediction_validation()

            # Make prediction on the consolidated prediction file
            make_pred = model_prediction(path, config, self.log_file)
            op_path, json_predictions = make_pred.predictionFromModel()

            return Response("Prediction file created at \"%s\" \n and a few of the predictions are %s"
                            % (op_path, json.loads(json_predictions)))
        else:
            message = 'Invalid path: %s. Please check!!!!' % path
            self.log_writer.log(self.log_file, message)
            return Response("Invalid path: \"%s\". Please cross-check!" % path)

    def api_response(self, dict_request):
        try:
            path = dict_request['folderPath']
            self.log_writer.log(self.log_file, 'Processing prediction initiated via api call. '
                                               'Prediction folder given: %s' % path)

            # check if the path exists and throw error if not
            if os.path.exists(path):
                config = self.read_params()

                # Validate the Prediction Files given
                pred_val = pred_validation(path, config, self.log_file)
                pred_val.prediction_validation()

                # Make prediction on the consolidated prediction file
                make_pred = model_prediction(path, config, self.log_file)
                op_path, json_predictions = make_pred.predictionFromModel()

                return {'Output File': op_path, 'Sample Predictions': json.loads(json_predictions)}
            else:
                message = 'Invalid path: %s. Please check!!!!' % path
                self.log_writer.log(self.log_file, message)
                return {'response': message}

        except Exception as e:
            return {'response': str(e)}


