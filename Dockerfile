# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary directories into the container
COPY ./artifacts/models/best_model.joblib ./artifacts/models/best_model.joblib
COPY ./app.py ./app.py
COPY ./templates ./templates
COPY ./static ./static 
COPY ./requirements.txt ./requirements.txt


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run Uvicorn to serve the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
