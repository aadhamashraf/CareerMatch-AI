import streamlit as st
import fitz  # PyMuPDF
import json
import ollama
import re

st.set_page_config(page_title="CV Parser with Job Match", page_icon="🧠", layout="wide")
st.title("CV Parser + Job Relevance Scorer (Local LLM with Ollama)")

st.markdown("Upload a PDF CV → Extract structured info → Enter target job → Get relevance score & recommendations.")

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# JSON EXTRACTION HELPERS
# -----------------------------
def extract_json_from_text(text):
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except:
            try:
                json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
                return json.loads(json_str)
            except:
                return {}
    return {}

# -----------------------------
# OLLAMA: CV STRUCTURE PARSER
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
CV Text:
\"\"\"{cv_text}\"\"\" 
Return only JSON.
"""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]
    parsed_json = extract_json_from_text(content)
    return parsed_json

# -----------------------------
# OLLAMA: JOB MATCH SCORER
# -----------------------------
def score_job_relevance(cv_json, job_profile):
    prompt = f"""
You are an ATS + HR expert. 
Compare the CV JSON with the target job profile and return ONLY valid JSON.

SCHEMA:
{{
  "relevance_score": 0-100,
  "fit_level": "", 
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "recommendation": ""
}}

Guidelines:
- Base the score on **skills match**, **experience relevance**, and **project alignment**.
- Fit level must be one of: "Strong Fit", "Moderate Fit", "Needs Improvement", "Weak Fit".
- Recommendation must be a short, actionable paragraph.

CV JSON:
{json.dumps(cv_json)}

Target Job Profile:
\"\"\"{job_profile}\"\"\" 

Return only JSON.
"""

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]
    return extract_json_from_text(content)

# -----------------------------
# STREAMLIT UI
# -----------------------------
uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

job_profile = st.text_area("Enter Target Job Profile", placeholder="Example: Data Scientist with experience in NLP, Python, ML models, deep learning, cloud, APIs...", height=120)

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted CV Text (Preview)")
    st.text_area("Extracted Text", text[:2000] + ("..." if len(text) > 2000 else ""), height=250)

    if st.button("Analyze CV + Evaluate Job Match"):
        with st.spinner("Running CV parsing + job scoring..."):
            cv_data = analyze_cv_with_ollama(text)

            if not cv_data:
                st.error("Error parsing CV. Model returned empty JSON.")
            else:
                st.success("CV Parsed Successfully!")
                st.json(cv_data)

                # Download Parsed JSON
                st.download_button(
                    label="Download CV JSON",
                    data=json.dumps(cv_data, indent=4),
                    file_name="cv_parsed.json",
                    mime="application/json"
                )

                # Only score if job profile exists
                if job_profile.strip():
                    score_result = score_job_relevance(cv_data, job_profile)

                    if score_result:
                        st.subheader("📌 Job Relevance Result")
                        st.json(score_result)

                        st.download_button(
                            label="Download Relevance Score",
                            data=json.dumps(score_result, indent=4),
                            file_name="cv_job_relevance.json",
                            mime="application/json"
                        )
                    else:
                        st.error("Could not compute job relevance score.")
                else:
                    st.warning("Enter a job profile to compute relevance score.")
else:
    st.info("Upload a PDF CV to start.")
