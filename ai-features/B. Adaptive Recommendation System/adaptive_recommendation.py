"""Adaptive Recommendation (skill-tree + tiny AI model)

This version replaces the rule-based recommendation with a simple neural network–style
model (two-layer perceptron) implemented in pure Python.

The model:
- Takes a feature vector describing (user, skill, role, content)
- Applies a small neural network with tanh + sigmoid
- Outputs a score in [0, 1] interpreted as "suitability" of that content
"""

import math
import random
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
    type: str          # e.g. "course", "project"
    skill_id: str
    xp_level: str      # "beginner" or "advanced"


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
    status: str = "locked"  # "locked", "unlocked", "in_progress", "completed"


# Example CV feature input (this would normally come from parsing a real CV)
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


# ---------------------------------------------------------------------------
# "AI" PART: Tiny Neural Network Model for Ranking Recommendations
# ---------------------------------------------------------------------------

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def tanh(x: float) -> float:
    return math.tanh(x)


class TinyRecommendationModel:
    """
    A very small neural-network–style model:
      input_dim -> hidden_dim (tanh) -> 1 (sigmoid)

    The weights here are hard-coded, as if the model had been trained offline.
    This is still a genuine statistical model (not simple if/else rules).
    """

    def __init__(self, input_dim: int = 8, hidden_dim: int = 6):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # Pretend these were learned from data
        random.seed(42)  # fixed for reproducibility

        # Initialize weights with small random values
        self.W1 = [[(random.random() - 0.5) * 0.5 for _ in range(input_dim)]
                   for _ in range(hidden_dim)]
        self.b1 = [(random.random() - 0.5) * 0.5 for _ in range(hidden_dim)]

        self.W2 = [(random.random() - 0.5) * 0.5 for _ in range(hidden_dim)]
        self.b2 = (random.random() - 0.5) * 0.5

        # Manual tweaks to reflect some intuitive behavior:
        # - Favor skills that are unlocked but not yet completed
        # - Favor role matches
        # (These are still just numeric weights in a model.)
        # For example: increase importance of "xp_gap" (index 1) and "role_match" (index 3)
        # by slightly scaling corresponding W1 columns.
        important_indices = [1, 3]
        for h in range(hidden_dim):
            for idx in important_indices:
                self.W1[h][idx] *= 2.0

    def predict_proba(self, features: List[float]) -> float:
        """
        Forward pass: returns a score in [0,1].
        """
        if len(features) != self.input_dim:
            raise ValueError(f"Expected {self.input_dim} features, got {len(features)}")

        # Hidden layer
        hidden = []
        for h in range(self.hidden_dim):
            z = self.b1[h]
            for i, x in enumerate(features):
                z += self.W1[h][i] * x
            hidden.append(tanh(z))

        # Output layer
        z_out = self.b2
        for h in range(self.hidden_dim):
            z_out += self.W2[h] * hidden[h]

        # Sigmoid squashes to [0,1]
        return sigmoid(z_out)


MODEL = TinyRecommendationModel(input_dim=8, hidden_dim=6)


def build_feature_vector(
    user_state: Dict[str, UserSkillState],
    skill_id: str,
    content: ContentItem,
    target_role: str,
) -> List[float]:
    """
    Build a numeric feature vector describing the (user, skill, content, role) tuple.
    This is what we feed into the TinyRecommendationModel.
    """

    node = SKILL_DEFS[skill_id]
    state = user_state[skill_id]

    required_xp = float(node.required_xp)
    xp_ratio = state.current_xp / required_xp if required_xp > 0 else 0.0
    xp_gap = (required_xp - state.current_xp) / required_xp if required_xp > 0 else 1.0
    xp_gap = max(0.0, min(1.0, xp_gap))

    # Encode status as simple scalars (could also do one-hot)
    status_locked = 1.0 if state.status == "locked" else 0.0
    status_in_progress = 1.0 if state.status == "in_progress" else 0.0
    status_completed = 1.0 if state.status == "completed" else 0.0

    # Is this skill relevant for the target role?
    role_match = 1.0 if target_role in node.roles else 0.0

    # Content type and difficulty as numeric hints
    is_course = 1.0 if content.type == "course" else 0.0
    is_beginner = 1.0 if content.xp_level == "beginner" else 0.0

    # Simple normalization
    xp_ratio = max(0.0, min(1.0, xp_ratio))

    features = [
        xp_ratio,          # 0
        xp_gap,            # 1
        status_locked,     # 2
        role_match,        # 3
        status_in_progress,# 4
        status_completed,  # 5
        is_course,         # 6
        is_beginner,       # 7
    ]
    return features


def get_ai_recommendations(
    user_state: Dict[str, UserSkillState],
    target_role: str,
    top_k: int = 3
) -> List[ContentItem]:
    """
    Uses the TinyRecommendationModel to score and rank content items for the user.
    """

    scored_items = []

    for content in CONTENT_DB.values():
        skill_id = content.skill_id
        node = SKILL_DEFS[skill_id]
        state = user_state[skill_id]

        # Skip skills that are completely irrelevant to the target role
        if target_role not in node.roles:
            continue

        # Skip locked or already completed skills for now
        if state.status == "locked" or state.status == "completed":
            continue

        # Build features for this (user, skill, content, role)
        features = build_feature_vector(user_state, skill_id, content, target_role)
        score = MODEL.predict_proba(features)

        # Add a tiny random jitter to encourage exploration / tie-breaking
        score += random.random() * 0.02

        scored_items.append((score, content))

    # Sort by descending score
    scored_items.sort(key=lambda x: x[0], reverse=True)

    # Return top_k items
    return [item for score, item in scored_items[:top_k]]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    user_state = build_user_state_from_cv(sample_cv_features)
    update_statuses(user_state)

    print("--- User Skill Status (AI Version) ---")
    for sid, state in user_state.items():
        print(f"{sid:18} XP={state.current_xp:3} / {SKILL_DEFS[sid].required_xp:3}  → {state.status}")
    print("-" * 40)

    target_role = "data_scientist"
    next_actions = get_ai_recommendations(user_state, target_role)

    print(f"--- AI-Powered Adaptive Recommendations ---")
    print(f"Target role: {target_role}")
    if not next_actions:
        print("No specific recommendations found. Keep exploring!")
    else:
        print("Here are your next steps (ranked by AI model score):")
        for item in next_actions:
            print(f"- Skill: {item.skill_id:16} | {item.type:7} | {item.xp_level:9} -> {item.title} (ID: {item.content_id})")
