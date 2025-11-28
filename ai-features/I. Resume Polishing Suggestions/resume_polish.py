import openai
import os

# openai.api_key will be read from environment in normal execution
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

def build_system_prompt():
    return """
[SYSTEM PROMPT]

👤 You are a Career Coach and an expert Resume Writer.

🎯 Your task is to take a bullet point from a user's resume and rewrite it to be more professional, powerful, and achievement-oriented.

📝 Rules you must follow:
1.  Start the sentence with a strong "Action Verb" in the past tense.
2.  Use STAR or PAR method where possible; quantify results if available.
3.  Preserve the original meaning and keep the rewrite concise.
4.  Return ONLY the polished sentence.
"""


def polish_resume_sentence_v2(user_bullet_point: str) -> str:
    system_prompt = build_system_prompt()
    user_prompt = f"""
[USER INPUT]
Original: {user_bullet_point}
Polished:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=100
        )
        polished = response.choices[0].message['content'].strip()
        return polished
    except Exception as e:
        return f"Error: Could not polish sentence. {e}"


if __name__ == "__main__":
    test_sentence_1 = "I made some social media posts."
    print(polish_resume_sentence_v2(test_sentence_1))
