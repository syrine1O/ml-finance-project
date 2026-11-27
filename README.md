# ml-finance-project

Prévision de la volatilité du S&P 500 et du TSX avec des modèles économétriques (HAR, GARCH) et du machine learning (LightGBM). Les modèles sont comparés avec les mêmes données, la même période de test et les mêmes mesures d'erreur.

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| `data/` | `spx.csv`, `tsx.csv` (rendements `ret` et variance réalisée `rv`) ; `raw/` : données brutes téléchargées |
| `notebooks/` | Notebooks numérotés (`00_...`, `01_donnees.ipynb`, ...) |
| `src/` | Code commun : `utils.py` (MSE, QLIKE, sauvegarde des prévisions) |
| `results/` | Fichiers de prévisions au format commun |
| `figures/` | Graphiques pour le rapport |
| `docs/` | Documentation (par ex. `variables.md`) |

## Installation

Python 3.11 ou 3.12 (Anaconda). Dans Anaconda Prompt (Windows) ou le Terminal (Mac) :

```
conda create -n mlfin python=3.12 -y
conda activate mlfin
git clone <lien-du-dépôt>
cd ml-finance-project
pip install -r requirements.txt
pip install jupyterlab
```

Pour travailler : `conda activate mlfin`, puis `jupyter lab`.

## Ordre d'exécution des notebooks

`01_donnees` → `05a_features` → `02_exploration` → `04_har` → `04b_log_har` → `03b_garch_multi` → `05_lightgbm_T11` → `06_resultats` → `07_robustesse`.

Chaque notebook de modèle écrit ses prévisions dans `results/` ; `06_resultats` les rassemble et produit les tables 4 et 6, les tests directs et la figure 5 ; `07_robustesse` ajoute les tests complémentaires (tables 7 à 12, figure 6) sans modifier les résultats principaux. `03_garch` est le notebook exploratoire du GARCH à h = 1 (figure 4, table 3b) ; il n'écrit pas de prévisions. `00_tests_utils` teste `src/utils.py`. Les anciens essais sont dans `notebooks/archive/` et ne doivent pas être relancés.

## Format des données

Colonnes de `data/spx.csv` et `data/tsx.csv` : `Date, open, high, low, close, ret, rv, vix`

- `ret` : rendement logarithmique quotidien, en % (×100)
- `rv` : variance réalisée Garman-Klass, en %² (×10 000)
- `vix` : VIX du jour (recopié de la veille si Wall Street est fermée)

## Format commun des prévisions

Chaque modèle sauvegarde ses prévisions avec `save_forecasts` de `src/utils.py`, dans `results/forecasts_<indice>_<modèle>.csv`, avec les colonnes :

`date, model, horizon, forecast, actual`

- `date` : jour où la prévision est faite, à la clôture
- `horizon` : 1, 5 ou 22 jours
- `forecast` : variance moyenne prévue sur les `horizon` jours suivants, en %²
- `actual` : variance réalisée moyenne sur ces mêmes jours

## Règles d'équipe

1. **Mêmes unités pour tous** : rendements en %, variance en %². Une prévision de variance doit être strictement positive.
2. **Mêmes mesures d'erreur** : seulement `mse` et `qlike` de `src/utils.py`. QLIKE est la mesure principale.
3. **Même période de test** : début le `2015-01-01` (`TEST_START`). On coupe toujours dans l'ordre du temps, jamais au hasard, et on n'utilise jamais d'information du futur.
4. **Un seul format de prévision** : tout passe par `save_forecasts`. On ne modifie pas `utils.py` sans prévenir l'équipe.
5. **Travail avec Git** : on fait *Fetch/Pull origin* avant de commencer, on envoie (*Commit* puis *Push*) avec un message clair, et on ne modifie pas le fichier d'une autre personne sans lui en parler.
