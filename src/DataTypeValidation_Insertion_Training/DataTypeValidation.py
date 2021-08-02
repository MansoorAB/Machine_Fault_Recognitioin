import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from application_logging.logger import App_Logger


class dBOperation:
    """
      This class shall be used for handling all the SQL operations.

      Written By: Mansoor Baig
      Version: 1.0
      Revisions: None

      """
    def __init__(self, config, log_file):
        self.badFilePath = config['validate_data']['bad_raw']
        self.goodFilePath = config['validate_data']['good_raw']
        self.path = config['prepare_data']['train_db_folder']
        self.fileFromDb = config['prepare_data']['train_folder']
        self.fileName = config['prepare_data']['train_file']
        self.logger = App_Logger()
        self.log_file = log_file


    def dataBaseConnection(self,DatabaseName):

        """
                Method Name: dataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError

                 Written By: Mansoor Baig
                Version: 1.0
                Revisions: None

                """
        try:
            os.makedirs(self.path, exist_ok=True)
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
            self.logger.log(self.log_file, "Opened %s database successfully" % DatabaseName)
        except ConnectionError:
            self.logger.log(self.log_file, "Error while connecting to database: %s" %ConnectionError)
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):
        """
                        Method Name: createTableDb
                        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
                        Output: None
                        On Failure: Raise Exception

                         Written By: Mansoor Baig
                        Version: 1.0
                        Revisions: None

                        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
                self.logger.log(self.log_file, "Training table already exists!!")
                self.logger.log(self.log_file, "Closed %s database successfully" % DatabaseName)

            else:

                for key in column_names.keys():
                    type = column_names[key]

                    #in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))


                conn.close()

                self.logger.log(self.log_file, "Training table newly created successfully!!")
                self.logger.log(self.log_file, "Closed %s database successfully" % DatabaseName)

        except Exception as e:
            self.logger.log(self.log_file, "Error while creating table: %s " % e)
            conn.close()
            self.logger.log(self.log_file, "Closed %s database successfully" % DatabaseName)
            raise e


    def insertIntoTableGoodData(self,Database):

        """
                               Method Name: insertIntoTableGoodData
                               Description: This method inserts the Good data files from the Good_Raw folder into the
                                            above created table.
                               Output: None
                               On Failure: Raise Exception

                                Written By: Mansoor Baig
                               Version: 1.0
                               Revisions: None

        """

        conn = self.dataBaseConnection(Database)
        onlyfiles = [f for f in listdir(self.goodFilePath)]

        for file in onlyfiles:
            try:
                with open(self.goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                conn.commit()
                            except Exception as e:
                                raise e
                self.logger.log(self.log_file, " %s: File loaded successfully!!" % file)
            except Exception as e:
                conn.rollback()
                self.logger.log(self.log_file,"Error while creating table: %s " % e)
                shutil.move(self.goodFilePath+'/' + file, self.badFilePath)
                self.logger.log(self.log_file, "File Moved Successfully %s" % file)
                conn.close()

        conn.close()


    def selectingDatafromtableintocsv(self,Database):

        """
                               Method Name: selectingDatafromtableintocsv
                               Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                            above created .
                               Output: None
                               On Failure: Raise Exception

                                Written By: Mansoor Baig
                               Version: 1.0
                               Revisions: None

        """

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(self.log_file, "File exported successfully!!!")

        except Exception as e:
            self.logger.log(self.log_file, "File exporting failed. Error : %s" %e)





