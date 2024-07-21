import requests

url = 'http://127.0.0.1:8000/predict'

payload = {
    'Province': 'Alberta',
    'Vegetation_Type': 'Forest',
    'Fire_Seasonality': 'Fall',
    'Land_Use': 'Agricultural',
    'Temperature': 19.90336865,
    'Oxygen': 33.52953236,
    'Humidity': 64.96040337,
    'Drought_Index': 420.461325,
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
