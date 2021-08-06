from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger


class Prediction_Data_validation:
    """
               This class shall be used for handling all the validation done on the Raw Prediction Data!!.

               Written By: Mansoor Baig
               Version: 1.0
               Revisions: None

               """

    def __init__(self, path, config, log_file):
        self.Batch_Directory = path
        self.config = config
        self.good_raw = self.config['predict_data']['good_raw']
        self.bad_raw = self.config['predict_data']['bad_raw']
        self.schema_path = config['predict_data']['prediction_schema']
        self.logger = App_Logger()
        self.log_file = log_file


    def valuesFromSchema(self):
        """
                                Method Name: valuesFromSchema
                                Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                                Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                                On Failure: Raise ValueError,KeyError,Exception

                                 Written By: Mansoor Baig
                                Version: 1.0
                                Revisions: None

                                        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberOfColumns = dic['NumberofColumns']

            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberOfColumns:: %s" % NumberOfColumns
            self.logger.log(self.log_file, message)

        except ValueError:
            self.logger.log(self.log_file,"ValueError:Value not found inside %s" % self.schema_path)
            raise ValueError

        except KeyError:
            self.logger.log(self.log_file, "KeyError:Key value error incorrect key passed")
            raise KeyError

        except Exception as e:
            self.logger.log(self.log_file, str(e))
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns


    def manualRegexCreation(self):

        """
                                      Method Name: manualRegexCreation
                                      Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                                  This Regex is used to validate the filename of the prediction data.
                                      Output: Regex pattern
                                      On Failure: None

                                       Written By: Mansoor Baig
                                      Version: 1.0
                                      Revisions: None

                                              """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadPredictionRawData(self):

        """
                                        Method Name: createDirectoryForGoodBadRawData
                                        Description: This method creates directories to store the Good Data and Bad Data
                                                      after validating the prediction data.

                                        Output: None
                                        On Failure: OSError

                                         Written By: Mansoor Baig
                                        Version: 1.0
                                        Revisions: None

                                                """
        try:
            if not os.path.isdir(self.good_raw):
                os.makedirs(self.good_raw)
                self.logger.log(self.log_file, "Good raw validation directory created.")
            if not os.path.isdir(self.bad_raw):
                os.makedirs(self.bad_raw)
                self.logger.log(self.log_file, "Bad raw validation directory created.")

        except OSError as ex:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def deleteExistingGoodDataPredictionFolder(self):
        """
                                            Method Name: deleteExistingGoodDataTrainingFolder
                                            Description: This method deletes the directory made to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Mansoor Baig
                                            Version: 1.0
                                            Revisions: None

                                                    """
        try:
            if os.path.isdir(self.good_raw):
                shutil.rmtree(self.good_raw)
                self.logger.log(self.log_file,"GoodRaw directory deleted successfully!!")
        except OSError as e:
            self.logger.log(self.log_file,"Error %s while Deleting Directory : %s"
                            % (e, self.config['predict_data']['good_raw']))
            raise OSError

    def deleteExistingBadDataPredictionFolder(self):

        """
                                            Method Name: deleteExistingBadDataTrainingFolder
                                            Description: This method deletes the directory made to store the bad Data.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Mansoor Baig
                                            Version: 1.0
                                            Revisions: None

                                                    """

        try:
            if os.path.isdir(self.bad_raw):
                shutil.rmtree(self.bad_raw)
                self.logger.log(self.log_file,"BadRaw directory deleted before starting validation!!!")
        except OSError as s:
            self.logger.log(self.log_file,"Error while Deleting Directory : %s" %s)
            raise OSError

    def moveBadFilesToArchiveBad(self):


        """
                                            Method Name: moveBadFilesToArchiveBad
                                            Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Mansoor Baig
                                            Version: 1.0
                                            Revisions: None

                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path= self.config['predict_data']['raw_archived']
            if not os.path.isdir(path):
                os.makedirs(path)
            dest = path + 'BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)

            files = os.listdir(self.bad_raw)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(self.bad_raw + f, dest)

            self.logger.log(self.log_file,"Bad files moved to archive")
            if os.path.isdir(self.bad_raw):
                shutil.rmtree(self.bad_raw)
            self.logger.log(self.log_file,"Bad Raw Data Folder Deleted successfully!!")
        except OSError as e:
            self.logger.log(self.log_file, "Error while moving bad files to archive:: %s" % e)
            raise OSError




    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
            Method Name: validationFileNameRaw
            Description: This function validates the name of the prediction csv file as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception

             Written By: Mansoor Baig
            Version: 1.0
            Revisions: None

        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataPredictionFolder()
        self.deleteExistingGoodDataPredictionFolder()
        self.createDirectoryForGoodBadPredictionRawData()

        onlyfiles = [f for f in listdir(self.Batch_Directory) if f.endswith('.csv')]
        try:
            for filename in onlyfiles:
                if re.match(regex, filename):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy(self.Batch_Directory + "/" + filename, self.good_raw)
                            self.logger.log(self.log_file,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)
                        else:
                            shutil.copy(self.Batch_Directory + "/" + filename, self.bad_raw)
                            self.logger.log(self.log_file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy(self.Batch_Directory + "/" + filename, self.bad_raw)
                        self.logger.log(self.log_file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(self.Batch_Directory + "/" + filename, self.bad_raw)
                    self.logger.log(self.log_file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
        except Exception as e:
            self.logger.log(self.log_file, "Error occurred while validating FileName %s" % e)
            raise e


    def validateColumnLength(self,NumberofColumns):
        """
                    Method Name: validateColumnLength
                    Description: This function validates the number of columns in the csv files.
                                 It is should be same as given in the schema file.
                                 If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                                 If the column number matches, file is kept in Good Raw Data for processing.
                                The csv file is missing the first column name, this function changes the missing name to "Wafer".
                    Output: None
                    On Failure: Exception

                     Written By: Mansoor Baig
                    Version: 1.0
                    Revisions: None

             """
        try:
            self.logger.log(self.log_file,"Column Length Validation Started!!")
            for file in listdir(self.good_raw):
                csv = pd.read_csv(self.good_raw + file)
                if csv.shape[1] == NumberofColumns:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(self.good_raw + file, index=None, header=True)
                else:
                    shutil.move(self.good_raw + file, self.bad_raw)
                    self.logger.log(self.log_file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

            self.logger.log(self.log_file, "Column Length Validation Completed!!")
        except OSError:
            self.logger.log(self.log_file, "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.log(self.log_file, "Error Occured:: %s" % e)
            raise e

    def deletePredictionFile(self):

        if os.path.exists(self.config['predict_data']['prediction_final_file']):
            os.remove(self.config['predict_data']['prediction_final_file'])

    def validateMissingValuesInWholeColumn(self):
        """
                                  Method Name: validateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception

                                   Written By: Mansoor Baig
                                  Version: 1.0
                                  Revisions: None

                              """
        try:
            self.logger.log(self.log_file, "Missing Values Validation Started!!")

            for file in listdir(self.good_raw):
                csv = pd.read_csv(self.good_raw + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move(self.good_raw + file, self.bad_raw)
                        self.logger.log(self.log_file,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(self.good_raw + file, index=None, header=True)
        except OSError:
            self.logger.log(self.log_file, "Error Occurred while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.log(self.log_file, "Error Occurred:: %s" % e)
            raise e













