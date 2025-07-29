
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InputData(BaseModel):
    input_id: str = None
    source_type: str
    original_format: str
    extracted_text: str
    confidence_score: float
    metadata: Dict[str, Any]

class ResponseData(BaseModel):
    input_id: str
    status: str
    extracted_text: str
    metadata: Dict[str, Any]

# Function to integrate with CrewAI
# Currently mocked, but designed for future CrewAI integration
async def send_to_reflection_agent(data: InputData) -> bool:
    """
    Sends data to Reflection Agent using CrewAI.
    Returns True if successful, False otherwise.
    """
    try:
        # Here we would use CrewAI SDK to send the data
        # For example: crewai.send_to_agent('reflection_agent', data)
        logger.info(f"Sending data to Reflection Agent for input_id: {data.input_id}")

        # For now, simulate successful send
        # In a real implementation, this would be:
        # from crewai import AgentClient
        # client = AgentClient()
        # response = client.send('reflection_agent', data.model_dump())
        # return response.success

        return True
    except Exception as e:
        logger.error(f"Error sending to Reflection Agent: {e}")
        return False

@app.post("/process_input", response_model=ResponseData)
async def process_input(input_data: InputData) -> ResponseData:
    """
    Endpoint to process input data from extraction modules.
    Validates the input, sends it to Reflection Agent via CrewAI,
    and returns a response to the client.
    """
    try:
        # Log received data
        logger.info(f"Received input data with ID: {input_data.input_id}")

        # Validate input data
        if not input_data.input_id:
            input_data.input_id = str(uuid.uuid4())
            logger.info(f"Generated new input_id: {input_data.input_id}")

        # Send data to Reflection Agent
        success = await send_to_reflection_agent(input_data)

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to send data to Reflection Agent"
            )

        # Prepare response
        response = ResponseData(
            input_id=input_data.input_id,
            status="processed",
            extracted_text=input_data.extracted_text,
            metadata=input_data.metadata
        )

        logger.info(f"Successfully processed input_id: {input_data.input_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing input: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Use port 8001 to avoid conflict with modality detector
        log_level="info"
    )
