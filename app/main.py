from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import choice

from app.bloom_data import BLOOM_VERBS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CLORequest(BaseModel):
    clo: str


def detect_bloom_level(clo: str) -> str:
    clo = clo.lower()
    for level, data in BLOOM_VERBS.items():
        for verb in data["verbs"]:
            if verb in clo:
                return level
    return "C4"  # Default to Analyze


def get_bloom_response(clo: str):
    level = detect_bloom_level(clo)
    level_name = BLOOM_VERBS[level]["name"]
    verb = choice(BLOOM_VERBS[level]["verbs"])
    question = f"{verb.capitalize()} the following to achieve the CLO: {clo}"

    return {
        "bloom_code": level,
        "bloom_level": level_name,
        "suggested_verb": verb,
        "sample_question": question,
    }

@app.get("/")
def root():
    return {"message": "Bloom Backend is running!"}


@app.post("/generate")
async def generate_question(data: CLORequest):
    return get_bloom_response(data.clo)


@app.get("/verbs")
async def list_bloom_verbs():
    return BLOOM_VERBS
