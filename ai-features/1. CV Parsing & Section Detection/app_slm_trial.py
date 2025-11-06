import streamlit as st
import fitz  # PyMuPDF
import json
import ollama
import re

st.set_page_config(page_title="CV Parser with Ollama (Fixed)", page_icon="🧠", layout="wide")
st.title("CV Parser using Local LLM (Ollama)")

st.markdown("Upload a PDF CV and extract structured info locally (Skills, Education, Projects, etc.)")

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    # Clean up common formatting noise
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# JSON EXTRACTION HELPERS
# -----------------------------
def extract_json_from_text(text):
    """Try to extract JSON-like text even if model response is messy."""
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except:
            try:
                # try cleaning extra commas or trailing text
                json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
                return json.loads(json_str)
            except:
                return {}
    return {}

# -----------------------------
# OLLAMA ANALYSIS
# -----------------------------
def analyze_cv_with_ollama(cv_text):
    prompt = f"""
You are an expert CV parser. 
Extract and return **only valid JSON** with the following schema:
{{
  "name": "",
  "contact": "",
  "summary": "",
  "education": [],
  "experience": [],
  "projects": [],
  "skills": [],
  "certifications": []
}}

Guidelines:
- Fill all applicable fields.
- Aggregate all **skills** and **projects** across the CV.
- No markdown, no text outside JSON.
- Ensure the JSON is syntactically correct.

CV Text:
\"\"\"{cv_text}\"\"\"
Return only JSON.
"""

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]

    parsed_json = extract_json_from_text(content)

    # Debugging info if output empty
    if not parsed_json or all(v == "" or v == [] for v in parsed_json.values()):
        st.warning("Model returned empty JSON. Displaying raw response for debugging:")
        st.code(content[:1000])
    
    return parsed_json

# -----------------------------
# STREAMLIT UI
# -----------------------------
uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("Extracted CV Text (Preview)")
    st.text_area("Extracted Text", text[:2000] + ("..." if len(text) > 2000 else ""), height=250)

    if st.button("Analyze with Ollama"):
        with st.spinner("Analyzing CV... This may take a few seconds ⏳"):
            result = analyze_cv_with_ollama(text)
        
        if result:
            st.success("CV Parsed Successfully!")
            st.json(result)

            # JSON Download
            json_str = json.dumps(result, indent=4, ensure_ascii=False)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="cv_parsed.json",
                mime="application/json"
            )
        else:
            st.error("Could not extract structured data. Try a smaller CV or clearer text.")
else:
    st.info("Upload a PDF CV to start.")
