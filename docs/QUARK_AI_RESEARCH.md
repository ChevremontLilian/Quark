# Quark — référence IA et journal des changements

Ce document est le point d'entrée commun des agents qui travaillent sur le
modèle Quark. Il réunit l'état observé du dépôt, les notions nécessaires pour
raisonner sur son entraînement et son inférence, et l'historique des
changements ML documentés ici.

## 1. Périmètre et état du projet

Quark est un petit modèle de dialogue français, piloté par l'application locale
IAM. Son architecture et sa boucle d'entraînement sont écrites dans le projet,
mais elles s'appuient sur PyTorch et SentencePiece : « construit de zéro » ne
signifie donc ni framework tensoriel maison, ni entraînement d'un grand modèle
de fondation.

| Domaine | Fait vérifié dans le dépôt |
| --- | --- |
| Entrée de l'application | `python -m Scripts` ou `python Scripts\IAM.py` |
| Orchestration | `Scripts/IAM.py`, classe `ModelManager` |
| Modèle et entraînement | `Scripts/pyAI.py`, classe `GPT` |
| Blocs | `Scripts/TransformerBlock.py`, `OptimizedTransformerBlock` |
| Configuration | `Scripts/config.py` |
| Corpus Q/R actif | `data/corpus_principal.txt` |
| Tokenizer actif | SentencePiece BPE, 1 024 pièces; réentraînement cible 2 048 |
| Checkpoint configuré | `Models/Reason.pth`; ancienne copie `Models/Reason-legacy.pth` |
| Tests | `tests/`, lancés avec `python -m unittest discover -s tests` |

Le corpus actif est composé de lignes `Q: question R: réponse`. Le chargeur
valide et normalise les enregistrements et peut éliminer les doublons stricts.
Les autres jeux de données sous `Models/data` ne sont pas le corpus actif.
Le fichier texte conserve ce format lisible : les marqueurs BOS/EOS sont des
IDs spéciaux ajoutés au moment de créer les séquences du modèle, pas des
chaînes littérales insérées dans les lignes Q/R.

### Architecture observée

- Modèle auto-régressif de type Transformer décodeur; objectif de prédiction du
  prochain token.
- Nouvelle configuration: contexte 256, embedding 256, 8 têtes, 4 blocs,
  dropout 0,1; le tokenizer actuellement présent conserve 1 024 IDs.
- Attention SDPA avec une projection QKV fusionnée et un masque causal booléen.
  Les vecteurs prefix K/V appris sont directement organisés par tête (64
  emplacements mémoire et 4 réflexion); ils ne sont pas concaténés à la
  séquence. Ils ne constituent ni une mémoire de conversation ni une preuve de
  raisonnement explicite.
- MLP standard `d → 4d → d` avec GELU, connexions résiduelles et LayerNorm.
  L'initialisation suit std 0,02 avec mise à l'échelle des projections
  résiduelles; les embeddings d'entrée et la tête de sortie partagent leurs poids.
- Les dimensions changent les clés/formes du checkpoint. `Reason.pth` est
  conservé sans modification et ne se charge pas dans cette architecture; sa
  copie de sauvegarde est `Reason-legacy.pth`.

## 2. Données, tokenisation et séquences

### Tokenizer actuellement configuré

`GPT.load_corpus()` charge `Models/tokenizer.model` sans le réentraîner. Le
réentraînement est une option explicite (`retrain_tokenizer=True`) et requiert
une nouvelle instance GPT afin de ne pas désaligner les poids :

- BPE, modèle présent de 1 024 pièces; un nouveau tokenizer demanderait 2 048
  pièces et utilise `hard_vocab_limit=False`;
- IDs spéciaux PAD=0, UNK=1, BOS=2 et EOS=3;
- normalisation SentencePiece par défaut `nmt_nfkc`;
- prompt d'entraînement et prompt de chat identiques: `BOS + "Q: {q} R:"`;
- réponse encodée avec son espace initial, suivie d'EOS.

