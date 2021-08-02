from datetime import datetime
from os import listdir
import pandas
from application_logging.logger import App_Logger


class dataTransform:

     """
               This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

               Written By: Mansoor Baig
               Version: 1.0
               Revisions: None

               """

     def __init__(self, config, log_file):
          self.goodDataPath = config['validate_data']['good_raw']
          self.logger = App_Logger()
          self.log_file = log_file


     def replaceMissingWithNull(self):
          """
                                           Method Name: replaceMissingWithNull
                                           Description: This method replaces the missing values in columns with "NULL" to
                                                        store in the table. We are using substring in the first column to
                                                        keep only "Integer" data for ease up the loading.
                                                        This column is anyways going to be removed during training.

                                            Written By: Mansoor Baig
                                           Version: 1.0
                                           Revisions: None

                                                   """

          try:
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    csv = pandas.read_csv(self.goodDataPath + "/" + file)
                    csv.fillna('NULL',inplace=True)
                    csv['Wafer'] = csv['Wafer'].str[6:]
                    csv.to_csv(self.goodDataPath+ "/" + file, index=None, header=True)
                    self.logger.log(self.log_file, "%s: File Transformed successfully!!" % file)
          except Exception as e:
               self.logger.log(self.log_file, "Data Transformation failed because:: %s" % e)
