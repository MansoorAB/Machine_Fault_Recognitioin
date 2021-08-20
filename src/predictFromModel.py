import pandas as pd
import os
from file_operations import file_methods
from data_preprocessing import preprocessing
from data_ingestion import data_loader_prediction
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from s3_operations import s3_methods
from datetime import datetime


class model_prediction:

    def __init__(self, path, config, log_file):
        self.file_object = log_file
        self.config = config
        self.log_writer = logger.App_Logger()
        if path is not None:
            self.pred_data_val = Prediction_Data_validation(path, config, log_file)

    def predictionFromModel(self):

        try:

            # deletes the existing prediction file from last run!
            self.pred_data_val.deletePredictionFile()

            self.log_writer.log(self.file_object, 'Start of Prediction...')

            # Get the consolidated prediction data .csv file
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer,
                                                                  self.config['predict_data']['prediction_file'])
            data = data_getter.get_data()

            # Impute null values in prediction with KNNImputer, if applicable
            preprocessor = preprocessing.Preprocessor(self.config, self.file_object, self.log_writer)
            is_null_present = preprocessor.is_null_present(data)
            if is_null_present:
                data = preprocessor.impute_missing_values(data)

            # Get the redundant columns information from reports and drop them from prediction data
            with open(self.config['reports']['cols2rmv'], 'r') as f:
                cols_to_drop = [col.strip() for col in f]
            f.close()
            data = preprocessor.remove_columns(data, cols_to_drop)

            # Download the trained models from Amazon s3 bucket
            s3m_object = s3_methods.S3Methods(self.file_object, self.log_writer)
            s3m_object.get_s3_bucket_data_to_local(self.config['s3_info']['models_bucket'], self.config['models'])

            # Get the KMeans clustering method saved during training
            file_loader = file_methods.File_Operation(self.config, self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            # Assign clusters to the prediction data based on fetched KMeans model
            clusters = kmeans.predict(data.drop(['Wafer'], axis=1))  # drops the first column for cluster prediction
            data['clusters'] = clusters
            clusters = data['clusters'].unique()

            op_file = self.config['predict_data']['prediction_final_file']
            if os.path.exists(op_file):
                os.remove(op_file)

            # For each cluster, make the prediction based on corresponding model saved during training.
            for i in clusters:
                cluster_data = data[data['clusters'] == i]
                # wafer_names = list(pd.to_numeric(cluster_data['Wafer'], downcast='integer'))
                wafer_names = list(map(int, cluster_data['Wafer']))

                cluster_data = data.drop(labels=['Wafer'], axis=1)
                cluster_data = cluster_data.drop(['clusters'], axis=1)

                # model_name = file_loader.find_correct_model_file(i)
                # model = file_loader.load_model(model_name)
                model = file_loader.get_cluster_model_file(i)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_names, result)), columns=['Wafer', 'Prediction'])
                result.to_csv(op_file, header=True, mode='a+', index=False)
                print(datetime.now(), 'prediction complete for cluster: %d' % i)
            self.log_writer.log(self.file_object, 'End of Prediction')

            # Upload the null values report and output prediction to s3 bucket
            s3m_object.upload_single_local_file_to_s3(self.config['s3_info']['reports_bucket'],
                                                      self.config['reports']['null_values_prediction'])
            s3m_object.upload_single_local_file_to_s3(self.config['s3_info']['reports_bucket'],
                                                      op_file, True)

            op_url = 'https://wafer-reports.s3.us-east-2.amazonaws.com/Predictions.csv'

        except Exception as ex:
            self.log_writer.log(self.file_object, 'Error occurred while running the prediction!! Error:: %s' % ex)
            raise ex

        return op_url, result.head().to_json(orient="records")




