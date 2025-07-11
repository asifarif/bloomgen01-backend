from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.services.ai_generator import llm_generate_multiple_questions
from app.bloom_data import BLOOM_VERBS
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Secure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Updated schema to support optional teacher-selected verbs
class CLORequest(BaseModel):
    clo: str
    topic: str
    bloom_code: str
    verbs: Optional[List[str]] = None

@app.get("/")
def root():
    return {"message": "Bloom AI Backend is running!"}

# ✅ Updated to forward optional verbs
@app.post("/generate")
async def generate_question(data: CLORequest):
    questions = llm_generate_multiple_questions(
        clo=data.clo,
        topic=data.topic,
        bloom_code=data.bloom_code,
        verbs=data.verbs  # ✅ new
    )
    return {"questions": questions}

@app.get("/verbs")
async def list_bloom_verbs():
    return JSONResponse(content=BLOOM_VERBS)