La perte ignore le prompt par défaut et utilise `-100` pour le prompt masqué
ainsi que pour PAD. La génération démarre de BOS, interdit PAD/UNK/BOS et
s'arrête sur EOS. Le tokenizer est un artefact séparé du checkpoint : une
égalité de taille ou d'IDs spéciaux ne garantit pas une égalité des associations
ID↔pièce.

### Construction des lots

Chaque séquence correspond à un enregistrement Q/R. Les questions normalisées
sont gardées dans une seule partition train ou validation pour limiter la
fuite d'exemples presque identiques. Les séquences sont tokenisées et paddées
une fois sur le périphérique; les indices sont groupés par longueur et chaque
lot est coupé à sa longueur maximale effective. Les positions PAD ne participent
pas à la perte. Les lignes invalides sont ignorées avec un avertissement et le
bruit connu (`mentirondelic` et gabarits exacts) est compté et filtré. Le
corpus source n'est pas modifié; `python -m Scripts.corpus_audit` liste les
candidats suspects et les questions ayant de nombreuses variantes.

Le générateur utilise `eval()` et `no_grad()`, une température par défaut 0,7,
top-k 40 et un maximum par défaut de 160 tokens. Il restaure le mode du modèle
après génération. La sortie du chat ne contient que la réponse et n'est pas
coupée au caractère `!`.

## 3. Notions ML utiles au diagnostic

### Objectif et familles d'apprentissage

- **Apprentissage supervisé :** apprendre à partir d'exemples et de cibles
  fournies; la relation Q/R du corpus sert ici à apprendre des continuations.
- **Auto-supervision :** fabriquer une cible à partir des données elles-mêmes.
  Ici, un extrait de tokens est l'entrée et le token suivant est la cible.
- **Fonction de perte :** mesure numérique de l'écart entre logits et cibles.
  Une baisse de cross-entropy indique une meilleure prédiction moyenne sur les
  tokens évalués; elle ne garantit pas une réponse utile ou vraie.
- **Optimisation :** calculer les gradients de la perte et mettre à jour les
  paramètres. AdamW adapte les mises à jour par paramètre et applique un
  weight decay découplé.
- **Généralisation :** capacité à réussir sur des questions non vues. La perte
  train seule ne la mesure pas; il faut comparer train et validation sans
  fuite.

### Tokenizer et représentations

Un tokenizer sous-mots découpe le texte en unités réutilisables. Les IDs sont
des indices, pas des mots ni des valeurs numériques avec un ordre sémantique.
Les embeddings apprennent un vecteur par ID. Le vocabulaire, les IDs spéciaux
et l'association ID↔pièce doivent rester alignés entre corpus, embeddings et
checkpoint.

Les limites de vocabulaire, la normalisation, les espaces et les marqueurs
`Q:`/`R:` changent les séquences apprises. Une sortie en sous-mots n'est pas
automatiquement un défaut : inspecter les IDs et leur décodage, les pièces
UNK/EOS/PAD et la correspondance avec le tokenizer du checkpoint avant de
modifier la taille du vocabulaire.

### Transformer décodeur

- L'attention causale permet à une position de consulter le passé, pas le futur.
- Les têtes parallèles apprennent différents motifs d'attention; leurs sorties
  sont réunies puis projetées.
- Le MLP transforme chaque position; les connexions résiduelles et
  normalisations facilitent l'optimisation.
- Les embeddings positionnels donnent une information d'ordre; la fenêtre de
  contexte limite la quantité d'historique visible.
- Des vecteurs appris appelés « mémoire » ou « réflexion » ne fournissent pas,
  par leur seul nom, une mémoire dynamique, un outil externe, ou une capacité
  cognitive garantie.

### Optimisation et régularisation dans Quark

