# -*- coding: utf-8 -*-
"""
This file combines:
- Feature 18: Gamified Skill Tree Modeling
- Feature 14: Adaptive Learning Recommendation (Rule-Based MVP)
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

# -----------------------------------------------------------------
# FEATURE 18: Skill Tree Definition (Your existing code)
# -----------------------------------------------------------------

@dataclass
class SkillNode:
    skill_id: str
    name: str
    required_xp: int
    depends_on: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)

# ==== Define the Skill Tree ====
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

# -----------------------------------------------------------------
# ## FEATURE 14: Content Database (Simulating Features 10 & 11)
# -----------------------------------------------------------------
# We define the "content" (courses/projects) that our
# recommendation engine can suggest.

@dataclass
class ContentItem:
    content_id: str
    title: str
    # 'type' tells the engine if this is for learning (course) or practice (project)
    type: str  # "course" or "project"
    # 'skill_id' links this content to the Skill Tree
    skill_id: str
    # 'level' helps the engine match content to user's XP
    xp_level: str  # "beginner" (for low XP) or "advanced" (for high XP)

# ==== Define the Content Database ====
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

# -----------------------------------------------------------------
# FEATURE 18: User State & XP Computation (Your existing code)
# -----------------------------------------------------------------

@dataclass
class UserSkillState:
    current_xp: int = 0
    status: str = "locked"  # locked, unlocked, in_progress, completed

# Example: simulated CV evidence per skill
sample_cv_features = {
    "python": {
        "years_experience": 1, "num_projects": 2, "has_cert": False,
    },
    "pandas": {
        "years_experience": 0.5, "num_projects": 1, "has_cert": False,
    },
    "sql": {
        "years_experience": 0, "num_projects": 0, "has_cert": False,
    },
}

def compute_initial_xp_for_skill(skill_id: str, cv_features: Dict) -> int:
    """Compute XP for one skill from CV features."""
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
    """Create UserSkillState dict for all skills in SKILL_DEFS."""
    user_state: Dict[str, UserSkillState] = {}
    for sid, node in SKILL_DEFS.items():
        xp = compute_initial_xp_for_skill(sid, cv_features)
        user_state[sid] = UserSkillState(current_xp=xp)
    return user_state

def is_unlocked(skill_id: str, user_state: Dict[str, UserSkillState]) -> bool:
    """Check if a skill's dependencies are met."""
    node = SKILL_DEFS[skill_id]
    if not node.depends_on:
        return True  # root skills
    for dep_id in node.depends_on:
        dep_node = SKILL_DEFS[dep_id]
        dep_state = user_state.get(dep_id, UserSkillState())
        threshold = 0.7 * dep_node.required_xp
        if dep_state.current_xp < threshold:
            return False
    return True

def update_statuses(user_state: Dict[str, UserSkillState]) -> None:
    """Update all skill statuses based on XP and dependencies."""
    for sid, node in SKILL_DEFS.items():
        state = user_state[sid]
        if state.current_xp >= node.required_xp:
            state.status = "completed"
        elif is_unlocked(sid, user_state):
            state.status = "in_progress" if state.current_xp > 0 else "unlocked"
        else:
            state.status = "locked"

# -----------------------------------------------------------------
# ## FEATURE 14: Adaptive Recommendation Engine (Upgraded)
# -----------------------------------------------------------------

# This threshold determines when to switch from "learning" (course)
# to "practice" (project).
# 30% of required XP seems like a good starting point.
PRACTICE_THRESHOLD_PERCENT = 0.3

def find_content_for_skill(skill_id: str, xp_level: str) -> Optional[ContentItem]:
    """
    Searches the CONTENT_DB for a matching course or project.
    """
    for item in CONTENT_DB.values():
        if item.skill_id == skill_id and item.xp_level == xp_level:
            return item
    return None

def get_adaptive_recommendations(
    user_state: Dict[str, UserSkillState],
    target_role: str,
    top_k: int = 3,
) -> List[ContentItem]:
    """
    (Feature 14) This is the "brain".
    It recommends specific Courses or Projects based on the user's
    XP level in each unlocked skill.
    """
    recommendations = []
    
    # Iterate through all skills defined in the tree
    for sid, node in SKILL_DEFS.items():
        state = user_state[sid]
        
        # --- Rule 1: Is this skill relevant to the user's goal?
        if target_role not in node.roles:
            continue
            
        # --- Rule 2: Is the skill available to work on?
        if state.status not in ("unlocked", "in_progress"):
            continue

        # --- Rule 3 (Adaptive Logic): Does the user need to LEARN or PRACTICE?
        practice_threshold_xp = node.required_xp * PRACTICE_THRESHOLD_PERCENT
        
        content_item = None
        if state.current_xp < practice_threshold_xp:
            # User has low XP. They need to LEARN.
            # Find a "beginner" "course" for this skill.
            content_item = find_content_for_skill(sid, xp_level="beginner")
        else:
            # User has some XP. They need to PRACTICE.
            # Find an "advanced" "project" for this skill.
            content_item = find_content_for_skill(sid, xp_level="advanced")
            
        # --- Rule 4: If we found a matching piece of content, add it.
        if content_item:
            recommendations.append(content_item)

    # For now, we just return the first K matches.
    # A smarter engine might sort them by "XP gap" or other heuristics.
    return recommendations[:top_k]

# -----------------------------------------------------------------
# ## Test Execution
# -----------------------------------------------------------------

if __name__ == "__main__":
    # Force Python to use UTF-8 for printing
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 1. Build user state from CV (Feature 18)
    user_state = build_user_state_from_cv(sample_cv_features)
    
    # 2. Update statuses (Feature 18)
    update_statuses(user_state)

    print("--- User Skill Status (Feature 18) ---")
    for sid, state in user_state.items():
        print(f"{sid:18} XP={state.current_xp:3} / {SKILL_DEFS[sid].required_xp:3}  → {state.status}")
    print("-" * 40)
    
    # 3. Get adaptive recommendations (Feature 14)
    target_role = "data_scientist"
    next_actions = get_adaptive_recommendations(user_state, target_role)

    print(f"--- Adaptive Recommendations (Feature 14) ---")
    print(f"Target role: {target_role}")
    
    if not next_actions:
        print("No specific recommendations found. Keep exploring!")
    else:
        print("Here are your next steps:")
        for item in next_actions:
            # This is the adaptive part!
            # It suggests a COURSE for 'ml_fundamentals' (0 XP)
            # It suggests a PROJECT for 'pandas' (high XP)
            print(
                f"- To improve '{item.skill_id}', we recommend this {item.type}:")
            print(f"  -> {item.title} (ID: {item.content_id})")

    # 4. Optional Visualization (Feature 18)
    if HAS_VIZ:
        G = nx.DiGraph()
        for sid, node in SKILL_DEFS.items():
            state = user_state[sid]
            label = f"{sid}\n({state.status})"
            G.add_node(sid, label=label)
            for dep in node.depends_on:
                G.add_edge(dep, sid)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_size=2500, node_color="#cceeff",
                labels={n: G.nodes[n]['label'] for n in G.nodes()})
        plt.title("Skill Tree Status")
        plt.axis("off")
        plt.show()