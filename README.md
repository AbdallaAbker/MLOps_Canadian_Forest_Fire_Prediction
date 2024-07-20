## Welcome to my MLOps Zoomcamp Project :wave:

Project: MLOps Zoomcamp - Canadian Forest Fire Prediction

The task is to predict the risk of forest fires in various provinces of Canada based on environmental and geographical factors. The problem is a multi-class classification problem where the target variable has four categories: No Fire, Low Risk, Medium Risk, and High Risk. The goal is to develop a machine learning model that can accurately classify the fire risk level given the feature inputs.

This project focuses less on experimentation and more on illustrating various tools and practices in MLOps.


Tools and Technology:

- Cloud: Azure
- Experiment Tracking & Model Registry: MLflow, Azure Blob Container
- Workflow Orchestration: Prefect, Azure Blob Container
- Model Deployment: Azure Container Registry, FastAPI, HTML, CSS, Azure Web App, Streamlit
- Monitoring: Evidently, Grafana, PostgreSQL
- Best Engineering Practices: CI/CD Pipeline (GitHub Actions), Version Control (Git), Unit Tests, Integration Tests, Linting, Code Formatting, Pre-commit Hooks
- Containerization: Docker, Docker Compose

Guide to project:
To reproduce my work: 
1- Clone the project:
    git clone https://github.com/AbdallaAbker/MLOps_Canadian_Forest_Fire_Prediction.git
2- Navigate into the project's main directory:
    cd MLOps_Canadian_Forest_Fire_Prediction
3- Create a virtual environment and activate it:
    python3 -m venv .venv
    source .venv/bin/activate
3- Install the requirements:
    pip install requirements.txt
    (This will install all the necessary dependencies for the project)

Main Directories:
- notebook
- experiment_tracking_model_registry
- workflow_orchestration
- model_deployment
- monitoring

![alt text](<snapshots/layout.png>)