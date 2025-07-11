# bloom-backend/app/services/ai_generator.py
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from app.bloom_data import BLOOM_VERBS
from random import sample

# Load env vars
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = os.getenv("GROQ_MODEL")


def get_bloom_level_name(bloom_code: str) -> str:
    return BLOOM_VERBS.get(bloom_code.upper(), {}).get("name", "Understand")


def get_verbs_for_level(bloom_code: str, count: int = 3) -> list[str]:
    verbs = BLOOM_VERBS.get(bloom_code.upper(), {}).get("verbs", [])
    return sample(verbs, k=min(count, len(verbs)))


def validate_verbs(verbs: list[str], bloom_code: str) -> list[str]:
    allowed = set(BLOOM_VERBS.get(bloom_code.upper(), {}).get("verbs", []))
    return [v for v in verbs if v in allowed]


def llm_generate_multiple_questions(clo: str, topic: str, bloom_code: str, verbs: list[str] = None):
    bloom_code = bloom_code.upper()
    bloom_level = get_bloom_level_name(bloom_code)

    if not verbs:
        verbs = get_verbs_for_level(bloom_code, 3)
    else:
        verbs = validate_verbs(verbs, bloom_code)
        if len(verbs) < 1:
            verbs = get_verbs_for_level(bloom_code, 3)

    prompt = f"""
You are an educational expert helping a teacher write strong exam questions.

Please generate **one detailed and distinct academic question** for each verb in this list:
{verbs}

Constraints:
- All questions must align with Bloom Level {bloom_code} ({bloom_level})
- The question should directly assess this CLO: "{clo}"
- The question must be based on this topic: "{topic}"
- Use the verb in a pedagogically meaningful way
- Avoid generic phrases like "Show the topic..."
- Make each question sound like a real midterm/final exam question
- Use higher-order thinking even at the C2 level, but stay within the level
- Each question should be 1–2 complete academic sentences

Respond only with a JSON array, like this:
[
  {{
    "bloom_code": "C2",
    "bloom_level": "Understand",
    "suggested_verb": "compare",
    "sample_question": "Compare the key features of two types of operating systems and explain how they affect system performance."
  }},
  ...
]
"""

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        # print("🧠 RAW GROQ RESPONSE:\n", content)

        # Extract only the JSON array part from the response
        match = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL)
        if match:
            clean_json = match.group(0)
            return json.loads(clean_json)
        else:
            raise ValueError("❌ No valid JSON array found in LLM response.")

    except Exception as e:
        print("❌ Fallback due to error:", e)
        return [
            {
                "bloom_code": bloom_code,
                "bloom_level": bloom_level,
                "suggested_verb": verb,
                "sample_question": f"{verb.capitalize()} the topic '{topic}' aligned with CLO: {clo}"
            } for verb in verbs
        ]
