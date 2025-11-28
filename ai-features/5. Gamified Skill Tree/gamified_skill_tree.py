# -*- coding: utf-8 -*-
"""Gamified skill tree — moved into numbered directory and renamed.

This is a cleaned copy of the original notebook/script that defined the
skill graph, user state, and role-aware recommendations.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAS_VIZ = True
except Exception:
    HAS_VIZ = False


@dataclass
class SkillNode:
    skill_id: str
    name: str
    required_xp: int
    depends_on: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)


SKILL_DEFS: Dict[str, SkillNode] = {
    "python": SkillNode(skill_id="python", name="Python Programming", required_xp=100, depends_on=[], roles=["data_scientist", "ml_engineer", "backend"]),
    "pandas": SkillNode(skill_id="pandas", name="Pandas for Data Analysis", required_xp=80, depends_on=["python"], roles=["data_scientist", "data_analyst"]),
    "ml_fundamentals": SkillNode(skill_id="ml_fundamentals", name="ML Fundamentals", required_xp=100, depends_on=["python"], roles=["data_scientist", "ml_engineer"]),
    "model_deployment": SkillNode(skill_id="model_deployment", name="Model Deployment", required_xp=80, depends_on=["ml_fundamentals"], roles=["ml_engineer"]),
    "sql": SkillNode(skill_id="sql", name="SQL for Data", required_xp=100, depends_on=[], roles=["data_analyst", "data_scientist"]),
    "data_viz": SkillNode(skill_id="data_viz", name="Data Visualization", required_xp=80, depends_on=["pandas"], roles=["data_analyst", "data_scientist"]),
}


@dataclass
class UserSkillState:
    current_xp: int = 0
    status: str = "locked"


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


def recommend_next_skills(user_state: Dict[str, UserSkillState], target_role: str, top_k: int = 3):
    candidates = []
    for sid, node in SKILL_DEFS.items():
        state = user_state[sid]
        if target_role not in node.roles:
            continue
        if state.status not in ("unlocked", "in_progress"):
            continue
        gap = node.required_xp - state.current_xp
        if gap <= 0:
            continue
        candidates.append((gap, sid))
    candidates.sort(reverse=True)
    return [sid for _, sid in candidates[:top_k]]


if __name__ == "__main__":
    sample_cv_features = {"python": {"years_experience": 1, "num_projects": 2, "has_cert": False}, "pandas": {"years_experience": 0.5, "num_projects": 1, "has_cert": False}, "sql": {"years_experience": 0, "num_projects": 0, "has_cert": False}}
    user_state = build_user_state_from_cv(sample_cv_features)
    update_statuses(user_state)
    target_role = "data_scientist"
    next_skills = recommend_next_skills(user_state, target_role)
    print("Recommended next skills:", next_skills)
