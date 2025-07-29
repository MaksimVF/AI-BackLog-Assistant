


# AI Backlog Assistant

## Project Overview

AI Backlog Assistant is a comprehensive system for processing and analyzing various types of input data (text, audio, video, images) to assist with backlog management. The system consists of multiple modules that work together to extract, process, and analyze information from different sources.

## Modules

### 1. Modality Detector
- **Location**: `modality_detector/`
- **Purpose**: Detects the type of input data (text, audio, video, image) and extracts basic metadata
- **Technologies**: Python, FastAPI, Pydantic
- **Status**: ✅ Implemented

### 2. Input Agent
- **Location**: `input_agent/`
- **Purpose**: Receives extracted data and forwards it to the Reflection Agent using CrewAI
- **Technologies**: FastAPI, Pydantic, CrewAI (mocked)
- **Status**: ✅ Implemented

### 3. Text Extraction (Planned)
- **Purpose**: Extract text from various file formats (PDF, DOCX, audio, video, images)
- **Technologies**: Tesseract, PyMuPDF, SpeechRecognition, etc.
- **Status**: ⏳ Planned

### 4. Weaviate Storage (Planned)
- **Purpose**: Store processed data in Weaviate vector database for semantic search
- **Technologies**: Weaviate Python client
- **Status**: ⏳ Planned

### 5. CrewAI Integration (Planned)
- **Purpose**: Forward data to Reflection Agent for further processing
- **Technologies**: CrewAI SDK
- **Status**: ⏳ Mocked (ready for integration)

## System Architecture

```
[User Input] → Modality Detector → Text Extraction → Input Agent → [CrewAI] → Reflection Agent
                                                               ↓
                                                        [Weaviate Storage]
```

## Current Implementation

### Modality Detector

Detects input type and returns metadata:

**Endpoint**: `POST /detect-modality`

**Request**:
- File upload or text input
- User metadata

**Response**:
```json
{
  "input_id": "uuid",
  "source_type": "text/audio/video/image",
  "original_format": "mp3/jpg/txt/pdf",
  "filename": "example.txt",
  "user_id": "user123",
  "timestamp": "2025-07-29T12:00:00"
}
```

### Input Agent

Receives extracted data and forwards to CrewAI:

**Endpoint**: `POST /process_input`

**Request**:
```json
{
  "input_id": "uuid",
  "source_type": "text/audio/video/image",
  "original_format": "mp3/jpg/txt/pdf",
  "extracted_text": "string",
  "confidence_score": 0.95,
  "metadata": {
    "filename": "example.txt",
    "user_id": "user123",
    "timestamp": "2025-07-29T12:00:00"
  }
}
```

**Response**:
```json
{
  "input_id": "uuid",
  "status": "processed",
  "extracted_text": "string",
  "metadata": {...}
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MaksimVF/AI-BackLog-Assistant.git
cd AI-BackLog-Assistant
```

2. Set up each module:

**Modality Detector**:
```bash
cd modality_detector
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run_server.sh  # Runs on port 8000
```

**Input Agent**:
```bash
cd input_agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run_server.sh  # Runs on port 8001 (change port in main.py if needed)
```

## Testing

### Modality Detector Tests
```bash
cd modality_detector
pytest test_modality.py
```

### Input Agent Tests
```bash
cd input_agent
pytest test_input_agent.py
```

## Integration Testing

To test the full pipeline:

1. Start both services
2. Send a test file to Modality Detector:
```bash
curl -X POST "http://localhost:8000/detect-modality" \
-F "file=@test.txt" \
-F "user_id=user123" \
-F "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

3. Use the returned metadata to send to Input Agent:
```bash
curl -X POST "http://localhost:8001/process_input" \
-H "Content-Type: application/json" \
-d '{
  "input_id": "uuid_from_modality_detector",
  "source_type": "text",
  "original_format": "txt",
  "extracted_text": "Sample text content",
  "confidence_score": 0.99,
  "metadata": {
    "filename": "test.txt",
    "user_id": "user123",
    "timestamp": "2025-07-29T12:00:00Z"
  }
}'
```

## Roadmap

### Version 0.1 (Current)
- ✅ Modality detection for files and text
- ✅ Input Agent with CrewAI mock integration
- ✅ Basic API endpoints
- ✅ Unit tests

### Version 0.2 (Planned)
- ✅ Text extraction from PDF, DOCX, images
- ✅ Audio transcription for MP3, WAV files
- ✅ Video processing pipeline
- ✅ Weaviate storage integration

### Version 0.3 (Future)
- ✅ Actual CrewAI integration
- ✅ Reflection Agent implementation
- ✅ Advanced semantic search
- ✅ User interface

## Development

### Prerequisites
- Python 3.8+
- Docker (for future containerization)
- Git

### Setup
```bash
git clone https://github.com/MaksimVF/AI-BackLog-Assistant.git
cd AI-BackLog-Assistant
```

### Contributing
1. Create a feature branch
2. Implement your changes
3. Write tests
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the project maintainers.

