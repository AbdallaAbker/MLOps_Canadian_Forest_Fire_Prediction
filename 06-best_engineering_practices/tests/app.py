import logging

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model
try:
    model = joblib.load('artifacts/models/best_model.joblib')
    logger.info('Model loaded successfully.')
except Exception as e:
    logger.error(f'Error loading the model: {e}')
    raise

app = FastAPI()


# Define the input data model
class ModelInput(BaseModel):
    Province: str
    Vegetation_Type: str
    Fire_Seasonality: str
    Land_Use: str
    Temperature: float
    Oxygen: float
    Humidity: float
    Drought_Index: float


# Define the prediction endpoint
@app.post('/predict')
def predict(data: ModelInput):
    try:
        logger.info(f'Received data: {data}')

        # Convert input data to pandas DataFrame
        scoring_data = {
            'Province': [data.Province],
            'Temperature': [data.Temperature],
            'Oxygen': [data.Oxygen],
            'Humidity': [data.Humidity],
            'Vegetation_Type': [data.Vegetation_Type],
            'Drought_Index': [data.Drought_Index],
            'Fire_Seasonality': [data.Fire_Seasonality],
            'Land_Use': [data.Land_Use],
        }
        scoring_df = pd.DataFrame(scoring_data)

        logger.info(f'Input data converted to DataFrame: {scoring_df}')

        # Make prediction
        prediction = model.predict(scoring_df)
        logger.info(f'Model prediction: {prediction}')

        return {'prediction': str(prediction[0])}
    except Exception as e:
        logger.error(f'Error during prediction: {e}')
        raise HTTPException(status_code=500, detail='Prediction error')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
