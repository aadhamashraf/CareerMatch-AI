"""Engagement prediction / challenge personalization utilities.

This module was extracted from the notebook (Feature 20). It provides a
simple synthetic-data generator, model training utilities and a small
runtime helper to decide on interventions.

The code is import-safe (no heavy work at import time) and includes a
lightweight demo under `if __name__ == '__main__'`.
"""
from typing import Dict, Tuple, Any

try:
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
except Exception:  # pragma: no cover - environment may not have ML deps
    np = None
    pd = None
    LogisticRegression = None


def generate_synthetic_engagement_data(num_samples: int = 500, seed: int = 42):
    """Create a simple synthetic dataset matching the original notebook."""
    if np is None or pd is None:
        raise RuntimeError("numpy/pandas are required for synthetic data generation")

    np.random.seed(seed)

    data = {
        'time_on_quest': np.random.uniform(5, 30, num_samples),
        'errors_in_session': np.random.randint(0, 15, num_samples),
        'quest_difficulty': np.random.randint(1, 6, num_samples),
        'prev_completion_rate': np.random.uniform(0.3, 1.0, num_samples),
    }
    df = pd.DataFrame(data)

    score = (
        (df['errors_in_session'] * 1.5)
        + (df['time_on_quest'] / df['quest_difficulty'])
        - (df['prev_completion_rate'] * 10)
    )
    prob_dropoff = 1 / (1 + np.exp(-(score - 10) / 5))
    df['dropped_off'] = (prob_dropoff > np.random.uniform(0, 1, num_samples)).astype(int)
    return df


def train_engagement_model(df):
    """Train a simple logistic regression on the synthetic dataset.

    Returns the trained model and a test dataset for evaluation.
    """
    if LogisticRegression is None:
        raise RuntimeError("sklearn is required to train the model")

    features = ['time_on_quest', 'errors_in_session', 'quest_difficulty', 'prev_completion_rate']
    target = 'dropped_off'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return model, acc


def predict_dropoff(model, user_data: Dict[str, Any]) -> float:
    """Return probability of drop-off for a single user's session dict.

    The user_data dict should contain keys in the same order as the features
    created by generate_synthetic_engagement_data.
    """
    features = ['time_on_quest', 'errors_in_session', 'quest_difficulty', 'prev_completion_rate']
    arr = [[user_data.get(k) for k in features]]
    if hasattr(model, 'predict_proba'):
        return float(model.predict_proba(arr)[0][1])
    # fallback (deterministic): use predict()
    return float(model.predict(arr)[0])


def check_user_engagement(model, user_data: Dict[str, Any], threshold: float = 0.7) -> Dict[str, Any]:
    """Helper that returns decision + probability given a user session dict."""
    prob = predict_dropoff(model, user_data)
    decision = 'intervene' if prob > threshold else 'ok'
    return {'prob_dropoff': prob, 'decision': decision}


if __name__ == '__main__':
    # run a short demo if executed directly
    print('Demo: training engagement model on synthetic data...')
    df = generate_synthetic_engagement_data(300)
    model, acc = train_engagement_model(df)
    print(f'Training complete — test accuracy: {acc:.2f}')

    sample_user = {
        'time_on_quest': 28,
        'errors_in_session': 12,
        'quest_difficulty': 4,
        'prev_completion_rate': 0.5,
    }
    out = check_user_engagement(model, sample_user, threshold=0.7)
    print('Sample user decision:', out)
