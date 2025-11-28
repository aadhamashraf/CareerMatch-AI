# CareerMatch Orchestrator (Integrator)

This small integration layer (in `integrator/`) provides a single, lightweight API
to call and chain the existing, scattered AI feature scripts inside `ai-features/`.

Why this exists
- The repository contains many proof-of-concept notebooks and scripts in `ai-features/`.
- The orchestrator loads those scripts (without rewriting them) and offers a stable
  API so you can build demos and glue multiple features together.

What it exposes
- `integrator.orchestrator.CareerMatchOrchestrator` — top-level class with methods:
  - `score_cv(cv_obj, job_title)` → explainable scoring + explanation
  - `build_roadmap(resume_text, target_role)` → roadmap planner
  - `recommend_micro_projects(cv_obj, job_title)` → micro-project recommendations
  - `adaptive_recommend(cv_features, target_role)` → recommendations using skill-tree
  - `polish_resume_sentence(sentence)` → uses `10. Resume Polishing Suggestions/resume_polish.py` (requires OpenAI creds for real runs)
  - `audit_fairness(candidate_df)` → runs fairness audits on a pandas DataFrame
  - `assess_engagement(user_data, threshold=0.7)` → trains a small synthetic model and assesses drop-off risk (Feature 20)
  - `query_knowledge_graph(query_type, subject)` → run tiny queries against the skills–courses–projects knowledge graph (Feature 21)

Quick demo
1. Run the demo runner (uses sample data if no file is provided):

```
python -m integrator.run_pipeline  # optionally pass a cv json file and job title
```

Next steps
- Move high-value functions into small importable modules to remove dependency on import-from-file.
- Add more tests and CI so each feature can be validated independently before composing them.
