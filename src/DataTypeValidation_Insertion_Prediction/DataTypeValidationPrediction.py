import shutil
import sqlite3
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
        self.config = config
        self.good_raw = config['predict_data']['good_raw']
        self.bad_raw = config['predict_data']['bad_raw']
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
            dbFolder = self.config['predict_data']['prediction_db_folder']
            os.makedirs(dbFolder, exist_ok=True)
            conn = sqlite3.connect(dbFolder + DatabaseName + '.db')
            self.logger.log(self.log_file, "Opened %s database successfully" % DatabaseName)
        except ConnectionError:
            self.logger.log(self.log_file, "Error while connecting to database: %s" % ConnectionError)
            raise ConnectionError
        return conn

    def createTableDb(self, DatabaseName, column_names):

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

            # To save execution time on local machine, table DROP is commented and only data is deleted

            conn.execute('DROP TABLE IF EXISTS Good_Raw_Data;')

            for key in column_names.keys():
                type = column_names[key]

                try:
                    conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key, dataType=type))
                except:
                    conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

            conn.close()

            self.logger.log(self.log_file, "Prediction Tables created successfully!!")
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
        onlyfiles = [f for f in listdir(self.good_raw)]

        for file in onlyfiles:
            try:
                with open(self.good_raw + file, "r") as f:
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
                shutil.move(self.good_raw, self.bad_raw)
                self.logger.log(self.log_file, "File Moved Successfully %s" % file)
                conn.close()
                raise e

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

            # Make the CSV output directory
            if not os.path.isdir(self.config['predict_data']['prediction_folder']):
                os.makedirs(self.config['predict_data']['prediction_folder'])

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.config['predict_data']['prediction_file'], 'w', newline=''),
                                 delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(self.log_file, "Prediction consolidated file exported successfully!!!")

        except Exception as e:
            self.logger.log(self.log_file, "File exporting failed. Error : %s" % e)
            raise e





