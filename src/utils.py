from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

RESULTS = Path(__file__).resolve().parents[1] / "results"
TEST_START = "2015-01-01"      # début de la période de test, la même pour tous
HORIZONS = [1, 5, 22]          # 1 jour, 1 semaine, 1 mois
FLOOR = 1e-4                   # plancher : une prévision de variance doit être > 0

def mse(y, f):
    y, f = np.asarray(y), np.asarray(f)
    return np.mean((y - f) ** 2)

def qlike(y, f):
    y, f = np.asarray(y), np.maximum(np.asarray(f), FLOOR)
    return np.mean(y / f - np.log(y / f) - 1)

def save_forecasts(df, model, index):
    """Sauvegarde au format commun : date, model, horizon, forecast, actual."""
    cols = ["date", "model", "horizon", "forecast", "actual"]
    assert list(df.columns) == cols, f"colonnes attendues : {cols}"
    assert (df["forecast"] > 0).all(), "prévision négative ou nulle"
    RESULTS.mkdir(exist_ok=True)
    df.to_csv(RESULTS / f"forecasts_{index}_{model}.csv", index=False)

def load_all_forecasts(index):
    files = RESULTS.glob(f"forecasts_{index}_*.csv")
    return pd.concat([pd.read_csv(f, parse_dates=["date"]) for f in files])

def loss_series(y, f, loss="qlike"):
    y, f = np.asarray(y), np.maximum(np.asarray(f), FLOOR)
    return y / f - np.log(y / f) - 1 if loss == "qlike" else (y - f) ** 2

def dm_test(y, f1, f2, h=1, loss="qlike"):
    """Diebold-Mariano. Statistique < 0 : le modèle 1 est meilleur."""
    d = loss_series(y, f1, loss) - loss_series(y, f2, loss)
    res = sm.OLS(d, np.ones(len(d))).fit(cov_type="HAC", cov_kwds={"maxlags": h})
    return float(res.tvalues[0]), float(res.pvalues[0])