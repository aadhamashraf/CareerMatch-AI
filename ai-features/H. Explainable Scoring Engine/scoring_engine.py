# -*- coding: utf-8 -*-
"""Explainable Scoring Engine — moved into numbered directory.

Provides scoring helpers (strength, relevance, completeness) and explainers.
"""

import json, re
from typing import List, Dict, Tuple
import pandas as pd
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

def infer_essential_skills(title: str):
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
    if cv_obj.get("summary"): parts.append(str(cv_obj["summary"]))

    sk = cv_obj.get("skills")
    if isinstance(sk, dict):
        for v in sk.values():
            if isinstance(v, list): parts.append(" ".join(map(str, v)))
            elif isinstance(v, str): parts.append(v)
    elif isinstance(sk, list):
        parts.append(" ".join(map(str, sk)))

    for p in cv_obj.get("projects", []) or []:
        if isinstance(p, dict):
            if p.get("name"): parts.append(str(p["name"]))
            if p.get("description"): parts.append(str(p["description"]))
            if p.get("tech"):
                parts.append(" ".join(map(str, p["tech"])) if isinstance(p["tech"], list) else str(p["tech"]))
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
    for s in re.split(r"[,\s/()\-]+", text):
        if s: tokens.add(normalize_token(s))
    return tokens


def completeness_score(cv_obj: Dict, essential_skills):
    req = [normalize_token(s) for s in (essential_skills or [])]
    if not req: return 0.0
    have = collect_skill_tokens(cv_obj)
    present = sum(1 for s in req if s in have)
    return (present / len(req)) * 100.0


def relevance_score(cv_obj: Dict, job_text: str) -> float:
    cv_text = cv_to_text(cv_obj).strip()
    job_text = (job_text or "").strip()
    if not cv_text or not job_text: return 0.0
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=1)
    X = vec.fit_transform([cv_text, job_text])
    return float(cosine_similarity(X[0], X[1])[0][0] * 100.0)


def presence_score_any(cv_obj: Dict, key: str) -> float:
    val = cv_obj.get(key)
    if not val: return 0.0
    if isinstance(val, (list, dict)): return 1.0 if len(val) > 0 else 0.0
    return 1.0


def education_proxy(cv_obj: Dict) -> float:
    if presence_score_any(cv_obj, "education") > 0: return 1.0
    summary = cv_obj.get("summary", "") or ""
    return 0.7 if re.search(r"\b(bachelor|undergraduate|bsc|bs|ba|msc|master|phd)\b", summary.lower()) else 0.0


def experience_proxy(cv_obj: Dict) -> float:
    return presence_score_any(cv_obj, "experience")


def projects_proxy(cv_obj: Dict) -> float:
    projects = cv_obj.get("projects", []) or []
    return min(1.0, (len(projects) if isinstance(projects, list) else 1) / 5.0)


def skills_proxy(cv_obj: Dict, essential_skills) -> float:
    return completeness_score(cv_obj, essential_skills) / 100.0


def certifications_proxy(cv_obj: Dict) -> float:
    return presence_score_any(cv_obj, "certifications")


def strength_score(cv_obj: Dict, essential_skills, weights: Dict[str, float]) -> Dict[str, float]:
    Edu  = education_proxy(cv_obj)
    Exp  = experience_proxy(cv_obj)
    Proj = projects_proxy(cv_obj)
    Skills = skills_proxy(cv_obj, essential_skills)
    Cert = certifications_proxy(cv_obj)
    wsum = sum(weights.values()) or 1.0
    w = {k: v/wsum for k, v in weights.items()}
    S = 100.0 * (w["Edu"]*Edu + w["Exp"]*Exp + w["Proj"]*Proj + w["Skills"]*Skills + w["Cert"]*Cert)
    return {"S": float(S), "Edu": float(Edu), "Exp": float(Exp), "Proj": float(Proj), "Skills": float(Skills), "Cert": float(Cert)}


def make_explanation(scores: Dict[str,float], subs: Dict[str,float], cv_obj: Dict, essentials, job_title: str):
    missing = find_missing_skills(cv_obj, essentials)
    summary = (
        f"Overall readiness for **{job_title}** looks **{pct_band(scores['Strength_S'])}** "
        f"(Strength {scores['Strength_S']} / 100). "
        f"Semantic **Relevance** is {pct_band(scores['Relevance_R'])} ({scores['Relevance_R']} / 100). "
        f"**Completeness** across essential skills is {pct_band(scores['Completeness_C'])} "
        f"({scores['Completeness_C']} / 100)."
    )
    bullets = [subscore_comment(k, v) for k, v in subs.items()]
    if missing:
        next_steps = ("To improve quickly, focus on the missing essentials: " + ", ".join(missing[:8]) + ". Add a short project or course for each one.")
    else:
        next_steps = "Great coverage of essentials. Deepen with advanced projects and deployment evidence."
    weakest = sorted(subs.items(), key=lambda x: x[1])[:2]
    targeted = [f"Boost **{k}** by: " + (
        "adding 1–2 professional experience bullets with measurable impact." if k=="Experience" else
        "publishing a recent repo with clear README, results, and links." if k=="Projects" else
        "explicitly listing the skill and referencing where you used it." if k=="Skills" else
        "adding degree details or relevant coursework." if k=="Education" else
        "adding a targeted certificate (e.g., AWS, TensorFlow)."
    ) for k,_ in weakest]
    return {"summary": summary, "why_strength": bullets, "next_steps": [next_steps] + targeted}


def pct_band(x: float):
    if x >= 85: return "excellent"
    if x >= 70: return "strong"
    if x >= 50: return "okay"
    if x >= 30: return "needs improvement"
    return "low"


def subscore_comment(name: str, v: float) -> str:
    tips = {
        "Education": "Add formal education details or list relevant coursework.",
        "Experience": "Add professional experience bullets with impact (metrics, ownership).",
        "Projects": "Show 2–3 recent, role-aligned projects with short outcomes.",
        "Skills": "Add missing essential skills explicitly in Skills or project bullets.",
        "Certifications": "If applicable, add relevant certificates or badges."
    }
    level = "high" if v >= 0.8 else ("moderate" if v >= 0.5 else "low")
    tip = tips.get(name, "Improve this area with concrete evidence.")
    return f"{name}: {level}. {tip}"


def find_missing_skills(cv_obj: Dict, essentials):
    req = [normalize_token(s) for s in (essentials or [])]
    have = collect_skill_tokens(cv_obj)
    return [s for s in essentials if normalize_token(s) not in have]
