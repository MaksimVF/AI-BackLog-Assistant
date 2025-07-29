

import pytest
from fastapi.testclient import TestClient
from main import app, InputData
import uuid

client = TestClient(app)

def test_process_input_success():
    """Test successful processing of input data"""
    test_data = {
        "input_id": str(uuid.uuid4()),
        "source_type": "text",
        "original_format": "txt",
        "extracted_text": "Test input text",
        "confidence_score": 0.95,
        "metadata": {"test_key": "test_value"}
    }

    response = client.post("/process_input", json=test_data)

    assert response.status_code == 200
    assert response.json()["status"] == "processed"
    assert response.json()["input_id"] == test_data["input_id"]
    assert response.json()["extracted_text"] == test_data["extracted_text"]

def test_process_input_missing_id():
    """Test that the system generates an ID if one is not provided"""
    test_data = {
        "source_type": "text",
        "original_format": "txt",
        "extracted_text": "Test input text",
        "confidence_score": 0.95,
        "metadata": {"test_key": "test_value"}
    }

    response = client.post("/process_input", json=test_data)

    assert response.status_code == 200
    assert response.json()["status"] == "processed"
    assert "input_id" in response.json()
    assert len(response.json()["input_id"]) > 0

def test_process_input_invalid_data():
    """Test error handling for invalid input data"""
    test_data = {
        "input_id": "test123",
        "source_type": "text",
        # Missing required fields
    }

    response = client.post("/process_input", json=test_data)

    assert response.status_code == 422  # Unprocessable Entity

def test_process_input_empty_text():
    """Test handling of empty extracted text"""
    test_data = {
        "input_id": str(uuid.uuid4()),
        "source_type": "text",
        "original_format": "txt",
        "extracted_text": "",
        "confidence_score": 0.95,
        "metadata": {"test_key": "test_value"}
    }

    response = client.post("/process_input", json=test_data)

    assert response.status_code == 200
    assert response.json()["status"] == "processed"
    assert response.json()["extracted_text"] == ""

