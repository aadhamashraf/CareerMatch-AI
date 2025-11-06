import streamlit as st
import fitz  # PyMuPDF
import json
import ollama
import re

st.set_page_config(page_title="CV Parser with Ollama (Optimized)", page_icon="🧠", layout="wide")

st.title("CV Parser using Local LLM (Ollama, Optimized)")

st.markdown("""
Upload a PDF CV and let a local LLM (Ollama) extract structured data — Skills, Education, Projects, and more!  
This version supports **chunked processing** for speed and **automatic aggregation** of all extracted sections.
""")

# -------------------------------
# PDF TEXT EXTRACTION
# -------------------------------
def extract_text_from_pdf(pdf_file):
    """Extracts full text from a PDF file."""
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text.strip()

# -------------------------------
# CHUNKING LOGIC
# -------------------------------
def chunk_text(text, max_length=3000):
    """Split CV text into smaller chunks for faster LLM processing."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# -------------------------------
# OLLAMA ANALYSIS
# -------------------------------
def analyze_cv_chunk(cv_chunk):
    """Analyzes one CV chunk with Ollama."""
    prompt = f"""
You are an expert CV parser. 
Extract structured JSON **only** from this CV portion.

The JSON MUST follow this schema:
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

Text:
\"\"\"{cv_chunk}\"\"\"

Return ONLY the JSON (no explanations, no markdown).
"""
    response = ollama.chat(model="phi", messages=[
        {"role": "user", "content": prompt}
    ])
    content = response["message"]["content"]

    try:
        json_str = content[content.find("{"):content.rfind("}") + 1]
        parsed_json = json.loads(json_str)
    except:
        parsed_json = {}
    return parsed_json

# -------------------------------
# MERGING LOGIC
# -------------------------------
def merge_results(results):
    """Merge multiple chunk results into one aggregated JSON."""
    merged = {
        "name": "",
        "contact": "",
        "summary": "",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "certifications": []
    }

    for r in results:
        if not r:
            continue
        for key, value in r.items():
            if isinstance(value, list):
                merged[key].extend(value)
            elif isinstance(value, str) and value.strip():
                # prefer first non-empty
                if not merged[key]:
                    merged[key] = value.strip()

    # remove duplicates in list-type fields
    for key in ["education", "experience", "projects", "skills", "certifications"]:
        merged[key] = list({json.dumps(i, sort_keys=True) if isinstance(i, dict) else i for i in merged[key]})
        merged[key] = [json.loads(i) if i.startswith("{") else i for i in merged[key]]

    return merged

# -------------------------------
# MAIN APP
# -------------------------------
uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Text (Preview)")
    st.text_area("Extracted CV Text", text[:2000] + ("..." if len(text) > 2000 else ""), height=300)

    if st.button(" Analyze with Ollama"):
        chunks = chunk_text(text)
        st.write(f"Detected {len(chunks)} chunks for processing ")

        results = []
        for i, chunk in enumerate(chunks):
            st.write(f"Analyzing chunk {i+1}/{len(chunks)}...")
            result = analyze_cv_chunk(chunk)
            results.append(result)

        final_result = merge_results(results)

        st.success("CV Parsed Successfully!")
        st.json(final_result)

        # Allow user to download the JSON result
        json_str = json.dumps(final_result, indent=4, ensure_ascii=False)
        st.download_button(
            label="Download Aggregated JSON",
            data=json_str,
            file_name="cv_parsed_aggregated.json",
            mime="application/json"
        )
else:
    st.info("Upload a PDF CV to start parsing.")
