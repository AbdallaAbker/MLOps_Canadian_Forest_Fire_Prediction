## Section 3: Welcome to the Workflow Orchestration :smiley:

![alt text](<../artifacts/images/prefect.png>)

- Navigate into directory  Dir: cd ./workflow_orchestration
- Activate the virtual enviroment in one terminal and run: 
  prefect server start 
- Open a new seperate terminal (Dir: cd ./workflow_orchestration) and activate mlflow server locally and run the following command:
    To run locally: mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
    To run on Azure Cloud: mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root wasbs://container-name@storage-account.blob.core.windows.net/mlartifacts -h 0.0.0.0 -p 5000
- Open a third seperate terminal and run orchestrate.py script against the server started in the previous steps.

