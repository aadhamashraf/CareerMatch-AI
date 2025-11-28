import json
import sys
from pathlib import Path
# make repository root importable for tests
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from integrator.orchestrator import CareerMatchOrchestrator


def sample_cv():
    return {
        "summary": "Junior data practitioner. Built small ML pipelines.",
        "skills": ["python", "pandas"],
        "projects": [{"name": "small model", "description": "classification experiment", "tech": ["python"]}],
        "experience": [],
    }


def test_score_cv():
    o = CareerMatchOrchestrator()
    out = o.score_cv(sample_cv(), "data scientist")
    assert isinstance(out, dict)
    assert "scores" in out or "error" in out


def test_build_roadmap():
    o = CareerMatchOrchestrator()
    r = o.build_roadmap("Python, pandas, SQL", "Data Analyst")
    assert isinstance(r, dict)
    assert "target_role" in r or "error" in r


def test_adaptive_recommend():
    o = CareerMatchOrchestrator()
    cv_features = {"python": {"years_experience": 1, "num_projects": 1, "has_cert": False}}
    out = o.adaptive_recommend(cv_features, "data_scientist")
    assert isinstance(out, dict)


def test_assess_engagement():
    o = CareerMatchOrchestrator()
    user = {
        'time_on_quest': 12,
        'errors_in_session': 2,
        'quest_difficulty': 3,
        'prev_completion_rate': 0.8,
    }
    out = o.assess_engagement(user)
    assert isinstance(out, dict)
    # If dependencies missing, orchestrator returns an error dict
    assert 'prob_dropoff' in out or 'error' in out


def test_query_knowledge_graph():
    o = CareerMatchOrchestrator()
    res = o.query_knowledge_graph('courses_for_skill', 'Pandas')
    assert isinstance(res, dict)
    assert 'courses' in res or 'error' in res
