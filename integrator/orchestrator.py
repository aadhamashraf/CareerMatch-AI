"""Simple orchestrator that loads scattered feature scripts and exposes a
consistent API for chaining them together.

Notes:
- This uses SourceFileLoader to import the Python scripts inside `ai-features/`
  which contains hyphen in the folder name and therefore cannot be imported as
  a normal package.
- The orchestrator keeps wrappers minimal and defensive so the repo can be
  used without installing heavy dependencies (e.g., SBERT, OpenAI). Missing
  features return friendly results explaining what failed.
"""
from importlib.machinery import SourceFileLoader
from types import ModuleType
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "ai-features"


def _load_module(name: str, filename: str) -> ModuleType:
    """Load a Python file by a path relative to ai-features.

    The orchestrator was updated to use a numbered directory layout. This
    helper accepts either a simple filename (legacy) or a relative path like
    "9. Explainable Scoring Engine/scoring_engine.py" and resolves it.
    """
    # Try direct path first
    path = FEATURES_DIR / filename
    if not path.exists():
        # Try to locate the file recursively by name
        target_name = Path(filename).name
        found = list(FEATURES_DIR.rglob(target_name))
        if not found:
            raise FileNotFoundError(f"Feature file not found (tried {filename}): {path}")
        # pick first match
        path = found[0]
    return SourceFileLoader(name, str(path)).load_module()


