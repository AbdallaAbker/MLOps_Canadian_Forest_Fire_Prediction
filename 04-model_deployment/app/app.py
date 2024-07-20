from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model
try:
    model = joblib.load("artifacts/models/best_model.joblib")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading the model: {e}")
    model = None

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(
    request: Request,
    province: str = Form(...),
    vegetation_type: str = Form(...),
    fire_seasonality: str = Form(...),
    land_use: str = Form(...),
    temperature: float = Form(...),
    oxygen: float = Form(...),
    humidity: float = Form(...),
    drought_index: float = Form(...)
):
    try:
        data = {
            'Province': [province],
            'Vegetation_Type': [vegetation_type],
            'Fire_Seasonality': [fire_seasonality],
            'Land_Use': [land_use],
            'Temperature': [temperature],
            'Oxygen': [oxygen],
            'Humidity': [humidity],
            'Drought_Index': [drought_index]
        }
        df = pd.DataFrame(data)

        if model is None:
            return {"error": "Model is not loaded"}

        prediction = model.predict(df)
        prediction_result = str(prediction[0])
        return templates.TemplateResponse("index.html", {"request": request, "prediction": prediction_result})
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return templates.TemplateResponse("index.html", {"request": request, "error": "Prediction error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
