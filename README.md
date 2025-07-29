


# AI Backlog Assistant

## Project Overview

AI Backlog Assistant is a comprehensive system for processing and analyzing various types of input data (text, audio, video, images) to assist with backlog management. The system consists of multiple modules that work together to extract, process, and analyze information from different sources.

## Modules

### 1. Modality Detector
- **Location**: `modality_detector/`
- **Purpose**: Detects the type of input data (text, audio, video, image)
- **Technologies**: Python, machine learning models

### 2. Input Agent
- **Location**: `input_agent/`
- **Purpose**: Receives extracted data and forwards it to the Reflection Agent
- **Technologies**: FastAPI, Pydantic, CrewAI (mocked)

## Input Agent Module

### Overview

The Input Agent module is responsible for receiving extracted data from various input sources and forwarding it to the Reflection Agent using CrewAI. This module acts as an integration layer between the data extraction modules and the reflection processing pipeline.

### Features

- FastAPI-based REST API for receiving input data
- Pydantic validation for input data structure
- Asynchronous processing for better performance
- Error handling and logging
- Integration with CrewAI for forwarding data to Reflection Agent

### API Endpoint

#### POST /process_input

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

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

```bash
./run_server.sh
```

The server will start on `http://localhost:8000`.

### Testing

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

### Running Tests

```bash
pip install pytest
pytest test_input_agent.py
```

## Development

### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Setup

1. Clone the repository
2. Navigate to the module directory
3. Create and activate a virtual environment
4. Install dependencies

### Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Write tests for your changes
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact the project maintainers.

