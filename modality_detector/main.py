
import os
import mimetypes
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class InputMetadata(BaseModel):
    user_id: str
    timestamp: str
    filename: Optional[str] = None

class OutputMetadata(BaseModel):
    input_id: str
    source_type: str
    original_format: str
    filename: Optional[str] = None
    user_id: str
    timestamp: str

def determine_modality(mime_type: str, filename: Optional[str] = None) -> tuple[str, str]:
    """Determine the source type and original format based on MIME type and filename."""
    # Default values
    source_type = "unknown"
    original_format = "unknown"

    # Map MIME types to source types
    mime_type_map = {
        # Text types
        "text/plain": ("text", "txt"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ("text", "docx"),
        "application/pdf": ("text", "pdf"),

        # Audio types
        "audio/mpeg": ("audio", "mp3"),
        "audio/wav": ("audio", "wav"),
        "audio/wave": ("audio", "wav"),
        "audio/x-wav": ("audio", "wav"),

        # Video types
        "video/mp4": ("video", "mp4"),
        "video/x-msvideo": ("video", "avi"),

        # Image types
        "image/jpeg": ("image", "jpg"),
        "image/png": ("image", "png"),
    }

    # If we have a known MIME type
    if mime_type in mime_type_map:
        source_type, original_format = mime_type_map[mime_type]
    # Try to determine from filename extension if MIME type is unknown
    elif filename:
        ext = os.path.splitext(filename)[1].lower()[1:]  # Get extension without dot
        # Map common extensions
        ext_map = {
            "txt": ("text", "txt"),
            "docx": ("text", "docx"),
            "pdf": ("text", "pdf"),
            "mp3": ("audio", "mp3"),
            "wav": ("audio", "wav"),
            "mp4": ("video", "mp4"),
            "avi": ("video", "avi"),
            "jpg": ("image", "jpg"),
            "jpeg": ("image", "jpg"),
            "png": ("image", "png"),
        }
        if ext in ext_map:
            source_type, original_format = ext_map[ext]

    return source_type, original_format

@app.post("/detect-modality", response_model=OutputMetadata)
async def detect_modality(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    timestamp: str = Form(...),
    filename: Optional[str] = Form(None),
):
    # Validate input - either file or text must be provided
    if file is None and text is None:
        raise HTTPException(status_code=400, detail="Either file or text must be provided")

    # Generate input ID
    input_id = str(uuid.uuid4())

    # Handle file input
    if file:
        # Get MIME type from file
        mime_type, _ = mimetypes.guess_type(file.filename)
        if not mime_type:
            # Try to get MIME type from file content
            file_content = await file.read(1024)  # Read first 1024 bytes
            await file.seek(0)  # Reset file pointer
            # Simple content-based detection (very basic)
            if file_content.startswith(b'%PDF'):
                mime_type = "application/pdf"
            elif file_content.startswith(b'ID3') or file_content[6:10] == b'ftypM4A':
                mime_type = "audio/mpeg"
            elif file_content.startswith(b'RIFF') and b'WAVE' in file_content:
                mime_type = "audio/wav"

        source_type, original_format = determine_modality(mime_type, file.filename)
        filename = file.filename

    # Handle text input
    elif text:
        source_type = "text"
        original_format = "txt"
        filename = filename or "input.txt"

    # Create output metadata
    output = OutputMetadata(
        input_id=input_id,
        source_type=source_type,
        original_format=original_format,
        filename=filename,
        user_id=user_id,
        timestamp=timestamp
    )

    # Log the operation
    print(f"Processed input: {output.model_dump()}")

    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
