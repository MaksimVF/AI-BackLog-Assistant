


#!/bin/bash

# Start the server in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Test text input
echo "Testing text input..."
curl -X POST "http://localhost:8000/detect-modality" \
  -F "text=Hello world" \
  -F "user_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "timestamp=2025-07-29T09:41:00Z"
echo -e "\n"

# Create a test file
echo "Creating test MP3 file..."
echo "fake mp3 content" > test.mp3

# Test file input
echo "Testing file input..."
curl -X POST "http://localhost:8000/detect-modality" \
  -F "file=@test.mp3" \
  -F "user_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "timestamp=2025-07-29T09:41:00Z"
echo -e "\n"

# Clean up
rm test.mp3

# Stop the server
kill $SERVER_PID

echo "Tests completed!"

