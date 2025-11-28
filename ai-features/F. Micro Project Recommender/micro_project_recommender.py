"""Micro-project recommender (moved into numbered directory)

This was migrated from copy_of_micro_project_recommender.py into a
dedicated directory and renamed to `micro_project_recommender.py`.
"""

import json, re, math
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np

# Try to import SBERT; fall back to TF-IDF if not available
USE_EMB = True
try:
    from sentence_transformers import SentenceTransformer, util as sbert_util
    EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    print("Embeddings not available; falling back to TF-IDF only.", e)
    USE_EMB = False
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

# Colab upload helper
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

# default example job show
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

projects = [
    ("p1","Build a Sentiment Analyzer","Kaggle","https://www.kaggle.com/datasets","NLP,Python,Scikit-Learn","2",2,"Train a simple text classifier (LogReg/SVM) on tweets; evaluate F1; deploy minimal CLI."),
    ("p2","Image Classifier (Cats vs Dogs)","Kaggle","https://www.kaggle.com/competitions/dogs-vs-cats","Computer Vision,TensorFlow,PyTorch","3",3,"Fine-tune a small CNN on a subset; report accuracy; export model."),
    ("p3","Sales Forecasting (Time Series)","UCI","https://archive.ics.uci.edu/","Pandas,Time Series,ARIMA","3",3,"Model and forecast monthly sales; compare ARIMA vs Prophet; plot results."),
    ("p4","ETL + Dashboard (Pandas + Plotly)","GitHub","https://github.com/","Data Visualization,Pandas,Plotly,SQL","2",2,"Build an ETL script and a small dashboard; 2–3 KPIs with charts."),
    ("p5","ML API with FastAPI + Docker","GitHub","https://github.com/","FastAPI,Docker,Deployment,Scikit-Learn","3",4,"Wrap a trained model in FastAPI; dockerize; add README & tests."),
    ("p6","Recommendation Mini-System","Kaggle","https://www.kaggle.com/","Recommender Systems,Python,Matrix Factorization","4",4,"Implicit feedback MF on a public dataset; hit@k metric; simple report."),
    ("p7","SQL Analytics Challenge","Hackerrank","https://www.hackerrank.com/","SQL,Data Analysis","2",2,"Solve 10–15 SQL queries; document learnings and edge cases."),
    ("p8","NLP Topic Modeling","Kaggle","https://www.kaggle.com/","NLP,Python,Topic Modeling","2",3,"Apply LDA/NMF to news dataset; visualize topics; interpret results."),
    ("p9","MLOps Lite: CI/CD for a Model","GitHub","https://github.com/","MLOps,CI/CD,Docker,GitHub Actions","5",5,"Set up CI/CD pipeline to test & build a container; push to registry."),
    ("p10","AWS S3 + Lambda Data Pipeline","AWS","https://aws.amazon.com/","AWS,Serverless,Python","4",4,"Ingest files to S3; trigger Lambda; basic transform; cost estimate."),
]
proj_df = pd.DataFrame(projects, columns=["id","title","source","url","tags","days","difficulty","description"])
proj_df["days"] = proj_df["days"].astype(int)
proj_df = proj_df[(proj_df["days"] >= 2) & (proj_df["days"] <= 5)].reset_index(drop=True)
proj_df["text"] = (proj_df["title"] + " " + proj_df["tags"] + " " + proj_df["description"]).str.lower()

PREF_DIFFICULTY_MAX = None
PREF_TIME_BUDGET_DAYS = None

df = proj_df.copy()
if PREF_DIFFICULTY_MAX is not None:
    df = df[df["difficulty"] <= PREF_DIFFICULTY_MAX]
if PREF_TIME_BUDGET_DAYS is not None:
    df = df[df["days"] <= PREF_TIME_BUDGET_DAYS]
df = df.reset_index(drop=True)


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


def recommend_for_skill(skill: str, df: pd.DataFrame, topk=3, role_hint: str = "") -> pd.DataFrame:
    docs = df["text"].tolist()
    query = f"{skill} for {role_hint}" if role_hint else skill
    sims = semantic_scores(query, docs)
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


def recommend_projects(cv_obj: Dict, essential: List[str], project_df: pd.DataFrame, k_per_skill: int = 3, role_hint: str = "") -> Dict[str, pd.DataFrame]:
    missing, present = skill_gaps(cv_obj, essential)
    out = {}
    for sk in missing:
        recs = recommend_for_skill(sk, project_df, topk=k_per_skill, role_hint=role_hint)
        out[sk] = recs
    return out


def explain_row(skill: str, row) -> str:
    tokens = row["text"]
    if skill.lower() in tokens:
        return f"mentions “{skill}” directly"
    return "high semantic match to skill and tags"


if __name__ == "__main__":
    missing_skills, present_skills = skill_gaps(cv, essential_skills)
    print("Present skills:", present_skills)
    print("Missing skills:", missing_skills)

    recs_by_skill = recommend_projects(cv, essential_skills, df, k_per_skill=3, role_hint=job_title)

    print("\n=== Micro-Project Recommendations by Missing Skill ===")
    for skill, d in recs_by_skill.items():
        if d.empty:
            print(f"\n[ {skill} ] → No micro-projects found in catalog.")
            continue
        print(f"\n[ {skill} ]")
        for _, r in d.iterrows():
            print(f"- {r['title']} ({r['days']} days, diff {r['difficulty']})  | score≈{r['score']:.2f}  | src: {r['source']}  | why: {explain_row(skill, r)}")
            print(f"  link: {r['url']}")

    rows = []
    for skill, d in recs_by_skill.items():
        for _, r in d.iterrows():
            rows.append({
                "missing_skill": skill,
                "project_id": r["id"],
                "title": r["title"],
                "source": r["source"],
                "url": r["url"],
                "days": int(r["days"]),
                "difficulty": int(r["difficulty"]),
                "score": round(float(r["score"]), 3),
                "why": explain_row(skill, r)
            })
    merged = pd.DataFrame(rows)
    merged if len(merged) else pd.DataFrame([{"info":"No recommendations; catalog empty or no missing skills."}])

    if 'merged' in globals() and len(merged):
        out_csv = "micro_project_recs.csv"
        merged.to_csv(out_csv, index=False)
        print("Saved:", out_csv)
    else:
        print("No merged results to export.")
