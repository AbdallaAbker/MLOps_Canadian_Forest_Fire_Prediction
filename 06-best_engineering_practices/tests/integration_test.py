# integration_test.py
import app
import pytest
from fastapi.testclient import TestClient

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
    # Check if prediction is in the response
    assert 'prediction' in response.json()


if __name__ == '__main__':
    test_predict_endpoint()
