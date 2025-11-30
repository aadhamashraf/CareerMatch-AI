import io, json, math, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict, List, Optional, Tuple
from sklearn.metrics import confusion_matrix, brier_score_loss, roc_curve
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore")

# For pretty display in notebooks; fall back to print if not available
try:
    from IPython.display import display
except ImportError:
    def display(x):
        print(x)



# Data loading
try:
    from google.colab import files
    COLAB = True
except Exception:
    COLAB = False

df = None
if COLAB:
    print("Upload a CSV with columns: candidate_id, score, [label], gender, education_tier, background")
    up = files.upload()
    if up:
        fname = list(up.keys())[0]
        df = pd.read_csv(io.BytesIO(up[fname]))
        print("Loaded:", fname, df.shape)

# If no CSV uploaded, generate synthetic data
if df is None:
    rng = np.random.default_rng(7)
    n = 400
    df = pd.DataFrame({
        "candidate_id": np.arange(n),
        "score": np.clip(rng.normal(65, 12, n), 0, 100),
        "gender": rng.choice(["male", "female", "nonbinary"], n, p=[0.5, 0.47, 0.03]),
        "education_tier": rng.choice(
            ["top_tier", "regular", "bootcamp", "self_taught"],
            n,
            p=[0.25, 0.55, 0.10, 0.10],
        ),
        "background": rng.choice(["traditional", "non_traditional"], n, p=[0.7, 0.3]),
    })

    # Simulate labels with a logistic relationship to score (this is like a true model)
    logits = (df["score"] - 60) / 8
    probs = 1 / (1 + np.exp(-logits))
    df["label"] = (rng.random(n) < probs).astype(int)

# Normalize column names
df.columns = [c.strip().lower() for c in df.columns]


# Train a simple model (Logistic Regression) 
LABEL_COL = "label"
GROUP_COLS = ["gender", "education_tier", "background"]

if LABEL_COL not in df.columns:
    raise ValueError(f"Expected a '{LABEL_COL}' column for training the model.")

X = df[["score"]].values 
y = df[LABEL_COL].astype(int).values

model = LogisticRegression()
model.fit(X, y)

df["model_score"] = model.predict_proba(X)[:, 1] * 100.0

SCORE_COL = "model_score"

USE_TOP_K = False         
SCORE_THRESHOLD = 70.0    
TOP_K = 100                

DI_LOWER, DI_UPPER = 0.8, 1.25


# Fairness / metrics helpers
def select_positive_mask(scores: pd.Series) -> pd.Series:
    """
    Convert continuous scores into binary selection decisions.
    Either:
      - Top-K selection, or
      - Threshold-based selection.
    """
    if USE_TOP_K:
        k = min(TOP_K, len(scores))
        if k <= 0:
            return pd.Series(False, index=scores.index)
        cutoff = scores.sort_values(ascending=False).iloc[k - 1]
        return scores >= cutoff
    return scores >= SCORE_THRESHOLD


def group_rates(
    y_pred: pd.Series,
    y_true: Optional[pd.Series],
    group: pd.Series
) -> pd.DataFrame:
    """
    Compute selection rate and confusion-matrix-based rates per group.
    """
    out = []
    for g, idx in group.groupby(group).groups.items():
        yp = y_pred.loc[idx]
        sel_rate = yp.mean() if len(yp) else np.nan
        row = {"group": g, "n": len(idx), "selection_rate": sel_rate}

        if y_true is not None and y_true.notna().any():
            yt = y_true.loc[idx].astype(int)
            try:
                tn, fp, fn, tp = confusion_matrix(yt, yp.astype(int), labels=[0, 1]).ravel()
            except ValueError:
                # Handle edge cases where confusion_matrix cannot ravel (e.g., only one class)
                tn = fp = fn = tp = 0
                if yt.eq(0).all() and yp.eq(0).all():
                    tn = len(yt)
                if yt.eq(1).all() and yp.eq(1).all():
                    tp = len(yt)
            tpr = tp / (tp + fn) if (tp + fn) > 0 else np.nan
            fpr = fp / (fp + tn) if (fp + tn) > 0 else np.nan
            row.update({"tpr": tpr, "fpr": fpr})

        out.append(row)

    return pd.DataFrame(out).sort_values("group").reset_index(drop=True)


def disparate_impact(selection_rates: pd.Series, ref_rate: float) -> pd.Series:
    """
    Disparate impact = selection_rate_group / selection_rate_reference.
    """
    return selection_rates / (ref_rate if ref_rate > 0 else np.nan)


def brier_by_group(
    scores: pd.Series,
    labels: pd.Series,
    group: pd.Series
) -> pd.DataFrame:
    """
    Compute Brier score per group (calibration measure).
    """
    out = []
    p = np.clip(scores / 100.0, 1e-6, 1 - 1e-6)
    for g, idx in group.groupby(group).groups.items():
        y = labels.loc[idx].astype(int)
        if len(idx) == 0:
            b = np.nan
        else:
            b = brier_score_loss(y, p.loc[idx])
        out.append({"group": g, "n": len(idx), "brier": b})
    return pd.DataFrame(out).sort_values("group").reset_index(drop=True)


def fairness_table(df: pd.DataFrame, group_col: str) -> Dict[str, pd.DataFrame]:
    """
    Build all fairness metrics for a single grouping column (e.g. gender).
    """
    assert SCORE_COL in df, f"Missing {SCORE_COL}"
    y_pred = select_positive_mask(df[SCORE_COL])
    y_true = df[LABEL_COL] if LABEL_COL in df.columns else None
    grp = df[group_col].astype(str)

    rates = group_rates(y_pred, y_true, grp)

    # Reference group = group with highest selection rate
    ref_idx = rates["selection_rate"].idxmax()
    ref_group = rates.loc[ref_idx, "group"]
    ref_rate = rates.loc[ref_idx, "selection_rate"]

    rates["disparate_impact"] = disparate_impact(rates["selection_rate"], ref_rate)
    rates["stat_parity_diff"] = rates["selection_rate"] - ref_rate
    rates["flag_80pct_rule"] = ~rates["disparate_impact"].between(DI_LOWER, DI_UPPER)

    cal = None
    if LABEL_COL in df:
        cal = brier_by_group(df[SCORE_COL], df[LABEL_COL], grp)

    return {
        "group": group_col,
