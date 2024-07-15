## Canadian Forest Fire Prediction

### Life cycle of Machine learning Project
- Understanding the Problem Statement
- Data Collection
- Data Checks & Discovery
- Exploratory Data Analysis (EDA)
- Data Pre-Processing
- Model Training
- Choose best model


1) Problem statement
    The task is to predict the risk of forest fires in various provinces of Canada based on environmental and geographical factors. The problem is a multi-class classification problem where the target variable has four categories: No Fire, Low Risk, Medium Risk, and High Risk. The goal is to develop a machine learning model that can accurately classify the fire risk level given the feature inputs.

2) Use Case:
- Resource allocation for firefighting efforts.
- Implementing precautionary measures during high-risk periods.

3) Data Collection:
The data consists of 9 column and 1000 rows.

## Dataset Description
The dataset consists of the following features:
- Province: The Canadian province where the data was recorded. (Categorical)
- Temperature: The ambient temperature in degrees Celsius. (Numerical)
- Oxygen: The oxygen concentration in the air in percentage. (Numerical)
- Humidity: The relative humidity in percentage. (Numerical)
- Vegetation_Type: The type of vegetation in the area. (Categorical)
- Drought_Index: The drought index, which is a measure of dryness, where higher values indicate more severe drought. (Numerical)
- Fire_Seasonality: The season during which the data was recorded. (Categorical)
- Land_Use: The type of land use in the area. (Categorical)
- Target: The risk level of forest fire. (Categorical)



A guide to run the two jupyter notebooks:
- Create virtual enviroment utilizing the requirements.txt file in the main directory
- Activate virtual enviroment 
- EDA.ipynb:
    ## Data Checks to perform
    - Check Missing values
    - Check Duplicates
    - Check data type
    - Check the number of unique values of each column
    - Check statistics of data set
    - Check various categories present in the different categorical column
    - EDA (various Visulizations)

- Preprocessing_and_Model_Training.ipynb:
    - Identify categorical, numerical, and target column
    - Store median, mode, cat_column, nu_column, target_column in YAML file for reproducibility
    - Preprocessing for Categorical & Numerical columns by applying one-hot encoding for categorical columns & standard scaler for for numerical columns
    - Utilize scikit-learn Pipeline for model training 
    - Create ML Pipeline for downstream usage


![alt text](snapshots/pairplot.png)

![alt text](snapshots/scikit-learn-Pipeline.png)