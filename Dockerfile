# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary directories into the container
COPY ./artifacts/models/best_model.joblib ./artifacts/models/best_model.joblib
COPY ./app/ ./app/

# Expose the ports the apps run on
EXPOSE 8500 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.run_app:app", "--host", "0.0.0.0", "--port", "8000"]
