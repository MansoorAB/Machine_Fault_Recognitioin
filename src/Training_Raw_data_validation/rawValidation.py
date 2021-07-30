import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger





class Raw_Data_validation:

    """
             This class shall be used for handling all the validation done on the Raw Training Data!!.

             Written By: Mansoor Baig
             Version: 1.0
             Revisions: None

             """

    def __init__(self,config, log_file):
        self.Batch_Directory = config['load_data']['raw_data']
        self.schema_path = config['load_data']['train_schema']
        self.raw_validated = config['load_data']['raw_validated']
        self.raw_good = config['load_data']['good_raw']
        self.raw_bad = config['load_data']['bad_raw']
        self.logger = App_Logger()
        self.file = log_file


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
            NumberofColumns = dic['NumberofColumns']

            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumns
            self.logger.log(self.file,message)

        except ValueError:
            self.logger.log(self.file,"ValueError:Value not found inside schema_training.json")
            raise ValueError

        except KeyError:
            self.logger.log(self.file, "KeyError:Key value error incorrect key passed")
            raise KeyError

        except Exception as e:
            self.logger.log(self.file, str(e))
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns


    def manualRegexCreation(self):
        """
                                Method Name: manualRegexCreation
                                Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                            This Regex is used to validate the filename of the training data.
                                Output: Regex pattern
                                On Failure: None

                                 Written By: Mansoor Baig
                                Version: 1.0
                                Revisions: None

                                        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadRawData(self):

        """
                                      Method Name: createDirectoryForGoodBadRawData
                                      Description: This method creates directories to store the Good Data and Bad Data
                                                    after validating the training data.

                                      Output: None
                                      On Failure: OSError

                                       Written By: Mansoor Baig
                                      Version: 1.0
                                      Revisions: None

                                              """

        try:
            if not os.path.isdir(self.raw_validated):
                os.makedirs(self.raw_validated)
                self.logger.log(self.file, "Created directory: %s" % self.raw_validated)

            if not os.path.isdir(self.raw_good):
                os.makedirs(self.raw_good)
                self.logger.log(self.file, "Created directory: %s" % self.raw_good)

            if not os.path.isdir(self.raw_bad):
                os.makedirs(self.raw_bad)
                self.logger.log(self.file, "Created directory: %s" % self.raw_bad)

        except OSError as ex:
            self.logger.log(self.file,"Error while creating Directory %s:" % ex)
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):

        """
                                            Method Name: deleteExistingGoodDataTrainingFolder
                                            Description: This method deletes the directory made  to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Mansoor Baig
                                            Version: 1.0
                                            Revisions: None

                                                    """

        try:
            if os.path.isdir(self.raw_good):
                shutil.rmtree(self.raw_good)
                self.logger.log(self.file, "Deleted directory: %s" %self.raw_good)
        except OSError as s:
            self.logger.log(self.file,"Error while Deleting Directory : %s" %s)
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):

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
            if os.path.isdir(self.raw_bad):
                shutil.rmtree(self.raw_bad)
                self.logger.log(self.file, "Deleted directory: %s" %self.raw_bad)
        except OSError as s:
            self.logger.log(self.file,"Error while Deleting Directory : %s" %s)
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

            source = 'Training_Raw_files_validated/Bad_Raw/'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'TrainingArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"Bad files moved to archive")
                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")
                file.close()
        except Exception as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise e




    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
                    Method Name: validationFileNameRaw
                    Description: This function validates the name of the training csv files as per given name in the schema!
                                 Regex pattern is used to do the validation.If name format do not match the file is moved
                                 to Bad Raw Data folder else in Good raw data.
                    Output: None
                    On Failure: Exception

                    Written By: Mansoor Baig
                    Version: 1.0
                    Revisions: None

                """

        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        #create new directories
        self.createDirectoryForGoodBadRawData()
        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy(self.Batch_Directory + "/" + filename, self.raw_good)
                            self.logger.log(self.file,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(self.Batch_Directory + "/" + filename, self.raw_bad)
                            self.logger.log(self.file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy(self.Batch_Directory + "/" + filename, self.raw_bad)
                        self.logger.log(self.file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(self.Batch_Directory + "/" + filename, self.raw_bad)
                    self.logger.log(self.file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)


        except Exception as e:
            self.logger.log(self.file, "Error occured while validating FileName %s" % e)
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
            self.logger.log(self.file,"Column Length Validation Started!!")
            for file in listdir(self.raw_good):
                csv = pd.read_csv(self.raw_good + "/" + file)
                if csv.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move(self.raw_good + "/" + file, self.raw_bad)
                    self.logger.log(self.file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(self.file, "Column Length Validation Completed!!")
        except OSError:
            self.logger.log(self.file, "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.log(self.file, "Error Occured:: %s" % e)
            raise e

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
            self.logger.log(self.file,"Missing Values Validation Started!!")

            for file in listdir(self.raw_good):
                csv = pd.read_csv(self.raw_good + "/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move(self.raw_good + "/" + file,
                                    self.raw_bad)
                        self.logger.log(self.file,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(self.raw_good + "/" + file, index=None, header=True)
        except OSError:
            self.logger.log(self.file, "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.log(self.file, "Error Occured:: %s" % e)
            raise e












