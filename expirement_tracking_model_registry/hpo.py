import argparse
import os
import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import ParameterGrid
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


mlflow.set_tracking_uri("http://0.0.0.0:5000")
mlflow.set_experiment("baseline-model-01")


def read_dataset(dataset_file_path):
    """Read dataset from the specified location"""
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
    """Load preprocessing pipeline and model"""
    baseline_model = joblib.load(
        os.path.join(model_pipeline_path, "baseline-model.joblib")
    )



def run_hpo_experiment(dataset_path, model_pipeline_path, hyperparams_file):
    best_accuracy = 0
    best_model = None
    best_model_name = None

    with mlflow.start_run():
        X_train = read_dataset(os.path.join(dataset_path, "X_train.csv"))
        y_train = read_dataset(os.path.join(dataset_path, "y_train.csv"))
        X_test = read_dataset(os.path.join(dataset_path, "X_test.csv"))
        y_test = read_dataset(os.path.join(dataset_path, "y_test.csv"))

        modes, medians, map_target_column, num_columns, cat_columns, target = load_preprocessing_params(preprocessing_params_file)

        numeric_transformer = StandardScaler()
        oh_transformer = OneHotEncoder()

        preprocessor = ColumnTransformer(
            [
                ("OneHotEncoder", oh_transformer, cat_columns),
                ("StandardScaler", numeric_transformer, num_columns),
            ]
        )

        with open(hyperparams_file) as file:
            hyperparams = yaml.load(file, Loader=yaml.FullLoader)

        for model_name, params in hyperparams['models'].items():
            print(f"Running experiment for {model_name} with parameters: {params}")
            param_grid = list(ParameterGrid(params))
            for i, param_combination in enumerate(param_grid):
                print(f"Running with parameter set {i + 1}/{len(param_grid)}: {param_combination}")

                if model_name == 'LogisticRegression':
                    model = LogisticRegression(**param_combination)
                elif model_name == 'DecisionTreeClassifier':
                    model = DecisionTreeClassifier(**param_combination)
                elif model_name == 'GaussianNB':
                    model = GaussianNB(**param_combination)
                elif model_name == 'RandomForestClassifier':
                    model = RandomForestClassifier(**param_combination)
                elif model_name == 'SVC':
                    model = SVC(**param_combination)
                else:
                    raise ValueError(f"Unsupported model: {model_name}")

                pipeline = Pipeline(
                    steps=[("preprocessor", preprocessor), ("model", model)]
                )

                pipeline.fit(X_train, y_train)
                y_pred = pipeline.predict(X_test)
                
                accuracy, precision, recall, f1score = accuracy_measures(y_test, y_pred, 'macro')
                print("accuracy: ", accuracy)
                print("precision: ", precision)
                print("recall: ", recall)
                print("f1score: ", f1score)

                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                mlflow.log_metric("f1score", f1score)

                mlflow.log_param(f"{model_name}_params_{i}", param_combination)

                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = pipeline
                    best_model_name = f"{model_name}_model_{i}"
                    
        preprocessing_params = {
        "best_model": best_model,
        "num_columns": num_columns,
        "target_column": "Target",
        'modes': modes,
        'medians': medians,
        'map_target_column': map_target_column
    }

    with open("../artiifacts/yaml/preprocessing-params.yaml", "w") as file:
        yaml.dump(preprocessing_params, file)               

    return best_model, best_model_name, best_accuracy



if __name__ == "__main__":

    dataset_path = "../data/processed/"
    model_pipeline_path = "../artifacts/models/"
    preprocessing_params_file = "../artiifacts/yaml/preprocessing-params.yaml"
    hyperparams_file = "../artiifacts/yaml/hyperparams.yaml"

    run_hpo_experiment(dataset_path, model_pipeline_path, hyperparams_file)
