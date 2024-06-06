#performing data transformation: data cleaning, feature engineering change categorical features to numerical features
import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #creates the pipeline (one hot encoding, standard scaler)
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

class DataTransformationConfig:
    preprocesser_obj_file_path=os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def get_data_transformer_object(self): #creates all the pkl files needed to change categorical values to numerical and viceversa
        
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            #this is a numerical pipeline. this runs on training data 
            num_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")), #imputer handles the missing values
                    ("scaler",StandardScaler())
                ]
                   )
            #this is a categorical pipeline. runs on the training dataset
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")), #imputer handles the missing values the stategy replaces the missing values like here with the most frequent(mode) data
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical columns standard scaling completed")
            logging.info("categorical columns encoding completed")

            #combines the two pipelines ;categorical and numerical
            preprocesser=ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline,numerical_columns),
                    ("cat_pipeline", cat_pipeline,categorical_columns)
                ]
            )
            return preprocesser
        except Exception as e:
            raise CustomException(e,sys)

#data transformation Techniques
    def initiate_data_transformation(self,train_path,test_path): #you get this data from data_ingestion.py
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()

            target_column_name ="math_score"
            numerical_columns = ["writing_score","reading_score"]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("saved preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preprocesser_obj_file_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocesser_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
            
