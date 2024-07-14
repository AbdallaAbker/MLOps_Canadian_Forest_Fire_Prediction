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


def store_data(df, dest_file_path, file_name):
    """Load dataset to the spicified location"""
    file_path = os.path.join(dest_file_path, file_name)
    df.to_csv(file_path, index=False)


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


def features_fillna(df, modes, medians):
    """Fill missing values using the same median and mode values"""
    for col in modes:
        df[col].fillna(modes[col], inplace=True)

    for col in medians:
        df[col].fillna(medians[col], inplace=True)

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
    modes, medians, map_target_column, num_columns, cat_columns, target = (
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


# def load_model_pipeline(model_pipeline_path):

#     """Load preprocessing pipleine and model"""
#     baseline_model = joblib.load(model_pipeline_path)

if __name__ == "__main__":
    file_name = ""
    dataset_file_path = "../data/raw/dataset.csv"
    dest_file_path = f"../data/processed/"
    model_pipeline_path = "../artiifacts/baseline-model.joblib"
    preprocessing_params_file = "../artiifacts/yaml/preprocessing-params.yaml"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_data_path",
        default=dataset_file_path,
        help="the location where the raw red wine quality data was saved",
    )
    parser.add_argument(
        "--dest_path",
        default=dest_file_path,
        help="the location where the resulting files will be saved.",
    )

    parser.add_argument(
        "--param_path",
        default=preprocessing_params_file,
        help="the location where the preprocessing param stored in a yaml file ",
    )

    args = parser.parse_args()
    main(args.raw_data_path, args.dest_path, args.param_path)
