# Variables utilisées par les modèles

Règle : chaque variable doit être connue à la clôture du jour t.
Sinon on utiliserait le futur (look-ahead).

| Variable | Définition | Connue à la clôture de t ? |
|---|---|---|
| rv_d | rv du jour t | Oui |
| rv_w | moyenne de rv de t-4 à t (5 jours) | Oui |
| rv_m | moyenne de rv de t-21 à t (22 jours) | Oui |
| ret | rendement du jour t, en % | Oui |
| ret_neg | min(ret, 0), seulement les jours de baisse | Oui |
| vix | niveau du VIX à la clôture de t | Oui |
| vix_diff | vix du jour t moins vix de la veille | Oui |

## Pourquoi ces variables

- rv_d, rv_w, rv_m : la volatilité est persistante (base du modèle HAR).
- ret_neg : une baisse augmente la volatilité plus qu'une hausse de même taille (effet de levier).
- vix : c'est l'anticipation du marché sur la volatilité à venir.
- vix_diff : une montée soudaine du VIX signale une peur qui augmente.
