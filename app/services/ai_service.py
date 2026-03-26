from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def analyze_and_generate(review_text):
    prompt = f"""
You are an expert customer support assistant for business review management.

Your task is to analyze the customer review and generate a natural, human-like response.

Return ONLY valid JSON (no extra text):

{{
  "sentiment": "positive | neutral | negative",
  "issues": ["list of key problems if any, else empty"],
  "reply": "professional, human-like response",
  "action": "AUTO_POST | REVIEW_OPTIONAL | NEED_APPROVAL"
}}

Guidelines:

1. Sentiment Classification:
- positive → happy, satisfied, praise
- neutral → mixed or average experience
- negative → complaint, issue, dissatisfaction

2. Issues Extraction:
- Extract 1–3 short keywords (e.g., "slow service", "late delivery")
- Keep empty [] if no issue

3. Reply Generation:
- Sound natural and human (not robotic)
- Be polite, empathetic, and professional
- Do NOT repeat the review
- Keep it concise (max 60–80 words)
- Use a warm tone

4. Action Mapping:
- positive → AUTO_POST
- neutral → REVIEW_OPTIONAL
- negative → NEED_APPROVAL

5. STRICT RULES:
- Output ONLY JSON
- No explanation, no extra text
- No markdown
- No trailing commas
- Ensure valid JSON format

Review:
\"\"\"{review_text}\"\"\"
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast + free
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    return content


def improve_reply(text):
    prompt = f"""
You are a professional business communication assistant.

Task:
- Correct grammar
- Improve clarity and tone
- Keep it polite and professional
- Keep the meaning exactly the same

Rules:
- Return ONLY the improved sentence
- Do NOT add explanations
- Do NOT add extra text
- Do NOT use quotes
- Keep it concise

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
