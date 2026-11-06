# T5 Construction des variables et des cibles SPX et TSX

## 1. Objectif et fichiers

Préparer les variables explicatives et les cibles des indices S&P 500 (SPX) et S&P/TSX (TSX), aux horizons de 1, 5 et 22 séances. Le notebook `notebooks/05a_features.ipynb` lit `data/spx.csv` et `data/tsx.csv`, puis écrit `data/features_spx.csv` et `data/features_tsx.csv`.

Une seule documentation réunit ici les définitions et le tableau des variables de l’équipe. Toutes les variables explicatives doivent être connues à la clôture de la séance t. Les cibles correspondent aux séances strictement suivantes et ne servent jamais de variables explicatives.

## 2. Données et convention temporelle

Les lignes sont triées chronologiquement. `Date` est la date d’information t, conservée comme index du tableau et comme première colonne des CSV. Les horizons désignent des observations successives de chaque marché, et non des jours calendaires. Les calendriers SPX et TSX peuvent différer.

Les fichiers sources fournissent `rv`, `ret` et `vix`. La préparation conserve leur définition et leur échelle. En particulier, elle ne transforme pas `rv` par racine carrée et ne modifie pas son annualisation : sa construction relève de la préparation des données sources. `ret` est exprimé en pourcentage selon la convention de l’équipe.

## 3. Variables explicatives

| Variable | Définition à t | Connue à la clôture de t ? |
|---|---|---|
| `rv_d` | `rv` de la séance t | Oui, sous réserve de la disponibilité des données sources |
| `rv_w` | Moyenne de `rv` de t−4 à t, soit 5 observations | Oui |
| `rv_m` | Moyenne de `rv` de t−21 à t, soit 22 observations | Oui |
| `ret` | Rendement de la séance t, en % | Oui |
| `ret_neg` | `min(ret, 0)`, nul en l’absence de rendement négatif | Oui |
| `vix` | Niveau du VIX de la séance t fourni dans les données | Oui, sous réserve de la disponibilité et de l’alignement des clôtures |
| `vix_diff` | VIX à t moins VIX à l’observation précédente disponible | Oui, sous la même réserve |

`vix_diff` se calcule avec `data["vix"].diff()` après tri et indexation des dates. Il mesure une variation en points de VIX, et non une variation relative en pourcentage. Les sept variables figurent dans les deux fichiers de variables.

### Motivation financière

Les composantes quotidienne, hebdomadaire et mensuelle de `rv` décrivent la persistance de la mesure réalisée et constituent les composantes historiques de l’approche HAR. `ret_neg` permet de représenter une éventuelle asymétrie entre les baisses et les hausses. Le VIX renseigne sur les anticipations de volatilité du marché américain, y compris lorsqu’il sert de variable explicative du TSX. Sa variation `vix_diff` décrit les changements de cet indicateur. Ces motivations ne constituent pas une preuve de causalité ou de performance prédictive.

## 4. Cibles futures

| Cible | Définition à la date d’information t | Disponible à la clôture de t ? |
|---|---|---|
| `y_h1` | `rv` à t+1 | Non |
| `y_h5` | Moyenne de `rv` de t+1 à t+5 | Non |
| `y_h22` | Moyenne de `rv` de t+1 à t+22 | Non |

La formule commune est `data["rv"].rolling(h).mean().shift(-h)`, pour h égal à 1, 5 ou 22. Le décalage aligne chaque moyenne strictement future sur la date t. Aucune cible n’inclut la valeur de `rv` à t.

Le tableau commun retire les lignes incomplètes sur toutes les colonnes avec `dropna()`. Avec les sources fournies, 21 lignes au début sont exclues faute d’historique mensuel et 22 à la fin faute de cible complète à 22 séances. Les trois horizons utilisent donc les mêmes lignes. Il ne s’agit pas d’un échantillon maximal distinct pour chaque horizon.

## 5. Protocole de l’équipe pour les modèles ultérieurs

La période de test commence le **1er janvier 2015**. Les mesures prévues sont **MSE et QLIKE**, selon les conventions d’évaluation de l’équipe. Le notebook T5 prépare les variables et décrit leurs corrélations ; il ne réalise aucun entraînement ni évaluation de modèle.

La séparation des dates doit également tenir compte des fenêtres cibles. Une observation d’entraînement n’est utilisable que si sa dernière séance cible précède strictement le début du test. Il faut donc purger les lignes d’entraînement qui empiètent sur le test, séparément pour chaque horizon. Un découpage par la seule date t ne suffit pas. La sélection de variables et les transformations estimées doivent aussi se limiter à l’entraînement.

