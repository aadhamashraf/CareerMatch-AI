"""Course recommender module (migrated into numbered directory)

Moved from `copy_of_skill_gap_course_recommender.py` and renamed to
`course_recommender.py` to match the numbered directory layout.
"""

import json, re
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np

USE_EMB = True
try:
    from sentence_transformers import SentenceTransformer, util as sbert_util
    EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    print("Embeddings not available; falling back to TF-IDF only.", e)
    USE_EMB = False
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

try:
    from google.colab import files
    COLAB = True
except Exception:
    COLAB = False

cv = None
if COLAB:
    print("Upload your CV JSON (e.g., cv_parsed.json)")
    up = files.upload()
    if len(up) > 0:
        fname = list(up.keys())[0]
        with open(fname, "r", encoding="utf-8") as f:
            cv = json.load(f)
        print("Loaded CV from:", fname)
else:
    cv = None

job_title = "Machine Learning Engineer"
job_description = (
    "Design and deploy ML systems using Python, NumPy/Pandas, scikit-learn, "
    "deep learning (TensorFlow/PyTorch), FastAPI/Flask, Docker, and cloud (AWS/GCP)."
)

essential_skills = []

DEFAULT_SKILLS_BY_TITLE = {
    "data scientist": ["Python","Pandas","NumPy","Scikit-Learn","SQL","Data Visualization","Statistics","ML Ops"],
    "machine learning engineer": ["Python","Pandas","NumPy","Scikit-Learn","TensorFlow","PyTorch","Docker","AWS","FastAPI","SQL"],
    "deep learning engineer": ["Python","PyTorch","TensorFlow","NumPy","Computer Vision","NLP","CUDA","Docker","AWS","MLOps"],
    "backend developer": ["Python","Django","FastAPI","PostgreSQL","Docker","CI/CD","AWS"],
    "frontend developer": ["JavaScript","React","TypeScript","HTML","CSS","REST","Testing"],
    "data analyst": ["SQL","Excel","Python","Pandas","Data Visualization","Power BI","Tableau"],
}

def infer_essential_skills(title: str) -> List[str]:
    t = (title or "").strip().lower()
    for k, v in DEFAULT_SKILLS_BY_TITLE.items():
        if k in t:
            return v
    return ["Python","SQL","Git"]

if not essential_skills:
    essential_skills = infer_essential_skills(job_title)


def normalize_token(token: str) -> str:
    return re.sub(r"[^a-z0-9#+]+", "", token.lower())

def cv_to_text(cv_obj: Dict) -> str:
    parts = []
    if cv_obj.get("summary"):
        parts.append(str(cv_obj["summary"]))

    sk = cv_obj.get("skills")
    if isinstance(sk, dict):
        for v in sk.values():
            if isinstance(v, list): parts.append(" ".join(map(str, v)))
            elif isinstance(v, str): parts.append(v)
    elif isinstance(sk, list):
        parts.append(" ".join(map(str, sk)))

    for p in cv_obj.get("projects", []) or []:
        if isinstance(p, dict):
            for k in ("name","description","tech"):
                if p.get(k):
                    if isinstance(p[k], list): parts.append(" ".join(map(str, p[k])))
                    else: parts.append(str(p[k]))
        else:
            parts.append(str(p))

    for key in ["experience","education","certifications"]:
        if key in cv_obj and cv_obj[key]:
            parts.append(str(cv_obj[key]))
    return "\n".join(parts)


def collect_skill_tokens(cv_obj: Dict) -> set:
    tokens = set()
    sk = cv_obj.get("skills")
    if isinstance(sk, dict):
        for v in sk.values():
            if isinstance(v, list):
                for s in v: tokens.add(normalize_token(str(s)))
            elif isinstance(v, str):
                tokens.add(normalize_token(v))
    elif isinstance(sk, list):
        for s in sk: tokens.add(normalize_token(str(s)))
    text = cv_to_text(cv_obj)
    for s in re.split(r"[\,\s/()\-]+", text):
        if s: tokens.add(normalize_token(s))
    return tokens


def skill_gaps(cv_obj: Dict, essential: List[str]) -> Tuple[List[str], List[str]]:
    have = collect_skill_tokens(cv_obj)
    req = [normalize_token(s) for s in essential]
    missing, present = [], []
    for raw in essential:
        tok = normalize_token(raw)
        if tok in have: present.append(raw)
        else: missing.append(raw)
    return missing, present