class CareerMatchOrchestrator:
    """High-level orchestrator that exposes unified methods to run features.

    All methods accept plain Python data structures (dicts/strings) and return
    JSON-serializable outputs where possible.
    """

    def __init__(self):
        # Lazy-load modules only when a method is invoked.
        self._modules: Dict[str, ModuleType] = {}

    def _module(self, name: str, filename: str) -> ModuleType:
        key = name
        if key not in self._modules:
            self._modules[key] = _load_module(name, filename)
        return self._modules[key]

    # --- Scoring / Explanation ---
    def score_cv(self, cv_obj: Dict[str, Any], job_title: str) -> Dict[str, Any]:
        """Runs the explainable scoring engine and returns scores + explanation."""
        mod = self._module("explainable_scoring_engine", "9. Explainable Scoring Engine/scoring_engine.py")
        # infer essential skills if module exposes helper
        essentials = []
        if hasattr(mod, "infer_essential_skills"):
            try:
                essentials = mod.infer_essential_skills(job_title)
            except Exception:
                essentials = []

        try:
            C = mod.completeness_score(cv_obj, essentials)
            R = mod.relevance_score(cv_obj, job_title)
            S_detail = mod.strength_score(cv_obj, essentials, {"Edu": 0.2, "Exp": 0.25, "Proj": 0.2, "Skills": 0.25, "Cert": 0.1})
            scores = {"Strength_S": round(S_detail["S"], 2), "Relevance_R": round(R, 2), "Completeness_C": round(C, 2)}
            subs = {"Education": round(S_detail["Edu"], 2), "Experience": round(S_detail["Exp"], 2), "Projects": round(S_detail["Proj"], 2), "Skills": round(S_detail["Skills"], 2), "Certifications": round(S_detail["Cert"], 2)}
            explanation = mod.make_explanation(scores, subs, cv_obj, essentials, job_title)
            return {"scores": scores, "subscores": subs, "explanation": explanation}
        except Exception as e:
            return {"error": "scoring_failed", "message": str(e)}

    # --- Roadmap ---
    def build_roadmap(self, resume_text: str, target_role: str, timeline_months: Optional[int] = None) -> Dict[str, Any]:
        mod = self._module("transparent_career_roadmap", "11. Transparent Career Roadmap Generation/roadmap_generation.py")
        try:
            ro = mod.build_roadmap_logic(resume_text, target_role, timeline_months)
            # model_dump or dict-like
            try:
                return ro.model_dump()
            except Exception:
                # fallback for Pydantic v1 or plain dict
                if isinstance(ro, dict):
                    return ro
                return dict(target_role=ro.target_role, detected_skills=ro.detected_skills, gaps=ro.gaps, roadmap=[s.dict() for s in ro.roadmap], narrative=ro.narrative)
        except Exception as e:
            return {"error": "roadmap_failed", "message": str(e)}

    # --- Micro-project recommendations ---
    def recommend_micro_projects(self, cv_obj: Dict[str, Any], job_title: str, k_per_skill: int = 3) -> Dict[str, Any]:
        mod = self._module("micro_project_recommender", "6. Micro Project Recommender/micro_project_recommender.py")
        # infer essential skills
        essentials = []
        if hasattr(mod, "infer_essential_skills"):
            try:
                essentials = mod.infer_essential_skills(job_title)
            except Exception:
                essentials = []
        # default: require cv_obj
        try:
            recs = mod.recommend_projects(cv_obj, essentials, mod.proj_df, k_per_skill, role_hint=job_title)
            # convert dataframes to serializable dicts
            out = {k: (v.to_dict(orient="records") if hasattr(v, "to_dict") else v) for k, v in recs.items()}
            return {"essentials": essentials, "recommendations": out}
        except Exception as e:
            return {"error": "micro_recs_failed", "message": str(e)}

    # --- Adaptive recommendation (skill tree + content db) ---
    def adaptive_recommend(self, cv_features: Dict[str, Any], target_role: str, top_k: int = 3) -> Dict[str, Any]:
        mod = self._module("adaptive_recommendation_system", "2. Adaptive Recommendation System/adaptive_recommendation.py")
        try:
            user_state = mod.build_user_state_from_cv(cv_features)
            mod.update_statuses(user_state)
            recs = mod.get_adaptive_recommendations(user_state, target_role, top_k=top_k)
            # convert dataclass objects to dicts
            out = [vars(r) for r in recs]
            status = {k: vars(v) for k, v in user_state.items()}
            return {"user_state": status, "recommendations": out}
        except Exception as e:
            return {"error": "adaptive_failed", "message": str(e)}

    # --- Resume polishing (LLM) ---
    def polish_resume_sentence(self, sentence: str) -> Dict[str, Any]:
        mod = self._module("resume_polish", "10. Resume Polishing Suggestions/resume_polish.py")
        try:
            if not hasattr(mod, "polish_resume_sentence_v2"):
                return {"error": "not_supported", "message": "polish function not available in module"}
            polished = mod.polish_resume_sentence_v2(sentence)
            return {"original": sentence, "polished": polished}
        except Exception as e:
            return {"error": "polish_failed", "message": str(e)}

    # --- Engagement prediction (Feature 20) ---
    def assess_engagement(self, user_data: Dict[str, Any], threshold: float = 0.7) -> Dict[str, Any]:
        """Train a small synthetic model (from feature 20) and assess the provided user session.

        This is intentionally lightweight and trains on synthetic data so it doesn't
        require any external datasets.
        """
        mod = self._module("engagement_prediction", "20. Engagement Prediction/engagement_prediction.py")
        try:
            df = mod.generate_synthetic_engagement_data(num_samples=300)
            model, acc = mod.train_engagement_model(df)
            out = mod.check_user_engagement(model, user_data, threshold)
            out["model_accuracy"] = acc
            return out
        except Exception as e:
            return {"error": "engagement_check_failed", "message": str(e)}

    # --- Knowledge graph / reasoning (Feature 21) ---
    def query_knowledge_graph(self, query_type: str, subject: str) -> Dict[str, Any]:
        """Run a small query on the dynamic knowledge graph. query_type must be one of:
        - 'courses_for_skill'
        - 'projects_for_skill'
        - 'skills_for_project'

        Returns JSON-serializable results.
        """
        mod = self._module("knowledge_graph", "21. Dynamic Knowledge Graph/knowledge_graph.py")
        try:
            G = mod.build_sample_graph()
            if query_type == 'courses_for_skill':
                return {"courses": mod.courses_teaching_skill(G, subject)}
            if query_type == 'projects_for_skill':
                return {"projects": mod.projects_requiring_skill(G, subject)}
            if query_type == 'skills_for_project':
                return {"skills": mod.find_skills_for_project(G, subject)}
            return {"error": "unknown_query", "message": f"unknown query_type '{query_type}'"}
        except Exception as e:
            return {"error": "kg_query_failed", "message": str(e)}

    # --- Bias auditing ---
    def audit_fairness(self, candidate_df) -> Dict[str, Any]:
        mod = self._module("bias_detection", "4. Bias Detection & Fairness Auditing/bias_detection.py")
        try:
            # The notebook exposes convenience functions; attempt to call fairness_table for common columns
            reports = {}
            for group in ["gender", "education_tier", "background"]:
                if group in candidate_df.columns:
                    rep = mod.fairness_table(candidate_df, group)
                    # serialize results for JSON
                    reports[group] = {
                        "reference_group": rep["reference_group"].to_dict(orient="records") if rep.get("reference_group") is not None else None,
                        "rates": rep["rates"].to_dict(orient="records") if rep.get("rates") is not None else None,
                        "calibration": rep["calibration"].to_dict(orient="records") if rep.get("calibration") is not None else None,
                    }
            return reports
        except Exception as e:
            return {"error": "fairness_failed", "message": str(e)}


if __name__ == "__main__":
    print("Integrator orchestrator — import and use CareerMatchOrchestrator from your code.")
