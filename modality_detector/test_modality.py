

import os
import tempfile
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from main import app, determine_modality

client = TestClient(app)

def test_determine_modality():
    # Test with known MIME types
    assert determine_modality("text/plain") == ("text", "txt")
    assert determine_modality("audio/mpeg") == ("audio", "mp3")
    assert determine_modality("video/mp4") == ("video", "mp4")
    assert determine_modality("image/jpeg") == ("image", "jpg")

    # Test with unknown MIME type but known extension
    assert determine_modality("unknown/type", "example.mp3") == ("audio", "mp3")
    assert determine_modality("unknown/type", "document.pdf") == ("text", "pdf")

    # Test with unknown MIME type and unknown extension
    assert determine_modality("unknown/type", "file.unknown") == ("unknown", "unknown")

def test_text_input():
    response = client.post(
        "/detect-modality",
        data={
            "text": "Hello world",
            "user_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["source_type"] == "text"
    assert data["original_format"] == "txt"
    assert "input_id" in data

def test_file_input():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(b"fake mp3 content")
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            response = client.post(
                "/detect-modality",
                files={"file": ("test.mp3", f, "audio/mpeg")},
                data={
                    "user_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )

        assert response.status_code == 200
        data = response.json()
        assert data["source_type"] == "audio"
        assert data["original_format"] == "mp3"
        assert data["filename"] == "test.mp3"
        assert "input_id" in data
    finally:
        os.unlink(tmp_path)

def test_missing_input():
    response = client.post(
        "/detect-modality",
        data={
            "user_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
    assert response.status_code == 400
    assert "Either file or text must be provided" in response.json()["detail"]

if __name__ == "__main__":
    test_determine_modality()
    test_text_input()
    test_file_input()
    test_missing_input()
    print("All tests passed!")

