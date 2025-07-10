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
You are an academic assistant. Given the CLO below, respond **strictly in JSON**. Do NOT include any extra text, markdown, natural language, or explanations.

You MUST return a JSON object in the following format **only**:
{{
  "bloom_code": "C3",
  "bloom_level": "Apply",
  "suggested_verb": "analyze",
  "sample_question": "How would you apply regression analysis to identify trends in disease incidence?"
}}

CLO: "{clo}"

Respond only in JSON format.
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

#    try:
#        return json.loads(content)
#    except json.JSONDecodeError:
#        return {
#            "error": "Failed to parse LLM response as JSON.",
#            "raw_response": content
#        }

    try:
        # Try to parse proper JSON directly
        return json.loads(content)

    except json.JSONDecodeError:
        bloom_code = re.search(r'"?bloom_code"?\s*[:=]\s*"?(C[1-6])"?', content)
        bloom_level = re.search(r'"?bloom_level"?\s*[:=]\s*"?(.*?)"?[,}]', content)
        verb = re.search(r'"?suggested_verb"?\s*[:=]\s*"?(.*?)"?[,}]', content)
        question = re.search(r'"?sample_question"?\s*[:=]\s*"?(.*?)"?[,}]', content)

        return {
            "bloom_code": bloom_code.group(1) if bloom_code else "C4",
            "bloom_level": bloom_level.group(1) if bloom_level else "Analyze",
            "suggested_verb": verb.group(1) if verb else "analyze",
            "sample_question": question.group(1) if question else f"Analyze the following to achieve the CLO: {clo}",
            "raw_response": content
        }
