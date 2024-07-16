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


with open("../artifacts/yaml/preprocessing-params.yaml") as file:
    preprocessing_params = yaml.load(file, Loader=yaml.FullLoader)
    
experiment_id = preprocessing_params["experiment_id"]
    
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment(experiment_id)


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
    num_columns = preprocessing_params["num_columns"]
    cat_columns = preprocessing_params["cat_columns"]
    target = preprocessing_params["target_column"]

    return modes, medians, num_columns, cat_columns, target


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

        modes, medians, num_columns, cat_columns, target = load_preprocessing_params(preprocessing_params_file)

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

    return best_model, best_model_name, best_accuracy


def register_model(best_model, best_model_name, best_accuracy, model_pipeline_path):
    client = mlflow.tracking.MlflowClient()
    # experiment_id = client.get_experiment_by_name("baseline-model-01").experiment_id
    runs = client.search_runs(experiment_id, order_by=["metrics.accuracy DESC"])

    if len(runs) > 0:
        production_run = runs[0]
        production_accuracy = production_run.data.metrics["accuracy"]

        if best_accuracy > production_accuracy:
            print(f"New model {best_model_name} with accuracy {best_accuracy} is better than production model with accuracy {production_accuracy}. Promoting new model.")
            joblib.dump(best_model, os.path.join(model_pipeline_path, "best_model.joblib"))
            mlflow.register_model(f"runs:/{production_run.info.run_id}/model", "ProductionModel")
            latest_mv = client.get_latest_versions("ProductionModel")[0]
            # client.set_registered_model_alias(model_name= "ProductionModel", latest_mv.version)
            client.transition_model_version_stage(
                name="ProductionModel",
                version=latest_mv.version,
                stage="Archived"
            )
        else:
            print(f"New model {best_model_name} with accuracy {best_accuracy} is not better than production model with accuracy {production_accuracy}.")
    else:
        print(f"No production model found. Registering {best_model_name} as the first production model.")
        joblib.dump(best_model, os.path.join(model_pipeline_path, "best_model.joblib"))
        mlflow.register_model(f"runs:/{best_model_name}/model", "ProductionModel")
        client.transition_model_version_stage(
            name="ProductionModel",
            version=1,
            stage="Production"
        )


if __name__ == "__main__":
    dataset_path = "../data/processed/"
    model_pipeline_path = "../artifacts/models/"
    preprocessing_params_file = "../artifacts/yaml/preprocessing-params.yaml"
    hyperparams_file = "../artifacts/yaml/hyperparams.yaml"

    best_model, best_model_name, best_accuracy = run_hpo_experiment(dataset_path, model_pipeline_path, hyperparams_file)
    register_model(best_model, best_model_name, best_accuracy, model_pipeline_path)
