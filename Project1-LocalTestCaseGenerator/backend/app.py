
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory to sys.path to access tools
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from tools.generate_test_cases import generate_test_cases

app = FastAPI(title="Local Test Case Generator")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestCaseRequest(BaseModel):
    user_story: str
    model: str = "llama3.2"

@app.post("/generate")
async def generate_endpoint(request: TestCaseRequest):
    try:
        # Layer 2: Navigation - Calling Layer 3: Tool
        result = generate_test_cases(request.user_story, request.model)
        
        print(f"DEBUG: Result for '{request.user_story}': {result}") # Debug print
        
        if "error" in result:

            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Local Test Case Generator"}
