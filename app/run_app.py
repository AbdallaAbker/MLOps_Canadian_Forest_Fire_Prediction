import streamlit as st
import numpy as np
import joblib
import pandas as pd

# Load the model
def load_model():
    try:
        model = joblib.load("./artifacts/models/best_model.joblib")
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

model = load_model()

# Define the Streamlit app
def main():
    st.title("Forest Fire Prediction App")

    st.write("""
    This app allows you to input features and get a prediction on the likelihood of a forest fire.
    """)

    # Input fields
    province = st.text_input("Province")
    vegetation_type = st.text_input("Vegetation Type")
    fire_seasonality = st.text_input("Fire Seasonality")
    land_use = st.text_input("Land Use")
    temperature = st.number_input("Temperature", value=0.0)
    oxygen = st.number_input("Oxygen", value=0.0)
    humidity = st.number_input("Humidity", value=0.0)
    drought_index = st.number_input("Drought Index", value=0.0)

    if st.button("Predict"):
        if model is not None:
            # Prepare input data
            input_data = {
                'Province': [province],
                'Vegetation_Type': [vegetation_type],
                'Fire_Seasonality': [fire_seasonality],
                'Land_Use': [land_use],
                'Temperature': [temperature],
                'Oxygen': [oxygen],
                'Humidity': [humidity],
                'Drought_Index': [drought_index]
            }
            input_df = pd.DataFrame(input_data)

            # Make prediction
            try:
                prediction = model.predict(input_df)
                st.success(f"Prediction: {prediction[0]}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.error("Model is not loaded. Please check the model path.")

if __name__ == "__main__":
    main()