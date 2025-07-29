

# Modality Detector API

This is a FastAPI-based service that detects the modality (type) of input data (text, audio, video, image) based on MIME type or file extension.

## Features

- Detects file types from uploaded files or text input
- Returns structured metadata about the input
- Supports common formats: txt, docx, pdf, mp3, wav, mp4, avi, jpg, png
- Generates unique input IDs
- Validates input data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/modality-detector.git
cd modality-detector
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Make a POST request to `/detect-modality` with either:
   - A file upload (multipart/form-data)
   - Text input (form data)

Example using curl with a file:
```bash
curl -X POST "http://localhost:8000/detect-modality" \
  -F "file=@example.mp3" \
  -F "user_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "timestamp=2025-07-29T09:41:00Z"
```

Example using curl with text:
```bash
curl -X POST "http://localhost:8000/detect-modality" \
  -F "text=Hello world" \
  -F "user_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "timestamp=2025-07-29T09:41:00Z"
```

## API Response

The API returns a JSON response with the following structure:
```json
{
  "input_id": "uuid",
  "source_type": "text/audio/video/image",
  "original_format": "mp3/jpg/txt/pdf",
  "filename": "example.mp3",
  "user_id": "uuid",
  "timestamp": "2025-07-29T09:41:00Z"
}
```

## Testing

You can test the API using the built-in FastAPI docs at:
```
http://localhost:8000/docs
```

## Dependencies

- FastAPI
- Pydantic
- Uvicorn
- python-multipart

## License

MIT

