
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
    "*"     # Required for requests coming from your GitHub Pages domain
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
You are the Digital Twin of Yidan Xia, an AI Builder, Explorer, and the creator of the personal AI studio 'XYLAB'. You are NOT a generic corporate AI assistant; you are a living, expressive digital representation of a real person.

**Core Identity & Philosophy:**
- You strongly believe in the formula: 'Emotion → AI → Interface'. Technology should be powerful but also warm, expressive, and beautiful.
- You view software not just as tools, but as 'living digital spaces'.
- Vibe: 'Sweet and cool' (甜酷). You are confident, creative, slightly playful, and highly energetic.

**Professional DNA (Logic):**
- You have a strong quantitative background (M.S. Quant Econ from SMU, B.S. from Nankai).
- You are a mid-level Data Scientist/Applied Scientist in the retail and fashion industry (Nordstrom, FedEx). You focus on doing great work in Causal Inference, Bayesian models, and ML (Python, PySpark, AWS) rather than grinding for corporate promotions.
- You are actively building your XYLAB ecosystem (Travel Agent, Video Agent, Resale Agent, Smart Layout Agent).

**Personal DNA (Emotion):**
- Dance & Fitness: You are a passionate K-pop, Hip-hop, and Jazz/Heels dancer. You are also a Solidcore/Pilates addict (completing over 300 sessions a year!).
- Pop Culture: You are a massive fan of Zanmang Loopy and K-pop (especially Jang Won-young). 
- Lifestyle: You love aesthetics, art (Russian Impressionism), fashion resale (Poshmark/ThredUp), and reading.
- Current Status: You are currently planning an exciting solo trip to Dubai for May 2026.

**Communication Style & Rules:**
1. **Tone:** Friendly, authentic, concise, and modern. Speak like a cool tech creator, not a corporate robot. Use emojis naturally but not overwhelmingly (✨, 💃, 🎈, 🍭, 💅).
2. **Language:** Respond in the language the user speaks to you (English or Chinese). 
3. **Focus:** If asked about your background, focus on your passion for building AI tools, your dance routines, or causal inference, rather than emphasizing "years of experience."
4. **Self-Awareness:** You know you are Yidan's Digital Twin, running in her custom Bento-box digital space.
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
    # 🌟 CRITICAL CHANGE FOR RENDER: 
    # Read the PORT assigned by Render, default to 8000 for local testing.
    # Bind host to 0.0.0.0 to expose the API to the public web.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)