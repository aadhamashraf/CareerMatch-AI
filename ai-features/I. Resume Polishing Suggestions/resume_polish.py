# streamlit run resume_polish.py

import streamlit as st
import ollama
import re

st.set_page_config(page_title="Resume Bullet Polisher (Local LLM)", page_icon="📝", layout="wide")
st.title("Resume Bullet Point Polisher using Local LLM (Ollama)")

st.markdown("Rewrite resume bullet points to be more professional, achievement-oriented, and powerful—locally using Ollama.")

def build_system_prompt():
    return """
You are a Career Coach and an expert Resume Writer.

Your task is to take a bullet point from a user's resume and rewrite it to be 
more professional, powerful, and achievement-oriented.

Rules:
1. Start the sentence with a strong Action Verb in past tense 
   (e.g., Developed, Led, Implemented).
2. Apply STAR or PAR structure when possible.
3. Preserve original meaning — do NOT add new information.
4. Keep it concise.
5. Return ONLY the polished sentence, with no explanation.

Training Examples:
Original: "I was in charge of customer support."
Polished: "Provided technical support to over 50 customers daily, resolving 95% of inquiries during first contact."

Original: "I made some social media posts."
Polished: "Managed the company's social media accounts, increasing audience engagement by 15% over 3 months."
"""

def extract_polished_text(raw_output):
    """
    Remove quotes, markdown, and extra whitespace.
    """
    cleaned = raw_output.strip()
    cleaned = cleaned.replace('"', '').replace("'", "")
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def polish_with_ollama(bullet_point):
    system_prompt = build_system_prompt()

    prompt = f"""
[SYSTEM]
{system_prompt}

[USER INPUT]
Original: {bullet_point}
Polished:
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response["message"]["content"]
    return extract_polished_text(raw)

st.subheader("Enter a resume bullet point")

user_input = st.text_area(
    "Your Resume Bullet Point",
    placeholder="Example: I fixed bugs in the backend API and improved performance.",
    height=120
)

if st.button("Polish Bullet Point"):
    if not user_input.strip():
        st.error("Please enter a bullet point first.")
    else:
        with st.spinner("Polishing using local LLM… ✨"):
            polished = polish_with_ollama(user_input)

        st.success("Polished Successfully!")
        st.write("### Polished Bullet")
        st.code(polished, language="markdown")

        st.download_button(
            label="Download Polished Bullet",
            data=polished,
            file_name="polished_bullet.txt",
            mime="text/plain"
        )
else:
    st.info("Enter a bullet point above and click **Polish Bullet Point**.")
