# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary directories &files into the docker container
COPY 04-model_deployment/app/ .
COPY ./artifacts/models/best_model.joblib ./artifacts/models/best_model.joblib
COPY ./04-model_deployment/requirements_deployment.txt ./requirements.txt


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run Uvicorn to serve the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
