# T5 — Construction des variables et des cibles

## 1. Objectif

Construire les variables explicatives et les cibles nécessaires à la prévision de la volatilité réalisée des indices S&P 500 (SPX) et S&P/TSX (TSX), aux horizons de 1, 5 et 22 jours de bourse.

Les données préparées sont enregistrées dans :
- data/features_spx.csv
- data/features_tsx.csv

## 2. Variables explicatives

- rv_d : volatilité réalisée quotidienne, disponible à la date t.
- rv_w : moyenne de la volatilité réalisée sur les cinq derniers jours de bourse, date t incluse.
- rv_m : moyenne de la volatilité réalisée sur les 22 derniers jours de bourse, date t incluse.
- ret : rendement de l'indice à la date t.
- ret_neg : composante négative du rendement, définie comme min(ret, 0).
- vix : indice VIX, indicateur des anticipations de volatilité du marché américain.

Les variables rv_d, rv_w et rv_m correspondent aux composantes quotidiennes, hebdomadaires et mensuelles utilisées dans l'approche HAR.

## 3. Variables cibles

- y_h1 : volatilité réalisée du prochain jour de bourse.
- y_h5 : moyenne de la volatilité réalisée des cinq prochains jours de bourse.
- y_h22 : moyenne de la volatilité réalisée des 22 prochains jours de bourse.

Les cibles sont calculées uniquement avec les observations futures. Elles ne sont jamais utilisées comme variables explicatives.

## 4. Prévention des fuites d'information

Les données sont triées chronologiquement.

À la date t :
- rv_w utilise les dates t-4 à t.
- rv_m utilise les 22 dernières observations connues.
- y_h5 utilise les dates t+1 à t+5.
- y_h22 utilise les dates t+1 à t+22.

Les tests anti-fuite ont réussi pour SPX et TSX sur la date vérifiée dans le notebook.

La séparation entraînement/test respecte l'ordre chronologique : 80 % des observations pour l'entraînement et 20 % pour le test.

Pour éviter une contamination aux frontières des périodes, il faut également vérifier que les cibles d'entraînement ne s'étendent pas sur la période de test, notamment pour les horizons de 5 et 22 jours.

## 5. Corrélations observées avec les cibles

Les corrélations de Pearson entre variables explicatives et cibles sont les suivantes.

| Variable | SPX y_h1 | SPX y_h5 | SPX y_h22 | TSX y_h1 | TSX y_h5 | TSX y_h22 |
|---|---:|---:|---:|---:|---:|---:|
| rv_d | 0.581 | 0.649 | 0.535 | 0.531 | 0.633 | 0.501 |
| rv_w | 0.649 | 0.724 | 0.622 | 0.633 | 0.743 | 0.596 |
| rv_m | 0.535 | 0.622 | 0.592 | 0.501 | 0.596 | 0.571 |
| ret | -0.187 | -0.187 | -0.129 | -0.137 | -0.175 | -0.122 |
| ret_neg | -0.427 | -0.446 | -0.365 | -0.344 | -0.410 | -0.331 |
| vix | 0.601 | 0.682 | 0.624 | 0.480 | 0.569 | 0.514 |

La volatilité hebdomadaire rv_w présente la corrélation positive la plus forte avec y_h5 pour les deux marchés.

Les rendements négatifs sont associés à une volatilité future plus élevée. La corrélation négative de ret_neg doit être interprétée en tenant compte du fait que cette variable est négative ou nulle.

Ces corrélations décrivent des associations statistiques et ne démontrent pas de relation causale.

## 6. Vérifications et limites

- Les fichiers de variables ont été générés avec 6 690 observations pour SPX et 6 670 pour TSX, et 9 colonnes chacun.
- Les résultats de corrélation et les tests anti-fuite ont été obtenus dans Google Colab.
- Les observations sans cible future complète doivent être retirées pour l'horizon concerné.
- Les valeurs manquantes doivent être contrôlées.
- La disponibilité réelle des valeurs VIX à la date de prévision doit être vérifiée.
- Les résultats de prédiction doivent être validés sur une période hors échantillon et idéalement avec une validation chronologique glissante.

## 7. Conclusion

Les variables explicatives et les cibles sont construites pour les deux indices. Les corrélations confirment l'intérêt des mesures historiques de volatilité, notamment rv_w, pour la prévision à cinq jours.

Les fichiers CSV constituent les livrables de préparation des données du T5. Les comparaisons de modèles LightGBM réalisées ensuite sont des analyses complémentaires.
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
