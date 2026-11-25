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
| Tokenizer | SentencePiece BPE, 1 024 pièces demandées |
| Checkpoint configuré | `Models/Reason.pth` |
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
- Fenêtre de contexte : 200 tokens; embedding : 128 dimensions; 4 têtes et
  4 blocs.
- Chaque bloc optimisé combine une attention multi-têtes causale, un MLP à rang
  faible (rang 16), des connexions résiduelles et des LayerNorm.
- Les blocs ajoutent 64 vecteurs de mémoire appris et 4 vecteurs de réflexion
  appris comme préfixe avant l'attention. Ce sont des paramètres appris, pas une
  mémoire de conversation persistante ni une preuve de raisonnement explicite.
- Le dropout configuré est de 0,1. Les gradients sont écrêtés à une norme de
  1,0.

## 2. Données, tokenisation et séquences

### Tokenizer actuellement configuré

`GPT.load_corpus()` entraîne SentencePiece sur le corpus et configure :

- BPE, vocabulaire demandé de 1 024 pièces et couverture des caractères de 1,0;
- IDs spéciaux PAD=0, UNK=1, BOS=2 et EOS=3;
- normalisation SentencePiece par défaut `nmt_nfkc`;
- chaque enregistrement est encodé puis son EOS est ajouté explicitement;
- le padding PAD est ignoré dans la cross-entropy.

Le code vérifie désormais les IDs spéciaux après chargement, encode chaque
séquence d'entraînement sous la forme `BOS + texte + EOS`, utilise BOS au début
du prompt de chat, arrête la génération sur EOS et masque la perte via
`tokenizer.pad_id()`. Un essai temporaire sur le corpus actif a confirmé les
IDs `(0, 1, 2, 3)`, un vocabulaire effectif de 1 024 pièces et une longueur
maximale observée de 189 tokens, marqueurs compris. La segmentation SentencePiece
peut varier avec le tokenizer entraîné.

**Point de vigilance :** le chargement actuel réentraîne le tokenizer et
remplace `tokenizer.model` avant de charger le checkpoint. Même si la taille du
vocabulaire et les IDs spéciaux restent identiques, cela ne prouve pas que
chaque ID représente le même sous-token que lors de l'entraînement du
checkpoint. Une divergence d'indexation est une hypothèse à vérifier quand les
sorties sont incohérentes; elle n'est pas démontrée par la seule présence de
sous-tokens dans une sortie. Pour une expérience reproductible, comparer le
tokenizer exact associé au checkpoint (par exemple empreinte du fichier et
vocabulaire), pas seulement sa taille.

### Construction des lots

Chaque séquence correspond à un enregistrement Q/R. Les questions normalisées
sont gardées dans une seule partition train ou validation pour limiter la
fuite d'exemples presque identiques. Les lots prennent des séquences
indépendantes, les tronquent à la fenêtre de contexte et les complètent avec
PAD. La cible est le token suivant.

Le générateur échantillonne à chaque position avec une softmax complète et
`torch.multinomial`, et s'arrête lorsqu'il produit EOS. Il n'applique
actuellement ni température, ni top-k, ni top-p. Ces paramètres peuvent changer
la lisibilité, mais ne corrigent pas une incompatibilité entre checkpoint et
tokenizer.

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

Les valeurs de référence définies dans `Scripts/config.py` sont notamment :
batch size 8, évaluation toutes les 250 étapes, patience 8, maximum 10 000
updates et 50 lots par estimation. Le taux de base du modèle est `1e-4`.

La boucle utilise désormais :

1. AdamW;
2. un warm-up linéaire de 5 % du nombre d'étapes, plafonné à 500 étapes
   (500 étapes avec la configuration de référence);
3. une décroissance cosinus jusqu'à 10 % du taux de base;
4. un weight decay de `0.05` sur les paramètres de dimension supérieure à 1,
   et `0.0` sur les vecteurs 1D (notamment biais et échelles de normalisation).

Le warm-up est défini en **updates d'optimiseur**, pas en époques. Une étape
signifie un lot traité et une mise à jour des poids.

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

- `load_corpus()` réentraîne le tokenizer; les checkpoints sauvegardent les
  poids du modèle, pas l'état de l'optimiseur ni du scheduler.
- L'estimation train/validation échantillonne des lots; les valeurs ont donc
  du bruit. Le split par groupe est déterministe, mais le sampling des lots ne
  l'est pas nécessairement.
- Le protocole actuel possède un split train/validation, pas un jeu de test
  final distinct.
- Un changement d'architecture peut rendre les anciens checkpoints
  incompatibles. Vérifier les clés et formes d'état et prévoir une migration
  explicite plutôt que masquer les erreurs.
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
