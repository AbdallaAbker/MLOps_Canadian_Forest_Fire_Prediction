## Section 4: Welcome to the Model Deployment :smiley:

### WepApp deployed on Azure Cloud. website: fire-forest-webapp.azurewebsites.net

![alt text](<../artifacts/images/website.png>)


![alt text](<../artifacts/images/cicd.png>)

The model has been deployed on Azure Wepp service utilizing the CICD pipline with github actions

To run the model on Azure Cloud:
- Provision Azure Web App with container resoure
- Create Container Registry
- Docker set up in local and push container registry:
    docker build -t aabkeropscontainerregistry.azurecr.io/mlops-fireforest:latest .
- Configure the GitHub Deployment center

- locate terminal to the main Dir: cd ./MLOps_Canadian_Forest_Fire_Prediction
- Check the Dockerfile to ensure what is needed for deployment:
    app.py
    The model: artifacts/models/best_model.joblib
    static folder
    template folder
- Utilize the CI/CD pipeline with github actions


### To push docker image into Azure Reigstry:
- Navigate into main directory:
- Run from terminal:
  docker build -t {YOUR-CONTAINER-REGISTRY-NAME}.azurecr.io/{YOUR-DOCKER-IMAGE-NAME}:latest .
  docker login {YOUR-CONTAINER-REGISTRY-NAME}.azurecr.io
  ENTER user name & password
  docker push {YOUR-CONTAINER-REGISTRY-NAME}.azurecr.io/{YOUR-DOCKER-IMAGE-NAME}:latest


### To run the model locally with no docker:
- Navigate into main directory:
  docker build -t test:v1
  docker run -it --rm -p 8000:8000 test:v1
  - To debug the newly created app folder inside docker container run: docker run -it --entrypoint=bash test:v1
  - Run the following command to test the deployment:
    curl -X POST "http://127.0.0.1:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "province": "Alberta",
        "vegetation_type": "Forest",
        "fire_seasonality": "Fall",
        "land_use": "Agricultural",
        "temperature": 19.90336865,
        "oxygen": 33.52953236,
        "humidity": 64.96040337,
        "drought_index": 420.461325
    }'
