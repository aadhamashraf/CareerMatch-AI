"""Adaptive Recommendation (skill-tree + adaptive recommendations)

This file is a moved and renamed copy of the original
`adaptive_recommendation_system.py` to fit into the numbered-directory layout.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import sys

# Optional: for visualization later
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False
    print("Visualization libs not installed. Run `pip install networkx` if needed.")


@dataclass
class SkillNode:
    skill_id: str
    name: str
    required_xp: int
    depends_on: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)


SKILL_DEFS: Dict[str, SkillNode] = {
    "python": SkillNode(
        skill_id="python", name="Python Programming", required_xp=100,
        depends_on=[], roles=["data_scientist", "ml_engineer", "backend"]
    ),
    "pandas": SkillNode(
        skill_id="pandas", name="Pandas for Data Analysis", required_xp=80,
        depends_on=["python"], roles=["data_scientist", "data_analyst"]
    ),
    "ml_fundamentals": SkillNode(
        skill_id="ml_fundamentals", name="ML Fundamentals", required_xp=100,
        depends_on=["python"], roles=["data_scientist", "ml_engineer"]
    ),
    "model_deployment": SkillNode(
        skill_id="model_deployment", name="Model Deployment", required_xp=80,
        depends_on=["ml_fundamentals"], roles=["ml_engineer"]
    ),
    "sql": SkillNode(
        skill_id="sql", name="SQL for Data", required_xp=100,
        depends_on=[], roles=["data_analyst", "data_scientist"]
    ),
    "data_viz": SkillNode(
        skill_id="data_viz", name="Data Visualization", required_xp=80,
        depends_on=["pandas"], roles=["data_analyst", "data_scientist"]
    ),
}


@dataclass
class ContentItem:
    content_id: str
    title: str
    type: str
    skill_id: str
    xp_level: str


CONTENT_DB: Dict[str, ContentItem] = {
    "C101": ContentItem(
        content_id="C101", title="Python for Beginners Course",
        type="course", skill_id="python", xp_level="beginner"
    ),
    "C102": ContentItem(
        content_id="C102", title="Intro to Pandas Course",
        type="course", skill_id="pandas", xp_level="beginner"
    ),
    "P101": ContentItem(
        content_id="P101", title="Pandas Sales Data Analysis Project",
        type="project", skill_id="pandas", xp_level="advanced"
    ),
    "C103": ContentItem(
        content_id="C103", title="SQL Fundamentals Course",
        type="course", skill_id="sql", xp_level="beginner"
    ),
    "C201": ContentItem(
        content_id="C201", title="Machine Learning A-Z Course",
        type="course", skill_id="ml_fundamentals", xp_level="beginner"
    ),
    "P201": ContentItem(
        content_id="P201", title="Titanic Survivor Prediction Project",
        type="project", skill_id="ml_fundamentals", xp_level="advanced"
    ),
}


@dataclass
class UserSkillState:
    current_xp: int = 0
    status: str = "locked"


sample_cv_features = {
    "python": {"years_experience": 1, "num_projects": 2, "has_cert": False},
    "pandas": {"years_experience": 0.5, "num_projects": 1, "has_cert": False},
    "sql": {"years_experience": 0, "num_projects": 0, "has_cert": False},
}


def compute_initial_xp_for_skill(skill_id: str, cv_features: Dict) -> int:
    feat = cv_features.get(skill_id)
    if not feat:
        return 0
    years = feat.get("years_experience", 0)
    projects = feat.get("num_projects", 0)
    has_cert = feat.get("has_cert", False)
    xp = 0
    xp += min(50, years * 20)
    xp += min(30, projects * 10)
    xp += 20 if has_cert else 0
    required = SKILL_DEFS[skill_id].required_xp
    return int(min(xp, required))


def build_user_state_from_cv(cv_features: Dict[str, Dict]) -> Dict[str, UserSkillState]:
    user_state: Dict[str, UserSkillState] = {}
    for sid, node in SKILL_DEFS.items():
        xp = compute_initial_xp_for_skill(sid, cv_features)
        user_state[sid] = UserSkillState(current_xp=xp)
    return user_state


def is_unlocked(skill_id: str, user_state: Dict[str, UserSkillState]) -> bool:
    node = SKILL_DEFS[skill_id]
    if not node.depends_on:
        return True
    for dep_id in node.depends_on:
        dep_node = SKILL_DEFS[dep_id]
        dep_state = user_state.get(dep_id, UserSkillState())
        threshold = 0.7 * dep_node.required_xp
        if dep_state.current_xp < threshold:
            return False
    return True


def update_statuses(user_state: Dict[str, UserSkillState]) -> None:
    for sid, node in SKILL_DEFS.items():
        state = user_state[sid]
        if state.current_xp >= node.required_xp:
            state.status = "completed"
        elif is_unlocked(sid, user_state):
            state.status = "in_progress" if state.current_xp > 0 else "unlocked"
        else:
            state.status = "locked"


PRACTICE_THRESHOLD_PERCENT = 0.3


def find_content_for_skill(skill_id: str, xp_level: str) -> Optional[ContentItem]:
    for item in CONTENT_DB.values():
        if item.skill_id == skill_id and item.xp_level == xp_level:
            return item
    return None


def get_adaptive_recommendations(user_state: Dict[str, UserSkillState], target_role: str, top_k: int = 3) -> List[ContentItem]:
    recommendations = []
    for sid, node in SKILL_DEFS.items():
        state = user_state[sid]
        if target_role not in node.roles:
            continue
        if state.status not in ("unlocked", "in_progress"):
            continue
        practice_threshold_xp = node.required_xp * PRACTICE_THRESHOLD_PERCENT
        content_item = None
        if state.current_xp < practice_threshold_xp:
            content_item = find_content_for_skill(sid, xp_level="beginner")
        else:
            content_item = find_content_for_skill(sid, xp_level="advanced")
        if content_item:
            recommendations.append(content_item)
    return recommendations[:top_k]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    user_state = build_user_state_from_cv(sample_cv_features)
    update_statuses(user_state)
    print("--- User Skill Status (Feature 18) ---")
    for sid, state in user_state.items():
        print(f"{sid:18} XP={state.current_xp:3} / {SKILL_DEFS[sid].required_xp:3}  → {state.status}")
    print("-" * 40)
    target_role = "data_scientist"
    next_actions = get_adaptive_recommendations(user_state, target_role)
    print(f"--- Adaptive Recommendations (Feature 14) ---")
    print(f"Target role: {target_role}")
    if not next_actions:
        print("No specific recommendations found. Keep exploring!")
    else:
        print("Here are your next steps:")
        for item in next_actions:
            print(f"- To improve '{item.skill_id}', we recommend this {item.type}:")
            print(f"  -> {item.title} (ID: {item.content_id})")
