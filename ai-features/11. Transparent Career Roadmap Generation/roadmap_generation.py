"""Transparent career roadmap generator (moved and renamed).

Provides resume parsing, knowledge graph lookup, gap analysis and a small
roadmap builder. Previously `transparent_career_roadmap_generation.py` at the
root of `ai-features`.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI
import re
import json

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

app = FastAPI(title="Transparent Career Roadmap API")

class ResumeInput(BaseModel):
    text: str
    target_role: str
    timeline_months: Optional[int] = None


class RoadmapStep(BaseModel):
    step: str
    type: str
    duration_weeks: int
    reason: str
    resource: Optional[str] = None


class RoadmapOutput(BaseModel):
    target_role: str
    detected_skills: List[str]
    gaps: List[str]
    roadmap: List[RoadmapStep]
    narrative: str

KNOWLEDGE_GRAPH = {
    "Machine Learning Engineer": {
        "skills": {
            "Machine Learning Basics": {"importance": 0.9, "prereq": ["Probability & Statistics", "Python"]},
            "Deep Learning": {"importance": 0.95, "prereq": ["Machine Learning Basics", "Linear Algebra"]},
            "Model Deployment": {"importance": 0.8, "prereq": ["Docker", "REST APIs"]},
            "Data Engineering": {"importance": 0.7, "prereq": ["SQL"]}
        },
        "resources": {
            "Machine Learning Basics": "Course: Intro to ML (example)",
            "Deep Learning": "Course: Deep Learning Specialization (example)",
            "Model Deployment": "Project: Deploy model with Docker + FastAPI",
            "Data Engineering": "Course: Data Engineering Bootcamp",
            "SQL": "Course: SQL for Data Analysis",
            "Python": "Course: Python for Data Science",
        }
    },
    "Data Analyst": {
        "skills": {
            "Data Analysis": {"importance": 0.9, "prereq": ["Excel", "Python"]},
            "SQL": {"importance": 0.85, "prereq": []},
            "Visualization": {"importance": 0.8, "prereq": ["Data Analysis"]}
        },
        "resources": {
            "Data Analysis": "Course: Data Analysis with Python",
            "SQL": "Course: SQL for Data Analysis",
            "Visualization": "Project: Build dashboards with PowerBI or Tableau"
        }
    }
}

SKILL_SYNONYMS = {
    "ml": "Machine Learning Basics",
    "machine learning": "Machine Learning Basics",
    "deep learning": "Deep Learning",
    "tensorflow": "Deep Learning",
    "pytorch": "Deep Learning",
    "deploy": "Model Deployment",
    "deployment": "Model Deployment",
    "data analysis": "Data Analysis",
    "sql": "SQL",
    "excel": "Excel",
    "visualization": "Visualization",
    "python": "Python",
    "linear algebra": "Linear Algebra",
    "probability": "Probability & Statistics",
    "statistics": "Probability & Statistics",
    "docker": "Docker",
    "rest": "REST APIs",
    "rest api": "REST APIs"
}


def simple_skill_extractor(text: str) -> List[str]:
    text_low = text.lower()
    found = set()
    for k in SKILL_SYNONYMS:
        if re.search(r"\b" + re.escape(k) + r"\b", text_low):
            found.add(SKILL_SYNONYMS[k])
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            token = ent.text.lower().strip()
            if token in SKILL_SYNONYMS:
                found.add(SKILL_SYNONYMS[token])
    return sorted(found)


def normalize_skills(skills: List[str]) -> List[str]:
    normalized = []
    for s in skills:
        key = s.lower()
        normalized.append(SKILL_SYNONYMS.get(key, s))
    return list(dict.fromkeys(normalized))


def get_role_requirements(role: str) -> Optional[Dict[str, Any]]:
    return KNOWLEDGE_GRAPH.get(role)


def gap_analysis(detected: List[str], role_req: Dict[str, Any]) -> List[Dict[str, Any]]:
    req_skills = role_req.get("skills", {})
    gaps = [{"skill": skill, "importance": meta.get("importance", 0)} for skill, meta in req_skills.items() if skill not in detected]
    return sorted(gaps, key=lambda x: -x["importance"])


def resolve_prereqs(skill: str, role_req: Dict[str, Any]) -> List[str]:
    skills_meta = role_req.get("skills", {})
    visited = set()
    order = []
    def dfs(s):
        if s in visited:
            return
        visited.add(s)
        meta = skills_meta.get(s, {})
        for p in meta.get("prereq", []):
            dfs(p)
        order.append(s)
    dfs(skill)
    order = [v for v in order if v != skill]
    return order


def schedule_steps(gaps: List[Dict[str, Any]], role_req: Dict[str, Any], detected: List[str]) -> List[RoadmapStep]:
    roadmap = []
    seen = set()
    for gap in gaps:
        skill = gap["skill"]
        prereqs = resolve_prereqs(skill, role_req)
        for p in prereqs:
            if p not in detected and p not in seen:
                roadmap.append(RoadmapStep(step=p, type="Course/Preparation", duration_weeks=2, reason=f"Prerequisite for {skill}", resource=role_req.get("resources", {}).get(p)))
                seen.add(p)
        if skill not in seen:
            roadmap.append(RoadmapStep(step=skill, type="Course/Project", duration_weeks=3, reason=f"Core requirement for {role_req}", resource=role_req.get("resources", {}).get(skill)))
            seen.add(skill)
    return roadmap


def generate_narrative(detected: List[str], gaps: List[Dict[str, Any]], role: str) -> str:
    if not gaps:
        return f"Your resume already aligns well with the {role} role. Focus on projects and portfolios to showcase your expertise."
    gap_names = [g['skill'] for g in gaps[:3]]
    return f"For the {role} role, you are missing key skills such as {', '.join(gap_names)}. Start by covering their prerequisites, then move to advanced applications. Completing these topics will significantly strengthen your fit for {role}."


def build_roadmap_logic(resume_text: str, target_role: str, timeline_months: Optional[int] = None) -> RoadmapOutput:
    detected = simple_skill_extractor(resume_text)
    normalized = normalize_skills(detected)
    role_req = get_role_requirements(target_role)
    if not role_req:
        return RoadmapOutput(target_role=target_role, detected_skills=normalized, gaps=[], roadmap=[], narrative=f"Role '{target_role}' not found in knowledge graph.")
    gaps = gap_analysis(normalized, role_req)
    roadmap_steps = schedule_steps(gaps, role_req, normalized)
    narrative = generate_narrative(normalized, gaps, target_role)
    return RoadmapOutput(target_role=target_role, detected_skills=normalized, gaps=[g["skill"] for g in gaps], roadmap=roadmap_steps, narrative=narrative)


@app.post("/generate_roadmap", response_model=RoadmapOutput)
def generate_roadmap(input: ResumeInput):
    return build_roadmap_logic(input.text, input.target_role, input.timeline_months)


if __name__ == "__main__":
    sample_resume = """
    Ahmed Hassan
    Skills: Python, pandas, linear algebra, tensorflow, SQL
    Experience: Built small ML models for university projects.
    """
    result = build_roadmap_logic(sample_resume, "Machine Learning Engineer")
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
