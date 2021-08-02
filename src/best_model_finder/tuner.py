from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
import json
import numpy as np


class Model_Finder:
    """
                This class shall  be used to find the model with best accuracy and AUC score.
                Written By: Mansoor Baig
                Version: 1.0
                Revisions: None

                """

    def __init__(self,config,file_object,logger_object):
        self.config = config
        self.file_object = file_object
        self.logger_object = logger_object
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')

    def get_best_params_for_random_forest(self,cn,train_x,train_y):
        """
                                Method Name: get_best_params_for_random_forest
                                Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                                             Use Hyper Parameter Tuning.
                                Output: The model with the best parameters
                                On Failure: Raise Exception

                                Written By: Mansoor Baig
                                Version: 1.0
                                Revisions: None

                        """
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_random_forest method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid = {"n_estimators": self.config['estimators']['RandomForest']['params']['n_estimators'],
                               "criterion": self.config['estimators']['RandomForest']['params']['criterion'],
                               "max_depth": self.config['estimators']['RandomForest']['params']['max_depth'],
                               "max_features": self.config['estimators']['RandomForest']['params']['max_features']}

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid,
                                     verbose=self.config['estimators']['GridSearchCV']['params']['verbose'],
                                     cv=self.config['estimators']['GridSearchCV']['params']['cv'])

            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # dump the best parameters to json file
            params_file = self.config['reports']['params']

            with open(params_file, "a") as f:
                params = {
                    "cluster#": int(cn),
                    "model#": "RandomForest",
                    "criterion": self.criterion,
                    "max_depth": self.max_depth,
                    "max_features": self.max_features,
                    "n_estimators": self.n_estimators
                }
                json.dump(params, f, indent=4)
                f.write('\n')

            #creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # training the mew model
            self.clf.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'Random Forest best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return self.clf
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_random_forest method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Random Forest Parameter tuning  failed. Exited the get_best_params_for_random_forest method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_xgboost(self,cn,train_x,train_y):

        """
                                        Method Name: get_best_params_for_xgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        On Failure: Raise Exception

                                        Written By: Mansoor Baig
                                        Version: 1.0
                                        Revisions: None

                                """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_params_for_xgboost method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_xgboost = {
                'learning_rate': self.config['estimators']['XGBoost']['params']['learning_rate'],
                'max_depth': self.config['estimators']['XGBoost']['params']['max_depth'],
                'n_estimators': self.config['estimators']['XGBoost']['params']['n_estimators']
            }

            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),self.param_grid_xgboost,
                                    verbose=self.config['estimators']['GridSearchCV']['params']['verbose'],
                                    cv=self.config['estimators']['GridSearchCV']['params']['cv'])

            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # dump the best parameters to json file
            params_file = self.config['reports']['params']

            with open(params_file, "a") as f:
                params = {
                    "cluster#": int(cn),
                    "model#": "XGBoost",
                    "learning_rate": self.learning_rate,
                    "max_depth": self.max_depth,
                    "n_estimators": self.n_estimators
                }
                json.dump(params, f, indent=4)
                f.write('\n')

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'XGBoost best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()


    def get_best_model(self,cluster_num, train_x,train_y,test_x,test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                On Failure: Raise Exception

                                                Written By: Mansoor Baig
                                                Version: 1.0
                                                Revisions: None

                                        """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        # create best model for XGBoost
        try:
            self.xgboost= self.get_best_params_for_xgboost(cluster_num,train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x) # Predictions using the XGBoost Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost) # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score)) # Log AUC

            # create best model for Random Forest
            self.random_forest=self.get_best_params_for_random_forest(cluster_num,train_x,train_y)
            self.prediction_random_forest=self.random_forest.predict(test_x) # prediction using the Random Forest Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)
                self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest) # AUC for Random Forest
                self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.random_forest_score))

            # dump the comparison scores to json file
            scores_file = self.config['reports']['scores']

            with open(scores_file, "a") as f:
                scores = {
                    "cluster#": int(cluster_num),
                    "XGBoost Score": self.xgboost_score,
                    "RF Score": self.random_forest_score
                }
                self.logger_object.log(self.file_object, 'Writing scores for cluster: %d' % cn)
                json.dump(scores, f, indent=4)
                f.write('\n')

            #comparing the two models
            if(self.random_forest_score <  self.xgboost_score):
                return 'XGBoost',self.xgboost
            else:
                return 'RandomForest',self.random_forest





        except Exception as e:
                self.logger_object.log(self.file_object,
                                       'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                           e))
                self.logger_object.log(self.file_object,
                                       'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
                raise Exception()