Les anciennes comparaisons LightGBM fondées sur un découpage 80/20 et sur MAE/RMSE ne font pas partie des livrables validés. Aucun gain de 22,8 % n’est retenu. Les essais correspondants et leurs anciennes sorties ont été retirés du notebook.

## 6. Corrélations descriptives recalculées

Corrélations de Pearson sur l’ensemble des lignes conservées, arrondies à trois décimales. Elles incluent la période de test prévue : elles sont descriptives et ne doivent pas servir à sélectionner un modèle hors échantillon.

| Variable | SPX y_h1 | SPX y_h5 | SPX y_h22 | TSX y_h1 | TSX y_h5 | TSX y_h22 |
|---|---:|---:|---:|---:|---:|---:|
| rv_d | 0.581 | 0.649 | 0.535 | 0.531 | 0.633 | 0.501 |
| rv_w | 0.649 | 0.724 | 0.622 | 0.633 | 0.743 | 0.596 |
| rv_m | 0.535 | 0.622 | 0.592 | 0.501 | 0.596 | 0.571 |
| ret | -0.187 | -0.187 | -0.129 | -0.137 | -0.175 | -0.122 |
| ret_neg | -0.427 | -0.446 | -0.365 | -0.344 | -0.410 | -0.331 |
| vix | 0.601 | 0.682 | 0.624 | 0.480 | 0.569 | 0.514 |
| vix_diff | 0.166 | 0.152 | 0.100 | 0.110 | 0.121 | 0.087 |

`rv_w` présente la corrélation la plus élevée avec `y_h5` parmi ces variables dans les deux marchés : 0,724 pour SPX et 0,743 pour TSX. La corrélation de `vix_diff` avec `y_h5` est de 0,152 pour SPX et de 0,121 pour TSX. Ces associations ne mesurent pas une amélioration de prévision hors échantillon.

La corrélation négative de `ret_neg` doit se lire avec son signe : une valeur plus négative, donc une baisse plus forte de l’indice, est associée à une cible plus élevée. Cette observation ne démontre pas à elle seule un effet causal.

## 7. Exécution et contrôles sur les fichiers fournis

| Élément | SPX | TSX |
|---|---:|---:|
| Observations sources | 6 733 | 6 713 |
| Observations conservées | 6 690 | 6 670 |
| Observations retirées | 43 | 43 |
| Première date conservée | 2000-02-03 | 2000-02-03 |
| Dernière date conservée | 2026-09-10 | 2026-09-09 |
| Variables explicatives | 7 | 7 |
| Cibles | 3 | 3 |
| Colonnes numériques hors Date | 10 | 10 |
| Colonnes du CSV avec Date | 11 | 11 |

Les CSV régénérés ne contiennent aucune valeur manquante ni infinie. Les dates sont uniques et croissantes. Les contrôles comparent les sept variables aux calculs attendus et les trois cibles aux moyennes des observations strictement futures, sur toutes les lignes conservées. Un contrôle supplémentaire modifie des valeurs après une date médiane et vérifie que les variables explicatives antérieures ne changent pas. La relecture des CSV exportés reproduit les valeurs des tableaux calculés.

Ces contrôles valident la construction temporelle du notebook sur les fichiers fournis. Ils ne démontrent pas l’absence de révisions des sources ou la disponibilité historique exacte du VIX à l’heure de prévision. Ces éléments relèvent de la qualité et de l’alignement des sources.

## 8. Relancer le notebook

Depuis le dossier `notebooks`, le notebook utilise `../data`. Depuis la racine du dépôt, il utilise `data`. Aucun chemin personnel `/content/spx.csv` n’est imposé.

Dans Colab, si les deux fichiers sources sont absents, le notebook propose leur import et les enregistre dans un dossier `data`. Exécuter les cellules dans l’ordre pour créer les variables, contrôler les calculs, afficher les corrélations et exporter les deux fichiers. La dernière cellule permet de télécharger les CSV depuis Colab.

Les résultats de cette documentation proviennent d’une exécution du notebook corrigé sur les sources fournies. Le SPX a été récupéré dans le tableau `rawLines` complet de la page GitHub HTML transmise, contenant 6 734 lignes dont l’en-tête. Le fichier TSX transmis sous le nom `tsx 2.csv` a été utilisé comme `tsx.csv`, sans changement des données.
