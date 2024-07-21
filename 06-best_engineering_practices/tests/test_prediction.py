# tests/integration_test.py
import pytest
from fastapi.testclient import TestClient
from app import app  # Ensure your FastAPI app is imported correctly

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        '/predict',
        json={
            'province': 'Alberta',
            'vegetation_type': 'Forest',
            'fire_seasonality': 'Fall',
            'land_use': 'Agricultural',
            'temperature': 19.9,
            'oxygen': 33.5,
            'humidity': 65.0,
            'drought_index': 420.4,
        },
    )
    assert response.status_code == 200
    assert 'prediction' in response.json()

if __name__ == '__main__':
    pytest.main()
