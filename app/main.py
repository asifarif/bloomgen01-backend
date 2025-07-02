# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/generate")
def generate_question(clo: str):
    # Placeholder logic
    return {
        "clo": clo,
        "suggested_verb": "analyze",
        "sample_question": f"Analyze the following based on CLO: {clo}"
    }
