# bloom-backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.bloom_data import BLOOM_VERBS
from app.services.ai_generator import llm_generate_question  # ✅ new

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Secure later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CLORequest(BaseModel):
    clo: str

@app.get("/")
def root():
    return {"message": "Bloom AI Generator is running!"}

@app.post("/generate")
async def generate_question(data: CLORequest):
    return llm_generate_question(data.clo)

@app.get("/verbs")
async def list_bloom_verbs():
    return BLOOM_VERBS
