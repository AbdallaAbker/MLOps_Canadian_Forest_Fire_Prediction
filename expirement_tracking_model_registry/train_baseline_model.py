import argparse
import os

import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer

from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score

# Modelling
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

mlflow.set_tracking_uri = "http://0.0.0.0:5000"
mlflow.set_experiment = "baseline-model-01"


def read_dataset(dataset_file_path):
    """Read dataset from the spicified location"""
    df = pd.read_csv(dataset_file_path)
    return df


def load_preprocessing_params(preprocessing_params_file):
    """Load preprocessing parameters from yaml file in the artifacts folder"""
    with open(preprocessing_params_file) as file:
        preprocessing_params = yaml.load(file, Loader=yaml.FullLoader)

    modes = preprocessing_params["modes"]
    medians = preprocessing_params["medians"]
    map_target_column = preprocessing_params["map_target_column"]
    num_columns = preprocessing_params["num_columns"]
    cat_columns = preprocessing_params["cat_columns"]
    target = preprocessing_params["target_column"]

    return modes, medians, map_target_column, num_columns, cat_columns, target


def accuracy_measures(y_test, predictions, avg_method):
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average=avg_method)
    recall = recall_score(y_test, predictions, average=avg_method)
    f1score = f1_score(y_test, predictions, average=avg_method)
    return accuracy, precision, recall, f1score


def load_model_pipeline(model_pipeline_path):
    """Load preprocessing pipleine and model"""
    baseline_model = joblib.load(
        os.path.join(model_pipeline_path, "baseline-model.joblib")
    )


def run_expirement(dataset_path, model_pipeline_path):

    with mlflow.start_run():

        X_train = read_dataset(os.path.join(dataset_path, "X_train.csv"))
        y_train = read_dataset(os.path.join(dataset_path, "y_train.csv"))
        X_test = read_dataset(os.path.join(dataset_path, "X_test.csv"))
        y_test = read_dataset(os.path.join(dataset_path, "y_test.csv"))

        # baseline_model = load_model_pipeline(model_pipeline_path)
        modes, medians, map_target_column, num_columns, cat_columns, target = (
            load_preprocessing_params(preprocessing_params_file)
        )

        # mlflow.log_params("modes": modes, "median": medians, "map_target_column": map_target_column, "num_columns": num_columns, "cat_columns": cat_columns, "target": target)

        numeric_transformer = StandardScaler()
        oh_transformer = OneHotEncoder()

        preprocessor = ColumnTransformer(
            [
                ("OneHotEncoder", oh_transformer, cat_columns),
                ("StandardScaler", numeric_transformer, num_columns),
            ]
        )

        baseline_model = Pipeline(
            steps=[("preprocessor", preprocessor), ("lr", LogisticRegression())]
        )

        baseline_model.fit(X_train, y_train)

        joblib.dump(
            baseline_model, os.path.join(model_pipeline_path, "baseline-model.joblib")
        )

        mlflow.log_artifacts(model_pipeline_path, "baseline_model")
        y_pred = baseline_model.predict(X_test)
        
        accuracy, precision, recall, f1score = accuracy_measures(y_test, y_pred, 'macro')
        print("accuracy: ", accuracy)
        print("precision: ", precision)
        print("recall: ", recall)
        print("f1score: ", f1score)

        Clasification_Report = classification_report(y_pred, y_test)
        print("Clasification Report: \n", Clasification_Report)
        Confusion_Matrix = confusion_matrix(y_pred, y_test)
        print("Confusion Matrix: \n", Confusion_Matrix)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1score", f1score)
        

if __name__ == "__main__":

    dataset_path = "../data/processed/"
    model_pipeline_path = "../artiifacts/models/"
    preprocessing_params_file = "../artiifacts/yaml/preprocessing-params.yaml"

    run_expirement(dataset_path, model_pipeline_path)
