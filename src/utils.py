import numpy as np


def mse(y_true, y_pred):
    """Erreur quadratique moyenne."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean((y_true - y_pred) ** 2))


def qlike(y_true, y_pred):
    """QLIKE pour des prévisions de variance (valeurs > 0)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if (y_true <= 0).any() or (y_pred <= 0).any():
        raise ValueError("QLIKE exige des valeurs strictement positives.")
    ratio = y_true / y_pred
    return float(np.mean(ratio - np.log(ratio) - 1))