Les valeurs de départ définies dans `Scripts/config.py` sont : batch size 32,
évaluation toutes les 250 étapes, patience 6, maximum 6 000 updates,
20 lots d'évaluation et taux d'apprentissage `5e-4`. Le seuil de convergence
est 0,1; les deux dictionnaires `MODEL_PARAMS` et `TRAINING_PARAMS` centralisent
ces valeurs.

La boucle utilise :

1. AdamW avec betas `(0.9, 0.95)` et `fused=True` sur CUDA;
2. un warm-up linéaire de 5 % du nombre d'étapes, plafonné à 500 étapes
   (300 étapes pour 6 000 updates);
3. une décroissance cosinus jusqu'à 10 % du taux de base;
4. un weight decay de `0.05` sur les matrices seulement; biais, LayerNorm et
   préfixes K/V sont exclus;
5. autocast bf16 sur CUDA quand le périphérique le prend en charge.

Le warm-up est défini en **updates d'optimiseur**, pas en époques. Une étape
signifie un lot traité et une mise à jour des poids.

La boucle conserve/restaure le meilleur état évalué, sauvegarde atomiquement
par fichier temporaire puis `os.replace`, et ne sauvegarde pas les poids
courants moins bons lors d'un arrêt ou d'une exception. Une perte non finie
déclenche une erreur explicite. Le journal d'évaluation rapporte aussi les
tokens/s observés.

## 4. Lire les symptômes sans tirer de conclusions hâtives

| Observation | Vérifications utiles avant d'agir |
| --- | --- |
| Train et validation stagnent ensemble | Taux réellement appliqué, gradients, lots/cibles, données, tokenisation, capacité du modèle et courbe par étape. |
| Train baisse mais validation stagne ou monte | Surapprentissage possible; contrôler la séparation par question, les doublons, la régularisation et la taille/qualité des données. |
| Loss instable ou non finie | Vérifier les logits/pertes/gradients non finis, le taux effectif, les IDs hors vocabulaire et les lots; ne pas augmenter arbitrairement le taux. |
| Sorties en pièces incohérentes | Comparer le tokenizer exact du checkpoint, encoder puis décoder des exemples connus, compter UNK, contrôler EOS/PAD et examiner la distribution des logits. |
| Sortie trop aléatoire | Inspecter la température et les stratégies d'échantillonnage; confirmer auparavant l'alignement tokenizer/checkpoint et la qualité du modèle. |
| Sortie répétitive ou coupée | Vérifier données, EOS et procédure d'arrêt; mesurer répétitions et longueur, puis tester le décodage séparément de l'entraînement. |

Ce tableau propose des expériences, pas des causes établies. Une seule
observation (par exemple une loss plate ou des sous-tokens visibles) ne permet
pas d'identifier le défaut.

## 5. Méthode de recherche et d'ingénierie

Pour tout changement d'entraînement ou d'architecture :

1. **Établir les faits :** localiser les producteurs de données, les appels,
   valeurs effectives, checkpoints et tests. Distinguer observation,
   hypothèse et interprétation.
2. **Formuler une hypothèse falsifiable :** nommer un mécanisme et le signal
   qui devrait changer si l'hypothèse est correcte.
3. **Protéger une référence :** conserver les mêmes corpus, split, seed,
   tokenizer, nombre de tokens vus, batch et protocole d'évaluation lorsque
   l'on compare deux réglages.
4. **Isoler une variable :** changer un paramètre à la fois; enregistrer sa
   valeur et la courbe train/validation. Répéter avec plusieurs seeds avant de
   généraliser si le bruit de mesure est important.
5. **Évaluer le comportement :** compléter la loss par des exemples tenus à
   l'écart, exactitude/qualité adaptées à la tâche, taux de répétition, taux
   UNK et inspection humaine structurée. Ne jamais présenter la loss comme une
   mesure complète d'intelligence.
6. **Vérifier le résultat :** lancer les tests ciblés, mesurer le critère
   annoncé, signaler les limites et ne pas annoncer un gain sans comparaison
   contrôlée.

