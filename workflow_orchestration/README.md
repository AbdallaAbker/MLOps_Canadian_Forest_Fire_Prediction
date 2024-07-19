Welcome to the Workflow Orchestration Section :wave:

![alt text](../snapshots/prefect.png)

1- locate your terminal directory into Dir: cd ./workflow_orchestration
2- Activate the virtual enviroment in one terminal and run: prefect server start 
3- Open a new seperate terminal and orchestrate.py script against the server started in the previous step. 
4- Make sure to stay in the correct directory Dir: cd ./workflow_orchestration and Run: python orchestrate.py
3- Open a third seperate terminal (Dir: cd ./workflow_orchestration) and activate mlflow server locally and run the following command:
    mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

