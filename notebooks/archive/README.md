# Archives

Notebooks de travail conservés pour l'historique. Ils ne font pas partie du pipeline et ne doivent pas être relancés.

- `00_lightgbm_essai.ipynb` : premier essai de LightGBM.
- `05_lightgbm_v1.ipynb` : LightGBM v1 (S&P 500 seulement, hyperparamètres fixés à la main). Il montre pourquoi l'objectif `gamma` a été retenu : avec la perte quadratique par défaut, certaines prévisions sont négatives, ramenées au plancher de 1e-4, et la QLIKE explose (ex. 2018-12-26). **Attention : relancé, il écraserait `results/forecasts_spx_LGBM.csv`.** La version officielle est `05_lightgbm_T11.ipynb`.