Pour comparer des modèles, contrôler notamment le nombre de tokens traités,
le split, la version du tokenizer, le budget de calcul, le protocole de
génération et les seeds. Une variation simultanée de ces facteurs rend
l'attribution causale incertaine.

### Reproductibilité et limites actuelles

- `load_corpus()` ne réentraîne pas le tokenizer par défaut; les checkpoints
  sauvegardent les poids du modèle, pas le tokenizer ni l'état de l'optimiseur
  et du scheduler.
- L'estimation train/validation échantillonne des lots; les valeurs ont donc
  du bruit. Le split par groupe est déterministe, mais le sampling des lots et
  leur bucketing ne l'est pas nécessairement.
- Le protocole actuel possède un split train/validation, pas un jeu de test
  final distinct.
- La loss réponse-seule n'est pas directement comparable à la loss historique
  qui inclut le prompt.
- Les checkpoints de l'ancienne architecture sont incompatibles avec les
  nouvelles formes; le chargement les signale et l'entraînement depuis zéro
  reste disponible. L'ancien fichier est archivé, pas supprimé.
- Les paramètres du modèle, tokenizer, corpus, seeds, versions logicielles,
  durée et nombre de tokens vus sont des métadonnées à conserver pour des
  comparaisons solides.

## 6. Historique des changements documentés

### 2026-11-25 — stabilisation de l'entraînement et vérification tokenizer

- Ajout d'un scheduler warm-up linéaire puis cosinus, avec plancher de LR à
  10 % du taux de base.
- Passage du weight decay de `0.01` à `0.05` pour les poids de matrices;
  exclusion des paramètres 1D, dont biais et échelles de normalisation.
- AdamW était déjà l'optimiseur; il est conservé et le logging de configuration
  précise maintenant optimizer, weight decay et nombre d'étapes warm-up.
- Vérification explicite des IDs PAD/UNK/BOS/EOS; EOS et PAD sont lus depuis le
  tokenizer au lieu de dupliquer leurs valeurs numériques dans la boucle.
- Ajout de tests ciblés sur la rampe warm-up, la décroissance et le cas d'une
  seule étape. Validation exécutée : `python -m unittest discover -s tests`
  (7 tests réussis).
- Vérification sur le corpus actif dans un répertoire temporaire : tokenizer
  BPE de 1 024 pièces et IDs `(0, 1, 2, 3)`. Aucun tokenizer produit lors de
  cette vérification n'a été conservé dans le dépôt.
- Ajout de BOS avant chaque séquence d'entraînement et à chaque prompt de
  génération, conservation d'EOS après chaque exemple et arrêt de la génération
  lorsqu'EOS est produit. Le fichier Q/R brut conserve son format; les marqueurs
  sont des IDs spéciaux, pas des chaînes ordinaires.
- Ajout de tests sur les frontières BOS/EOS des séquences et sur l'arrêt de
  génération.
- Ajout de cette référence IA et de son historique dans
  `docs/QUARK_AI_RESEARCH.md`, ainsi que du skill
  `.github/skills/quark-ai-research/SKILL.md`, qui impose la lecture du guide
  avant tout travail IA sur Quark.
- Ajout de liens vers le guide et le skill dans le `README.md` racine.

### 2026-11-26 — refonte du pipeline Q/R et essais courts

- Le pipeline utilise maintenant des préfixes K/V appris, l'attention SDPA,
  un MLP `d → 4d → d`, des poids liés et une initialisation GPT-2-like.
  L'entraînement charge le tokenizer existant par défaut, masque le prompt et
  PAD de la perte, groupe le split par question et restaure le meilleur état.
- L'API d'entraînement est `fit()`; l'API `nn.Module.train()` reste disponible.
  Le chat partage le prompt d'entraînement, génère la réponse seule et utilise
  `eval()` / `no_grad()`. L'UI signale les checkpoints incompatibles et peut
  lancer un entraînement depuis zéro.
