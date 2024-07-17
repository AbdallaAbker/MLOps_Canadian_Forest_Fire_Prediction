import datetime
import io
import logging
import random
import time
import uuid

import joblib
import pandas as pd
import psycopg
import pytz
import yaml
############# Evidently Library ###################
from evidently import ColumnMapping
from evidently.metrics import (ColumnDriftMetric, DatasetDriftMetric,
                               DatasetMissingValuesMetric)
from evidently.report import Report

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""
reference_data = pd.read_csv("../data/raw/reference.csv")
raw_data = pd.read_csv("../data/raw/dataset.csv")
model = joblib.load("../artifacts/models/best_model.joblib")

begin = datetime.datetime(2024, 7, 4, 0, 0)
num_features = ["Temperature", "Oxygen", "Humidity", "Drought_Index"]
cat_features = ["Province", "Vegetation_Type", "Fire_Seasonality", "Land_Use"]

column_mapping = ColumnMapping(
    target=None,
    prediction="Target",
    numerical_features=num_features,
    categorical_features=cat_features,
)


report = Report(
    metrics=[
        ColumnDriftMetric(column_name="Target"),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric(),
    ]
)

# Ensure current_data is a DataFrame
# if isinstance(current_data, pd.Series):
#     current_data = current_data.to_frame().T
    
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


def features_fillna(df):
    """Fill missing values using the same median and mode values"""
    for col in modes:
        df[col] = df[col].fillna(modes[col])

    for col in medians:
        df[col] = df[col].fillna(medians[col])

    return df

def prep_db():
    """
    This function ensure these is a database called test, if not it creates a new one
    """
    with psycopg.connect(
        "host=localhost port=5432 user=postgres password=example",
        autocommit=True,
    ) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
        with psycopg.connect(
            "host=localhost port=5432 dbname=test user=postgres password=example"
        ) as conn:
            conn.execute(create_table_statement)


def calculate_metrics_postgresql(curr, i):
    current_data = raw_data.iloc[i : i + 1]
    # current_data = pd.DataFrame(current_data[num_features + cat_features])  #ensure incoming data is a dataframe
    # current_data.fillna(0, inplace=True)
    current_data["Target"] = model.predict(current_data.apply(features_fillna))

    report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    result = report.as_dict()

    prediction_drift = result["metrics"][0]["result"]["drift_score"]
    num_drifted_columns = result["metrics"][1]["result"]["number_of_drifted_columns"]
    share_missing_values = result["metrics"][2]["result"]["current"]["share_of_missing_values"]

    curr.execute(
        "insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
        (
            begin + datetime.timedelta(i),
            prediction_drift,
            num_drifted_columns,
            share_missing_values,
        ),
    )


def batch_monitoring_backfill(modes, medians, num_columns, cat_columns, target):
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect(
        "host=localhost port=5432 dbname=test user=postgres password=example",
        autocommit=True,
    ) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")


if __name__ == "__main__":

    preprocessing_params_file = "../artifacts/yaml/preprocessing-params.yaml"
    modes, medians, num_columns, cat_columns, target = load_preprocessing_params(preprocessing_params_file)
    batch_monitoring_backfill(modes, medians, num_columns, cat_columns, target)