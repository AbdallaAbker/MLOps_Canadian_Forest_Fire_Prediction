import argparse
import os
import pickle

import joblib
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


def read_dataset(dataset_file_path):
    """Read dataset from the spicified location"""
    df = pd.read_csv(dataset_file_path)
    return df


def store_data(df, dest_folder_path, file_name):
    """Load dataset to the spicified location"""
    file_path = os.path.join(dest_folder_path, file_name)
    df.to_csv(file_path, index=False)


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


def features_fillna(df, modes, medians):
    """Fill missing values using the same median and mode values"""
    for col in modes:
        df[col] = df[col].fillna(modes[col])

    for col in medians:
        df[col] = df[col].fillna(medians[col])

    return df


def split_dataset(df, cat_columns, num_columns, target):
    """split dataset in train and test"""

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    X_train = df_train[cat_columns + num_columns]
    y_train = df_train[target]

    X_test = df_test[cat_columns + num_columns]
    y_test = df_test[target]

    return X_train, y_train, X_test, y_test


def main(raw_data_path, dest_path, param_path):

    df = read_dataset(raw_data_path)
    modes, medians, num_columns, cat_columns, target = (
        load_preprocessing_params(preprocessing_params_file)
    )
    df = features_fillna(df, modes, medians)
    X_train, y_train, X_test, y_test = split_dataset(
        df, cat_columns, num_columns, target
    )

    # save datasets
    store_data(X_train, dest_path, file_name="X_train.csv")
    store_data(y_train, dest_path, file_name="y_train.csv")
    store_data(X_test, dest_path, file_name="X_test.csv")
    store_data(y_test, dest_path, file_name="y_test.csv")


if __name__ == "__main__":
    
    dataset_file_path = "../artifacts/data/raw/dataset.csv"
    dest_folder_path = f"../artifacts/data/processed/"
    model_pipeline_path = "../artifacts/baseline-model.joblib"
    preprocessing_params_file = "../artifacts/configs/yaml/preprocessing-params.yaml"

    main(dataset_file_path, dest_folder_path, preprocessing_params_file)
