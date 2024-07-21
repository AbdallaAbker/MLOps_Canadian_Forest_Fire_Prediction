# tests/test_load_model.py
import joblib
import pytest

def test_load_model():
    try:
        model = joblib.load("../artifacts/models/best_model.joblib")
        assert model is not None, "Model should be loaded successfully"
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")