- Le checkpoint préexistant a été conservé; sa copie `Reason-legacy.pth`
  possède le même SHA-256. Un chargement dans la nouvelle architecture échoue
  explicitement avec un message d'incompatibilité, sans modifier l'original.
- Mesures exploratoires sur NVIDIA RTX 4050 Laptop, PyTorch 2.15.0+cu134,
  autocast bf16, corpus Q/R actif et split groupé. Les nouveaux essais ont
  utilisé le seed 41, 100 updates et 20 lots d'évaluation. Les pertes sont des
  pertes moyennes échantillonnées sur les tokens de réponse; `tokens vus`
  exclut le padding.

| Variante | Vocab. | Batch | LR | Tokens vus | Train loss | Val réponse | Tokens/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline avant refonte (seed 42) | 1 024 | 8 | 1e-4 | non relevé | 6,3536 | 6,2974* | 32 464 |
| Refonte, anciens hyperparamètres | 1 024 | 8 | 1e-4 | 31 157 | 6,3934 | 6,4006 | 16 307 |
| Nouveau modèle, LR 3e-4 | 2 048 | 32 | 3e-4 | 105 126 | 5,5088 | 5,6001 | 74 187 |
| Nouveau modèle, LR 5e-4 | 2 048 | 32 | 5e-4 | 105 126 | 5,3349 | 5,4315 | 20 862 |
| Nouveau modèle, LR 1e-3 | 2 048 | 32 | 1e-3 | 105 126 | 5,1663 | 5,2675 | 17 417 |
| Ablation mémoire K/V désactivée | 2 048 | 32 | 5e-4 | 102 874 | 5,3756 | 5,6360 | 15 041 |
| Vocabulaire 1 024, budget rapproché | 1 024 | 29 | 5e-4 | 103 835 | 4,8835 | 4,9373 | 75 850 |

`*` La baseline historique apprend aussi le prompt; sa loss de validation
n'est donc pas comparable à la loss réponse-seule ci-dessus. L'ablation mémoire
conserve batch et nombre d'updates, mais les lots aléatoires donnent un budget
de tokens inférieur de 2,1 %. L'essai 1 024/2 048 rapproche le budget à 1,2 %
près en ajustant le batch; la taille de batch n'est donc pas strictement
identique. Les pertes sur des vocabulaires différents ne mesurent pas la même
segmentation token.

- Les valeurs train/validation de chaque run sont des mesures courtes,
  mono-seed, pas des évaluations de qualité généralisable. Les tokens/s
  observés ont varié fortement entre exécutions sur la même machine; aucune
  accélération n'est revendiquée sans répétitions synchronisées et GPU au
  repos. Aucun entraînement long ni jeu de test distinct n'a été exécuté.
- `python -m unittest discover -s tests` : 19 tests réussis. `git diff --check`
  passe également. Un test confirme que `loss_on_prompt=False` surcharge bien
  le défaut du modèle; cette précision évite de réinclure le prompt par erreur.

## 7. Glossaire rapide

| Terme | Sens pratique |
| --- | --- |
| Token / sous-token | Unité discrète produite par le tokenizer. |
| Logit | Score brut du modèle pour chacun des IDs du vocabulaire. |
| Cross-entropy | Perte de prédiction de la cible token suivante. |
| Epoch | Un passage complet sur un jeu de données; distinct d'un update. |
| Update / step | Une mise à jour des paramètres après rétropropagation. |
| Learning rate | Taille des mises à jour induites par les gradients. |
| Warm-up | Montée progressive du learning rate au début de l'entraînement. |
| Cosine decay | Diminution du learning rate suivant une courbe cosinus. |
| Weight decay | Régularisation appliquée aux paramètres par l'optimiseur. |
| Overfit | Bonne performance sur les données vues, généralisation faible. |
| Leakage | Information du jeu d'évaluation qui fuit dans l'entraînement. |
| Checkpoint | État sauvegardé des poids (et, si prévu, de l'entraînement). |
| Inference | Utilisation du modèle entraîné sans mise à jour de ses poids. |
