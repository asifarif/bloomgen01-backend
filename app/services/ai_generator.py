# bloom-backend/app/services/ai_generator.py
import os
import json
from dotenv import load_dotenv
from groq import Groq
import re

# Load .env variables
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def llm_generate_question(clo: str) -> dict:
    prompt = f"""
You are an academic assistant. Given the CLO below, respond strictly in valid JSON format. Do not include any natural language, markdown, or commentary.

Return the following keys:
- bloom_code: Bloom taxonomy code (C1–C6)
- bloom_level: Bloom level name
- suggested_verb: 1 action verb
- sample_question: academic question aligned with the CLO

CLO: "{clo}"

Respond only with a valid JSON object:
"""
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content
    print("🧠 RAW RESPONSE FROM GROQ:")
    print(content)

    try:
        # Safely strip extra space or newlines
        content_cleaned = content.strip()
        return json.loads(content_cleaned)

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        print("⚠️ Falling back to regex extraction")

        import re
        bloom_code = re.search(r'"?bloom_code"?\s*:\s*"?(C[1-6])"?', content)
        bloom_level = re.search(r'"?bloom_level"?\s*:\s*"?(.*?)"?[,}]', content)
        verb = re.search(r'"?suggested_verb"?\s*:\s*"?(.*?)"?[,}]', content)
        question = re.search(r'"?sample_question"?\s*:\s*"?(.*?)"?[,}]', content)

        return {
            "bloom_code": bloom_code.group(1) if bloom_code else "C4",
            "bloom_level": bloom_level.group(1) if bloom_level else "Analyze",
            "suggested_verb": verb.group(1) if verb else "analyze",
            "sample_question": question.group(1) if question else f"Analyze the following to achieve the CLO: {clo}",
            "raw_response": content
        }
