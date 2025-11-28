import io, json, math, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict, List, Optional, Tuple
from sklearn.metrics import confusion_matrix, brier_score_loss, roc_curve

warnings.filterwarnings("ignore")

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

if df is None:
    rng = np.random.default_rng(7)
    n = 400
    df = pd.DataFrame({
        "candidate_id": np.arange(n),
        "score": np.clip(rng.normal(65, 12, n), 0, 100),
        "gender": rng.choice(["male","female","nonbinary"], n, p=[0.5,0.47,0.03]),
        "education_tier": rng.choice(["top_tier","regular","bootcamp","self_taught"], n, p=[0.25,0.55,0.1,0.1]),
        "background": rng.choice(["traditional","non_traditional"], n, p=[0.7, 0.3]),
    })
    logits = (df["score"] - 60)/8
    probs = 1 / (1 + np.exp(-logits))
    df["label"] = (rng.random(n) < probs).astype(int)

df.columns = [c.strip().lower() for c in df.columns]

SCORE_COL = "score"
LABEL_COL = "label"
GROUP_COLS = ["gender", "education_tier", "background"]

USE_TOP_K = False
SCORE_THRESHOLD = 70.0
TOP_K = 100

DI_LOWER, DI_UPPER = 0.8, 1.25


def select_positive_mask(scores: pd.Series) -> pd.Series:
    if USE_TOP_K:
        k = min(TOP_K, len(scores))
        cutoff = scores.sort_values(ascending=False).iloc[k-1] if k > 0 else 1e9
        return scores >= cutoff
    return scores >= SCORE_THRESHOLD


def group_rates(y_pred: pd.Series, y_true: Optional[pd.Series], group: pd.Series) -> pd.DataFrame:
    out = []
    for g, idx in group.groupby(group).groups.items():
        yp = y_pred.loc[idx]
        sel_rate = yp.mean() if len(yp) else np.nan
        row = {"group": g, "n": len(idx), "selection_rate": sel_rate}
        if y_true is not None and y_true.notna().any():
            yt = y_true.loc[idx].astype(int)
            try:
                tn, fp, fn, tp = confusion_matrix(yt, yp.astype(int), labels=[0,1]).ravel()
            except ValueError:
                tn=fp=fn=tp=0
                if yt.eq(0).all() and yp.eq(0).all(): tn=len(yt)
                if yt.eq(1).all() and yp.eq(1).all(): tp=len(yt)
            tpr = tp / (tp + fn) if (tp + fn) > 0 else np.nan
            fpr = fp / (fp + tn) if (fp + tn) > 0 else np.nan
            row.update({"tpr": tpr, "fpr": fpr})
        out.append(row)
    return pd.DataFrame(out).sort_values("group").reset_index(drop=True)


def disparate_impact(selection_rates: pd.Series, ref_rate: float) -> pd.Series:
    return selection_rates / (ref_rate if ref_rate > 0 else np.nan)


def brier_by_group(scores: pd.Series, labels: pd.Series, group: pd.Series) -> pd.DataFrame:
    out = []
    p = np.clip(scores / 100.0, 1e-6, 1-1e-6)
    for g, idx in group.groupby(group).groups.items():
        y = labels.loc[idx].astype(int)
        b = brier_score_loss(y, p.loc[idx]) if len(idx) else np.nan
        out.append({"group": g, "n": len(idx), "brier": b})
    return pd.DataFrame(out).sort_values("group").reset_index(drop=True)


def fairness_table(df: pd.DataFrame, group_col: str) -> Dict[str, pd.DataFrame]:
    assert SCORE_COL in df, f"Missing {SCORE_COL}"
    y_pred = select_positive_mask(df[SCORE_COL])
    y_true = df[LABEL_COL] if LABEL_COL in df else None
    grp = df[group_col].astype(str)

    rates = group_rates(y_pred, y_true, grp)
    ref_idx = rates["selection_rate"].idxmax()
    ref_group = rates.loc[ref_idx, "group"]
    ref_rate = rates.loc[ref_idx, "selection_rate"]

    rates["disparate_impact"] = disparate_impact(rates["selection_rate"], ref_rate)
    rates["stat_parity_diff"] = rates["selection_rate"] - ref_rate
    rates["flag_80pct_rule"] = ~rates["disparate_impact"].between(DI_LOWER, DI_UPPER)

    cal = None
    if LABEL_COL in df:
        cal = brier_by_group(df[SCORE_COL], df[LABEL_COL], grp)

    return {"group": group_col, "reference_group": pd.DataFrame([{"reference_group": ref_group, "reference_rate": ref_rate}]), "rates": rates, "calibration": cal}


def serialize_reports(reports: Dict[str, Dict]) -> Dict:
    out = {"policy": {"use_top_k": USE_TOP_K, "score_threshold": SCORE_THRESHOLD, "top_k": TOP_K, "score_column": SCORE_COL, "label_column": LABEL_COL if LABEL_COL in df.columns else None, "di_bounds": [DI_LOWER, DI_UPPER], }, "audits": {}}
    for g, rep in reports.items():
        ref = rep["reference_group"].to_dict(orient="records")[0]
        rates = rep["rates"].to_dict(orient="records")
        cal = rep["calibration"].to_dict(orient="records") if rep["calibration"] is not None else None
        out["audits"][g] = {"reference_group": ref, "rates": rates, "calibration": cal}
    return out


def mitigation_hints():
    tips = [
        "- Review feature set for proxies of protected attributes; drop/transform if needed.",
        "- Consider **group-aware thresholding** (tune cutoffs to equalize TPR or selection rates within acceptable bands).",
        "- Use **post-processing** methods like reject-option classification to nudge borderline decisions fairly.",
        "- Try **re-weighting** or **re-sampling** training data to balance representation.",
        "- Add **explainability**: log per-candidate reasons to detect systematic gaps (e.g., projects count vs. education).",
        "- Monitor over time: run this audit per batch/week and store metrics to catch drift."
    ]
    return "\n".join(tips)


if __name__ == "__main__":
    available_groups = [g for g in GROUP_COLS if g in df.columns]
    reports = {}
    for g in available_groups:
        reports[g] = fairness_table(df, g)

    for g in reports:
        print("\n==============================")
        print(f"FAIRNESS REPORT by '{g}'")
        print("==============================")
        display(reports[g]["reference_group"])
        display(reports[g]["rates"])
        if reports[g]["calibration"] is not None:
            print("Calibration (Brier score, lower is better):")
            display(reports[g]["calibration"])

    for g in available_groups:
        plot_selection_rates(df, g)
        plot_score_hist(df, g)

    report_json = serialize_reports(reports)

    flags = []
    for g, rep in reports.items():
        r = rep["rates"]
        bad = r[r["flag_80pct_rule"] == True]
        if len(bad):
            for _, row in bad.iterrows():
                flags.append({"group": g, "value": row["group"], "disparate_impact": round(float(row["disparate_impact"]), 3)})
    flags_df = pd.DataFrame(flags)
    print("\n=== Flags (violating 80% rule) ===")
    display(flags_df if len(flags_df) else pd.DataFrame([{"status": "No DI violations"}]))

    pd.DataFrame(report_json["audits"][available_groups[0]]["rates"]).to_csv("fairness_rates_sample.csv", index=False)
    with open("fairness_report.json", "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)
    print("Saved: fairness_report.json, fairness_rates_sample.csv")

    print("\n=== Mitigation Hints ===\n" + mitigation_hints())
