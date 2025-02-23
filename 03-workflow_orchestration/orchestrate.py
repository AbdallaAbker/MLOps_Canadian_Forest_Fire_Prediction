import os

import joblib
import mlflow
import pandas as pd
import yaml
from prefect import flow, task
from sklearn.compose import ColumnTransformer
# Modelling
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

azure_remote_server_ip_adress = (
    None  # Paste Your Remote server Public IP Adress, e.g. "http://XX.XX.XXX.XXX:5000"
)
if not azure_remote_server_ip_adress:
    # Run locally If you dont provide the VM remote server public IP address
    remote_tracking_uri = 'http://0.0.0.0:5000/'
else:
    remote_tracking_uri = azure_remote_server_ip_adress
mlflow.set_tracking_uri(remote_tracking_uri)
mlflow.set_experiment = 'workflow-orchestration-baseline-model-01'


@task(name='Read_dataset', retries=5, retry_delay_seconds=5)
def read_dataset(dataset_file_path: str):
    """Read dataset from the spicified location"""
    df = pd.read_csv(dataset_file_path)
    return df


@task(name='load_preprocessing_params')
def load_preprocessing_params(preprocessing_params_file: str):
    """Load preprocessing parameters from yaml file in the artifacts folder"""
    with open(preprocessing_params_file) as file:
        preprocessing_params = yaml.load(file, Loader=yaml.FullLoader)

    modes = preprocessing_params['modes']
    medians = preprocessing_params['medians']
    num_columns = preprocessing_params['num_columns']
    cat_columns = preprocessing_params['cat_columns']
    target = preprocessing_params['target_column']

    return modes, medians, num_columns, cat_columns, target


def accuracy_measures(y_test, predictions, avg_method):
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average=avg_method)
    recall = recall_score(y_test, predictions, average=avg_method)
    f1score = f1_score(y_test, predictions, average=avg_method)
    return accuracy, precision, recall, f1score


@task(name='load_model', retries=2, retry_delay_seconds=5)
def load_model_pipeline(model_pipeline_path: str):
    """Load preprocessing pipleine and model"""
    baseline_model = joblib.load(
        os.path.join(model_pipeline_path, 'baseline-model.joblib')
    )


@flow(name='run_expirement', log_prints=True)
def run_expirement(dataset_path: str, model_pipeline_path: str):

    with mlflow.start_run():

        X_train = read_dataset(os.path.join(dataset_path, 'X_train.csv'))
        y_train = read_dataset(os.path.join(dataset_path, 'y_train.csv'))
        X_test = read_dataset(os.path.join(dataset_path, 'X_test.csv'))
        y_test = read_dataset(os.path.join(dataset_path, 'y_test.csv'))

        # baseline_model = load_model_pipeline(model_pipeline_path)
        modes, medians, num_columns, cat_columns, target = load_preprocessing_params(
            preprocessing_params_file
        )

        numeric_transformer = StandardScaler()
        oh_transformer = OneHotEncoder()

        preprocessor = ColumnTransformer(
            [
                ('OneHotEncoder', oh_transformer, cat_columns),
                ('StandardScaler', numeric_transformer, num_columns),
            ]
        )

        baseline_model = Pipeline(
            steps=[('preprocessor', preprocessor),
                   ('lr', LogisticRegression())]
        )

        baseline_model.fit(X_train, y_train)
        y_pred = baseline_model.predict(X_test)

        accuracy, precision, recall, f1score = accuracy_measures(
            y_test, y_pred, 'macro'
        )
        print('accuracy: ', accuracy)
        print('precision: ', precision)
        print('recall: ', recall)
        print('f1score: ', f1score)

        Clasification_Report = classification_report(y_pred, y_test)
        print('Clasification Report: \n', Clasification_Report)
        Confusion_Matrix = confusion_matrix(y_pred, y_test)
        print('Confusion Matrix: \n', Confusion_Matrix)

        # pathlib.Path("model_pipeline_path").mkdir(exist_ok=True)
        joblib.dump(
            baseline_model, os.path.join(
                model_pipeline_path, 'baseline-model.joblib')
        )

        mlflow.sklearn.log_model(
            model_pipeline_path, artifact_path='baseline_model')

        mlflow.log_metric('accuracy', accuracy)
        mlflow.log_metric('precision', precision)
        mlflow.log_metric('recall', recall)
        mlflow.log_metric('f1score', f1score)


if __name__ == '__main__':

    dataset_path = '../artifacts/data/processed/'
    model_pipeline_path = '../artifacts/models/'
    preprocessing_params_file = '../artifacts/configs/yaml/preprocessing-params.yaml'

    run_expirement(dataset_path, model_pipeline_path)
