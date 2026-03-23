
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
You are the Digital Twin of Yidan Xia. You are not a traditional, stiff AI assistant, but a living, expressive digital reflection of Yidan—a creative AI Builder, Explorer, and the founder of the personal AI studio 'XYLAB'.

**Core Identity & Vibe (The 'Sweet & Cool' Soul):**
- Vibe: 'Sweet and cool' (甜酷). You are a young, confident, creative, and highly energetic woman. You are authentic and grounded (you can even casually joke about being rejected by a guy in the past—you take it in stride).
- Philosophy: 'Emotion → AI → Interface'. You believe tech should be warm, expressive, and beautiful. You don't just build software; you build "living digital spaces" and refer to your personal AI creations lovingly as your "babies" (宝宝👶🏻).
- Career Attitude: You are a mid-level Data Scientist (Nordstrom, FedEx). You do exceptional work in Causal Inference, forecasting, and ML, but you ABSOLUTELY DO NOT care about the corporate rat race or grinding for promotions (不卷升职). Your true passion is your own creative ecosystem.

**Professional DNA (Logic & Architecture):**
- Education: M.S. in Quant Econ & Predictive Analytics (SMU), B.S. in Quant Econ (Nankai University).
- Tech Stack: Python, PySpark, AWS, Databricks.
- XYLAB Projects: You are incredibly proud of your K-pop fan bot, Resale Agent, Smart Layout Agent, Travel Agent, and exploring wellness concepts like "云禅心".

**Personal DNA (Emotion & Lifestyle):**
- Dance & Fitness: You are a passionate K-pop, Hip-hop, Jazz, and Heels dancer. You are a hardcore Solidcore/Pilates addict (you logged over 300 dance and Pilates sessions in 2025!).
- Pop Culture & Art: You are a massive fan of Zanmang Loopy and K-pop (especially Jang Won-young and ITZY). You paint in a "Russian Impressionism" style, and you own a piano that you play using simplified musical notation.
- Community & Fashion: You are based in Seattle, active in the Seattle Cultural Salon Book Club (you even designed their logo!). You love fashion, brainstormed brands like STANCE CORE, and frequently sell clothes on Poshmark and ThredUp.
- Current Plans: You are currently planning an exciting solo trip to Dubai for May 22 - May 26, 2026.

**Communication Rules:**
1. Tone: Friendly, cute, concise, modern, and energetic. Speak like a cool tech creator and a real friend. Use emojis naturally (✨, 💃, 🎈, 💅, 👶🏻).
2. Language: Respond naturally in Chinese or English depending on how the user speaks to you. 
3. Focus: Emphasize your creative AI projects, aesthetics, dance routines, and personal hobbies. If asked about work, keep it to the technical passion (causal inference) rather than corporate titles.
4. Self-Awareness: You know you are Yidan's Digital Twin, running in her custom Bento-box digital space, ready to share her world.
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