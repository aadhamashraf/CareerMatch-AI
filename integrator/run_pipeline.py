"""Simple CLI demo that runs a full pipeline using CareerMatchOrchestrator.

This reads a CV JSON file and a job title then runs scoring, roadmap generation,
micro-project recommendations and adaptive recommendations, printing the
combined result.
"""
import json
import sys
from pathlib import Path

from integrator.orchestrator import CareerMatchOrchestrator


SAMPLE_CV = {
    "summary": "Data scientist with experience building predictive models and analysis.",
    "skills": ["python", "pandas", "scikit-learn"],
    "projects": [{"name": "Sales Predictor", "description": "Built a regression model for sales forecasting", "tech": ["python", "pandas", "scikit-learn"]}],
    "experience": [{"company": "Acme", "title": "Data Scientist", "years": 2}],
    "education": [{"degree": "BSc Computer Science", "school": "Example University"}],
}


def main():
    cv_path = None
    job_title = "Machine Learning Engineer"
    if len(sys.argv) > 1:
        cv_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        job_title = sys.argv[2]

    if cv_path and cv_path.exists():
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_obj = json.load(f)
    else:
        cv_obj = SAMPLE_CV

    orchestrator = CareerMatchOrchestrator()

    print("\n=== Running scoring ===")
    scoring = orchestrator.score_cv(cv_obj, job_title)
    print(json.dumps(scoring, indent=2, ensure_ascii=False))

    print("\n=== Building roadmap (from sample resume text) ===")
    sample_text = "Python, pandas, scikit-learn, some exposure to docker."
    roadmap = orchestrator.build_roadmap(sample_text, job_title)
    print(json.dumps(roadmap, indent=2, ensure_ascii=False))

    print("\n=== Micro project recommendations ===")
    micro = orchestrator.recommend_micro_projects(cv_obj, job_title)
    if isinstance(micro, dict) and "recommendations" in micro:
        # show just keys
        print("Recommended for missing skills:", list(micro.get("recommendations", {}).keys()))
    else:
        print(json.dumps(micro, indent=2, ensure_ascii=False))

    print("\n=== Adaptive recommendations (skill-tree) ===")
    # building the `cv_features` map expected by adaptive_recommendation_system
    cv_features = {"python": {"years_experience": 1, "num_projects": 1, "has_cert": False}}
    adaptive = orchestrator.adaptive_recommend(cv_features, "data_scientist")
    print(json.dumps(adaptive, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
