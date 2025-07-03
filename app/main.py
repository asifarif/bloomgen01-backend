# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bloom Backend is running!"}


class CLORequest(BaseModel):
    clo: str

@app.post("/generate")
def generate_question(data: CLORequest):
    return {
        "clo": data.clo,
        "suggested_verb": "analyze",
        "sample_question": f"Analyze the following based on CLO: {data.clo}"
    }
