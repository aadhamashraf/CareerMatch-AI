"""Integrator package — glue to invoke scattered ai-features scripts from the repo.

This package loads feature modules from the `ai-features/` directory using
importlib so the existing notebooks/scripts do not need to be rewritten.

Use Integrator.orchestrator.CareerMatchOrchestrator for a single API to run
scoring, roadmap, micro-project recommendations, adaptive recommendations
and some other helpers.
"""

__all__ = ["orchestrator"]