data = [
    ("c1","Python for Data Science","Coursera",20,"Beginner","Learn Python, NumPy, Pandas for data analysis and ML basics."),
    ("c2","Advanced Scikit-Learn","Udemy",12,"Intermediate","Model selection, pipelines, feature engineering with scikit-learn."),
    ("c3","Deep Learning with PyTorch","Coursera",25,"Intermediate","Neural networks, CNNs, training pipelines with PyTorch."),
    ("c4","TensorFlow in Practice","Coursera",30,"Intermediate","TensorFlow models, Keras, deployment basics."),
    ("c5","SQL for Analytics","edX",15,"Beginner","Core SQL queries, joins, aggregations for analytics."),
    ("c6","Docker Essentials","Udemy",8,"Beginner","Containerization concepts, building and running images."),
    ("c7","FastAPI for ML APIs","Udemy",10,"Intermediate","Create fast APIs for ML inference with FastAPI."),
    ("c8","AWS Fundamentals","Coursera",18,"Beginner","Core AWS services, IAM, S3, EC2 for beginners."),
    ("c9","Pandas Mastery","DataCamp",10,"Beginner","Data wrangling and analysis with Pandas."),
    ("c10","MLOps Foundations","Coursera",22,"Intermediate","CI/CD, model monitoring, Docker, cloud workflows."),
]
catalog = pd.DataFrame(data, columns=["id","title","provider","hours","level","description"])
catalog["text"] = (catalog["title"] + " " + catalog["description"]).str.lower()

TIME_BUDGET_H = None
if TIME_BUDGET_H is not None:
    catalog = catalog[catalog["hours"] <= TIME_BUDGET_H].reset_index(drop=True)


def sbert_score(query: str, docs: List[str]) -> np.ndarray:
    q_emb = EMB_MODEL.encode([query], convert_to_tensor=True, normalize_embeddings=True)
    d_emb = EMB_MODEL.encode(docs, convert_to_tensor=True, normalize_embeddings=True)
    sims = sbert_util.cos_sim(q_emb, d_emb).cpu().numpy()[0]
    sims = (sims - sims.min()) / (sims.max() - sims.min() + 1e-8)
    return sims


def tfidf_score(query: str, docs: List[str]) -> np.ndarray:
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=1)
    X = vec.fit_transform([query] + docs)
    sims = (X[0] @ X[1:].T).toarray()[0]
    if sims.max() > 0: sims = sims / sims.max()
    return sims


def semantic_scores(query: str, docs: List[str]) -> np.ndarray:
    if USE_EMB:
        return sbert_score(query.lower(), docs)
    return tfidf_score(query.lower(), docs)


def recommend_for_skill(skill: str, df: pd.DataFrame, topk=3) -> pd.DataFrame:
    docs = df["text"].tolist()
    sims = semantic_scores(skill, docs)
    df = df.copy()
    df["score"] = sims
    df = df.sort_values("score", ascending=False)
    picks, seen = [], set()
    for _, row in df.iterrows():
        key = row["title"].split()[0].lower()
        if key not in seen:
            picks.append(row)
            seen.add(key)
        if len(picks) >= topk:
            break
    return pd.DataFrame(picks)


def recommend_courses(cv_obj: Dict, essential: List[str], catalog_df: pd.DataFrame, k_per_skill: int = 3) -> Dict[str, pd.DataFrame]:
    missing, present = skill_gaps(cv_obj, essential)
    out = {}
    for sk in missing:
        recs = recommend_for_skill(sk, catalog_df, topk=k_per_skill)
        out[sk] = recs
    return out


def explain_row(skill: str, row) -> str:
    if skill.lower() in row["text"]:
        return f"mentions “{skill}” directly"
    return "high semantic similarity to skill"


if __name__ == "__main__":
    missing_skills, present_skills = skill_gaps(cv, essential_skills)
    print("Present skills:", present_skills)
    print("Missing skills:", missing_skills)

    recs_by_skill = recommend_courses(cv, essential_skills, catalog, k_per_skill=3)

    print("\n=== Course Recommendations by Missing Skill ===")
    for skill, df in recs_by_skill.items():
        if df.empty:
            print(f"\n[ {skill} ] → No courses found in catalog.")
            continue
        print(f"\n[ {skill} ]")
        for _, r in df.iterrows():
            print(f"- {r['title']} ({r['provider']}, {r['hours']}h)  | score≈{r['score']:.2f}  | why: {explain_row(skill, r)}")

    rows = []
    for skill, df in recs_by_skill.items():
        for _, r in df.iterrows():
            rows.append({
                "missing_skill": skill,
                "course_id": r["id"],
                "title": r["title"],
                "provider": r["provider"],
                "hours": r["hours"],
                "level": r["level"],
                "score": round(float(r["score"]), 3),
                "why": explain_row(skill, r)
            })
    merged = pd.DataFrame(rows)
    merged if len(merged) else pd.DataFrame([{"info":"No recommendations; catalog empty or no missing skills."}])

    if 'merged' in globals() and len(merged):
        out_csv = "course_recs.csv"
        merged.to_csv(out_csv, index=False)
        print("Saved:", out_csv)
    else:
        print("No merged results to export.")
