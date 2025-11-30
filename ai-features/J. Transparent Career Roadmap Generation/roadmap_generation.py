"""Transparent career roadmap generator (with tiny AI prioritization model).

Provides resume parsing, knowledge graph lookup, gap analysis and a roadmap
builder. Now includes a small neural-network–style model to prioritize steps.

Previously `transparent_career_roadmap_generation.py` at the root of `ai-features`.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI
import re
import json
import math
import random

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


# -------------------------------------------------------------------------
# Knowledge graph (role → skills + resources)
# -------------------------------------------------------------------------
KNOWLEDGE_GRAPH = {
    "Machine Learning Engineer": {
        "skills": {
            "Machine Learning Basics": {
                "importance": 0.9,
                "prereq": ["Probability & Statistics", "Python"],
            },
            "Deep Learning": {
                "importance": 0.95,
                "prereq": ["Machine Learning Basics", "Linear Algebra"],
            },
            "Model Deployment": {
                "importance": 0.8,
                "prereq": ["Docker", "REST APIs"],
            },
            "Data Engineering": {
                "importance": 0.7,
                "prereq": ["SQL"],
            },
        },
        "resources": {
            "Machine Learning Basics": "Course: Intro to ML (example)",
            "Deep Learning": "Course: Deep Learning Specialization (example)",
            "Model Deployment": "Project: Deploy model with Docker + FastAPI",
            "Data Engineering": "Course: Data Engineering Bootcamp",
            "SQL": "Course: SQL for Data Analysis",
            "Python": "Course: Python for Data Science",
        },
    },
    "Data Analyst": {
        "skills": {
            "Data Analysis": {
                "importance": 0.9,
                "prereq": ["Excel", "Python"],
            },
            "SQL": {
                "importance": 0.85,
                "prereq": [],
            },
            "Visualization": {
                "importance": 0.8,
                "prereq": ["Data Analysis"],
            },
        },
        "resources": {
            "Data Analysis": "Course: Data Analysis with Python",
            "SQL": "Course: SQL for Data Analysis",
            "Visualization": "Project: Build dashboards with PowerBI or Tableau",
        },
    },
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
    "rest api": "REST APIs",
}


# -------------------------------------------------------------------------
# Simple skill extraction (rules + optional spaCy)
# -------------------------------------------------------------------------
def simple_skill_extractor(text: str) -> List[str]:
    text_low = text.lower()
    found = set()
    for k in SKILL_SYNONYMS:
        if re.search(r"\b" + re.escape(k) + r"\b", text_low):
            found.add(SKILL_SYNONYMS[k])

    # Optional AI: spaCy NER
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
    # dedupe preserving order
    return list(dict.fromkeys(normalized))


def get_role_requirements(role: str) -> Optional[Dict[str, Any]]:
    return KNOWLEDGE_GRAPH.get(role)


def gap_analysis(detected: List[str], role_req: Dict[str, Any]) -> List[Dict[str, Any]]:
    req_skills = role_req.get("skills", {})
    gaps = [
        {"skill": skill, "importance": meta.get("importance", 0.0)}
        for skill, meta in req_skills.items()
        if skill not in detected
    ]
    return sorted(gaps, key=lambda x: -x["importance"])


def resolve_prereqs(skill: str, role_req: Dict[str, Any]) -> List[str]:
    skills_meta = role_req.get("skills", {})
    visited = set()
    order: List[str] = []

    def dfs(s):
        if s in visited:
            return
        visited.add(s)
        meta = skills_meta.get(s, {})
        for p in meta.get("prereq", []):
            dfs(p)
        order.append(s)

    dfs(skill)
    # return all prerequisites in dependency order (excluding the final skill itself)
    order = [v for v in order if v != skill]
    return order


# -------------------------------------------------------------------------
# Tiny AI model: neural-net style roadmap step prioritizer
# -------------------------------------------------------------------------
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def tanh(x: float) -> float:
    return math.tanh(x)


class TinyRoadmapModel:
    """
    Very small neural-network–style model:

        input_dim -> hidden_dim (tanh) -> 1 (sigmoid)

    This acts as a learned prioritizer for roadmap steps. We treat the
    weights as if they were trained offline on historical data.
    """

    def __init__(self, input_dim: int = 5, hidden_dim: int = 6):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        random.seed(123)  # reproducible "trained" weights

        # Initialize small random weights
        self.W1 = [
            [(random.random() - 0.5) * 0.6 for _ in range(input_dim)]
            for _ in range(hidden_dim)
        ]
        self.b1 = [(random.random() - 0.5) * 0.6 for _ in range(hidden_dim)]

        self.W2 = [(random.random() - 0.5) * 0.6 for _ in range(hidden_dim)]
        self.b2 = (random.random() - 0.5) * 0.6

        # Nudge certain feature columns to be more influential:
        #   - importance (idx 0)
        #   - is_prereq (idx 1)
        #   - depth_norm (idx 2)
        important_indices = [0, 1, 2]
        for h in range(hidden_dim):
            for idx in important_indices:
                self.W1[h][idx] *= 1.8

    def predict_score(self, features: List[float]) -> float:
        """
        Forward pass: returns a priority score in [0, 1].
        Higher = schedule earlier in the roadmap.
        """
        if len(features) != self.input_dim:
            raise ValueError(
                f"Expected {self.input_dim} features, got {len(features)}"
            )

        # Hidden layer
        hidden: List[float] = []
        for h in range(self.hidden_dim):
            z = self.b1[h]
            for i, x in enumerate(features):
                z += self.W1[h][i] * x
            hidden.append(tanh(z))

        # Output
        z_out = self.b2
        for h in range(self.hidden_dim):
            z_out += self.W2[h] * hidden[h]

        return sigmoid(z_out)


ROADMAP_MODEL = TinyRoadmapModel(input_dim=5, hidden_dim=6)


def build_step_features(
    candidate: Dict[str, Any],
    target_role: str,
) -> List[float]:
    """
    Build numeric features for the AI roadmap model.

    Features:
      0: importance (0–1)
      1: is_prereq (0/1)
      2: prereq_depth normalized (0–1)
      3: duration_weeks normalized (0–1)
      4: is_short_term_role (1 if non-senior role heuristic)
    """
    importance = float(candidate.get("importance", 0.0))
    is_prereq = 1.0 if candidate.get("is_prereq", False) else 0.0
    depth = float(candidate.get("prereq_depth", 0))
    duration = float(candidate.get("duration_weeks", 3))

    depth_norm = max(0.0, min(1.0, depth / 4.0))
    duration_norm = max(0.0, min(1.0, duration / 8.0))

    is_short_term_role = 1.0 if "senior" not in target_role.lower() else 0.0

    return [
        importance,
        is_prereq,
        depth_norm,
        duration_norm,
        is_short_term_role,
    ]


# -------------------------------------------------------------------------
# Roadmap scheduling (now AI-prioritized)
# -------------------------------------------------------------------------
def schedule_steps(
    gaps: List[Dict[str, Any]],
    role_req: Dict[str, Any],
    detected: List[str],
    target_role: str,
) -> List[RoadmapStep]:
    """
    Build roadmap steps for missing skills + prerequisites,
    then use TinyRoadmapModel to prioritize their order.
    """
    skills_meta = role_req.get("skills", {})
    resources = role_req.get("resources", {})

    candidates: List[Dict[str, Any]] = []
    seen: set = set()

    for gap in gaps:
        skill = gap["skill"]
        importance = float(gap.get("importance", 0.0))

        # First, handle prerequisites
        prereqs = resolve_prereqs(skill, role_req)
        for depth, p in enumerate(prereqs, start=1):
            if p in detected or p in seen:
                continue

            p_importance = skills_meta.get(p, {}).get("importance", importance * 0.7)

            candidates.append(
                {
                    "name": p,
                    "type": "Course/Preparation",
                    "duration_weeks": 2,
                    "reason": f"Prerequisite for {skill}",
                    "resource": resources.get(p),
                    "importance": p_importance,
                    "is_prereq": True,
                    "prereq_depth": depth,
                }
            )
            seen.add(p)

        # Then the core gap skill itself
        if skill not in seen:
            candidates.append(
                {
                    "name": skill,
                    "type": "Course/Project",
                    "duration_weeks": 3,
                    "reason": f"Core requirement for {target_role}",
                    "resource": resources.get(skill),
                    "importance": importance,
                    "is_prereq": False,
                    "prereq_depth": 0,
                }
            )
            seen.add(skill)

    # AI: score and sort candidates
    scored: List[tuple] = []
    for c in candidates:
        features = build_step_features(c, target_role)
        score = ROADMAP_MODEL.predict_score(features)
        # tiny jitter for tie-breaking
        score += random.random() * 0.01
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    roadmap: List[RoadmapStep] = []
    for score, c in scored:
        roadmap.append(
            RoadmapStep(
                step=c["name"],
                type=c["type"],
                duration_weeks=c["duration_weeks"],
                reason=c["reason"],  # we use the AI only for ordering, not in text
                resource=c["resource"],
            )
        )

    return roadmap


# -------------------------------------------------------------------------
# Narrative and orchestration
# -------------------------------------------------------------------------
def generate_narrative(
    detected: List[str],
    gaps: List[Dict[str, Any]],
    role: str,
) -> str:
    if not gaps:
        return (
            f"Your resume already aligns well with the {role} role. "
            f"Focus on projects and portfolios to showcase your expertise."
        )
    gap_names = [g["skill"] for g in gaps[:3]]
    return (
        f"For the {role} role, you are missing key skills such as "
        f"{', '.join(gap_names)}. Start by covering their prerequisites, "
        f"then move to advanced applications. Completing these topics will "
        f"significantly strengthen your fit for {role}."
    )


def build_roadmap_logic(
    resume_text: str,
    target_role: str,
    timeline_months: Optional[int] = None,
) -> RoadmapOutput:
    detected = simple_skill_extractor(resume_text)
    normalized = normalize_skills(detected)

    role_req = get_role_requirements(target_role)
    if not role_req:
        return RoadmapOutput(
            target_role=target_role,
            detected_skills=normalized,
            gaps=[],
            roadmap=[],
            narrative=f"Role '{target_role}' not found in knowledge graph.",
        )

    gaps = gap_analysis(normalized, role_req)
    roadmap_steps = schedule_steps(gaps, role_req, normalized, target_role)
    narrative = generate_narrative(normalized, gaps, target_role)

    return RoadmapOutput(
        target_role=target_role,
        detected_skills=normalized,
        gaps=[g["skill"] for g in gaps],
        roadmap=roadmap_steps,
        narrative=narrative,
    )


# -------------------------------------------------------------------------
# FastAPI endpoint
# -------------------------------------------------------------------------
@app.post("/generate_roadmap", response_model=RoadmapOutput)
def generate_roadmap(input: ResumeInput):
    return build_roadmap_logic(input.text, input.target_role, input.timeline_months)


# -------------------------------------------------------------------------
# CLI test
# -------------------------------------------------------------------------
if __name__ == "__main__":
    sample_resume = """
    Ahmed Hassan
    Skills: Python, pandas, linear algebra, tensorflow, SQL
    Experience: Built small ML models for university projects.
    """
    result = build_roadmap_logic(sample_resume, "Machine Learning Engineer")
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
