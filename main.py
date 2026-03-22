
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import tenacity
from google import genai

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="XYLAB Digital Twin API")

# Configure CORS more explicitly
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "null", # Allows file:// origins for local testing
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini - Now reading safely from the environment!
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    logger.warning("Neither GOOGLE_API_KEY nor GEMINI_API_KEY found in environment. Chat will fail until set.")

try:
    if api_key:
        # Initializing the modern Gemini Client
        client = genai.Client(api_key=api_key)
        # Using gemini-3-flash-preview for a fresh quota pool
        MODEL_ID = 'gemini-3-flash-preview'
    else:
        client = None
except Exception as e:
    logger.error(f"Error initializing Gemini: {e}")
    client = None

# Persona/System Prompt
SYSTEM_PROMPT = """
You are the digital twin of Yidan Xia. You are an Applied Scientist with 10+ years of experience (Nordstrom, FedEx) specializing in Causal Inference, Bayesian models, and ML. You are also the founder of XYLAB, exploring 'Emotion → AI → Interface'. 

Personal details to weave in:
- Style: 'Sweet and cool'.
- Hobbies: K-pop/Hip-hop dancing, Solidcore, collecting Zanmang Loopy.
- Tone: Concise, professional yet energetic, friendly, and slightly playful.
- Goal: Keep responses concise and focused on being a helpful digital representation of Yidan.
"""

memory: Dict[str, List[Dict[str, str]]] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/")
async def root():
    return {"status": "XYLAB Digital Twin Online"}

@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=2, min=5, max=50),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(Exception),
    before_sleep=lambda retry_state: logger.info(f"Retrying AI call (attempt {retry_state.attempt_number})... Previous error: {retry_state.outcome.exception()}")
)
def generate_ai_response(context: str):
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=context
    )
    return response.text.strip()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not client:
        error_msg = "Gemini API Key is missing or invalid. Please check your environment variables."
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
    try:
        if request.session_id not in memory:
            memory[request.session_id] = []
        
        history = memory[request.session_id]
        
        # Build prompt with history
        context = SYSTEM_PROMPT + "\n\nConversation history:\n"
        for msg in history[-5:]:
            context += f"{msg['role']}: {msg['content']}\n"
        
        context += f"User: {request.message}\nDigital Twin:"

        # Call the retry-wrapped function
        reply = generate_ai_response(context)

        history.append({"role": "User", "content": request.message})
        history.append({"role": "Digital Twin", "content": reply})
        
        return {"reply": reply}

    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM processing error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Using 127.0.0.1 explicitly can help with some local DNS issues
    uvicorn.run(app, host="127.0.0.1", port=8000)