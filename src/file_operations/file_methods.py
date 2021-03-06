import pickle
import os
import shutil


class File_Operation:
    """
                This class shall be used to save the model after training
                and load the saved model for prediction.

                Written By: Mansoor Baig
                Version: 1.0
                Revisions: None

                """
    def __init__(self, config, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = config['models']

    def save_model(self, model, model_name, cn=9999):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception

            Written By: Mansoor Baig
            Version: 1.0
            Revisions: None
"""
        self.logger_object.log(self.file_object, 'Entered the save_model method of the File_Operation class')
        try:

            if cn == 9999:
                path = os.path.join(self.model_directory, model_name)
            else:
                # create separate directory for each cluster
                path = os.path.join(self.model_directory, 'Cluster'+str(cn))
                model_name = model_name+str(cn)

            # remove previously existing models directory
            if os.path.isdir(path):
                shutil.rmtree(path)

            # make a new directory
            os.makedirs(path)

            with open(path + '/' + model_name + '.sav', 'wb') as f:
                pickle.dump(model, f)  # save the model to file
            self.logger_object.log(self.file_object, 'Model File '+ model_name+' saved. '
                                                     'Exited the save_model method of the Model_Finder class')

            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Model File '+model_name+' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def load_model(self, filename):
        """
                    Method Name: load_model
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception

                    Written By: Mansoor Baig
                    Version: 1.0
                    Revisions: None
        """
        self.logger_object.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav',
                      'rb') as f:
                self.logger_object.log(self.file_object,
                                       'Model File ' + filename + ' loaded. '
                                       'Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self,cluster_number):
        """
                            Method Name: find_correct_model_file
                            Description: Select the correct model based on cluster number
                            Output: The Model file
                            On Failure: Raise Exception

                            Written By: Mansoor Baig
                            Version: 1.0
                            Revisions: None
                """
        self.logger_object.log(self.file_object, 'Entered the find_correct_model_file method'
                                                 ' of the File_Operation class')
        try:
            self.cluster_number= cluster_number
            self.folder_name=self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if self.file.index(str(self.cluster_number)) != -1: # i.e. cluster num found in folder name
                        self.model_name = self.file
                except:
                    continue
            self.logger_object.log(self.file_object, 'Best model for cluster %d is %s'
                                   % (cluster_number, self.model_name))
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class. '
                                   'Returned: %s' % self.model_name)
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in find_correct_model_file method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()

    def get_cluster_model_file(self,cluster_number):
        """
                            Method Name: get_cluster_model_file
                            Description: For a given cluster, this method returns the model pickle file
                            Output: The Model file
                            On Failure: Raise Exception

                            Written By: Mansoor Baig
                            Version: 1.0
                            Revisions: None
                """
        self.logger_object.log(self.file_object, 'Entered the get_cluster_model_file method'
                                                 ' of the File_Operation class')
        try:
            model_folder = self.model_directory + 'Cluster' + str(cluster_number)
            model_file = os.listdir(model_folder)[0]

            with open(model_folder + '/' + model_file, 'rb') as f:
                self.logger_object.log(self.file_object,
                                       'Model file: %s for cluster: %d loaded successfully.'
                                       % (model_file, cluster_number))
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception: %s occurred while loading model file for cluster: %d'
                                   % (e, cluster_number))
            raise Exception()


