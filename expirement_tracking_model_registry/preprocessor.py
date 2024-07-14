

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
    target = preprocessing_params["traget"]
    
    return modes, medians, map_target_column, num_columns, cat_columns, target


def split_dataset(df, cat_columns, num_columns, target):
    """split dataset in train and test"""

    df_train, df_test = train_test_split(df, test_size=0.2,random_state=42)
    X_train = df_train[cat_columns + num_columns]
    y_train = df_train[target]

    X_test = df_test[cat_columns + num_columns]
    y_test = df_test[target]

    return X_train, y_train, X_test, y_test

def features_fillna(df):
    """Fill missing values using the same median and mode values"""
    for col in modes:
        df[col].fillna(modes[col], inplace=True)

    for col in medians:
        df[col].fillna(medians[col], inplace=True)

    return df


def load_model_pipeline(model_pipeline_path):
    
    """Load preprocessing pipleine and model"""
    baseline_model = joblib.load(model_pipeline_path)


if __main__ == "__name__":

    dataset_file_path = "data/raw/dataset.csv"
    model_pipeline_path = "../artiifacts/baseline-model.joblib"
    preprocessing_params_file = "../artiifacts/yaml/preprocessing-params.yaml"
