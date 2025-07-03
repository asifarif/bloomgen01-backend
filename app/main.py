from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def generate_question(data: CLORequest):
    return {
        "clo": data.clo,
        "suggested_verb": "analyze",
        "sample_question": f"Analyze the following based on CLO: {data.clo}"
    }
