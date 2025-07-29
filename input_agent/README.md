

# Input Agent Module

## Overview

The Input Agent module is responsible for receiving extracted data from various input sources (text, audio, video, image) and forwarding it to the Reflection Agent using CrewAI. This module acts as an integration layer between the data extraction modules and the reflection processing pipeline.

## Features

- FastAPI-based REST API for receiving input data
- Pydantic validation for input data structure
- Asynchronous processing for better performance
- Error handling and logging
- Integration with CrewAI for forwarding data to Reflection Agent

## API Endpoint

### POST /process_input

**Request Body:**
```json
{
  "input_id": "uuid",
  "source_type": "text/audio/video/image",
  "original_format": "mp3/jpg/txt/pdf",
  "extracted_text": "string",
  "confidence_score": 0.95,
  "metadata": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**Response:**
```json
{
  "input_id": "uuid",
  "status": "processed",
  "extracted_text": "string",
  "metadata": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`.

## Testing

You can test the API using curl or any API client:

```bash
curl -X POST "http://localhost:8000/process_input" \
-H "Content-Type: application/json" \
-d '{
  "input_id": "test123",
  "source_type": "text",
  "original_format": "txt",
  "extracted_text": "Sample text for testing",
  "confidence_score": 0.99,
  "metadata": {"test": "data"}
}'
```

## Integration with CrewAI

The module includes a mock function for CrewAI integration. In a production environment, you would replace the `send_to_reflection_agent` function with actual CrewAI SDK calls.

## Error Handling

The module handles various error scenarios:
- Invalid input data (missing fields, wrong types)
- CrewAI communication failures
- Internal server errors

All errors are logged and appropriate HTTP responses are returned.

