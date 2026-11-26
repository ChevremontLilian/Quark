# IAM

IAM est une application locale Tkinter qui entraîne un petit modèle de dialogue
sur un corpus français Q/R. Les chemins sont calculés depuis le projet, et le
package `Scripts` conserve aussi le lancement historique par script.

## Installation et lancement

Python 3.10 ou plus récent est requis. À la racine du projet :

```powershell
python -m pip install -e .
python -m Scripts
```

Le lancement direct reste compatible :

```powershell
python Scripts\IAM.py
```

## Organisation

```text
Scripts/
  IAM.py               Interface et orchestration
  config.py            Chemins et paramètres du projet
  corpus.py            Validation, nettoyage et découpage du corpus
  memories.py          Persistance des mémoires
  pyAI.py              Modèle et boucle d'entraînement
  TransformerBlock.py  Couches Transformer
  __main__.py          Point d'entrée python -m Scripts
Models/
  Reason.pth           Checkpoint du modèle
  tokenizer.model      Tokenizer SentencePiece
data/
  corpus_principal.txt Corpus Q/R actif (source unique)
  corrections.txt      Historique des corrections
  memories.json        Mémoires locales, créé à la demande
tests/
  test_corpus.py          Tests du parsing et du découpage sans fuite
  test_training_schedule.py Tests du scheduler de learning rate
  test_token_boundaries.py  Tests des tokens BOS/EOS
```

Les anciennes copies sous `Models\data` ne sont pas lues par l'application.
`Models\dataCreation.py` produit désormais ses jeux expérimentaux sous
`data\generated` et ne remplace pas le corpus actif.

## Corpus et apprentissage

Chaque exemple actif tient sur une ligne :

```text
Q: Question R: Réponse
```

Vérifier le corpus sans le modifier :

```powershell
python -m Scripts.corpus
```

Normaliser les espaces, enlever les lignes vides et dédupliquer uniquement les
paires question/réponse strictement identiques :

```powershell
python -m Scripts.corpus --clean
```

Les réponses alternatives à une même question sont conservées. Pendant
l'entraînement, toutes les variantes d'une question normalisée sont placées
dans la même partition train ou validation afin d'éviter une fuite entre les
deux jeux.

Le tokenizer `Models/tokenizer.model` est réutilisé sans réentraînement au
chargement. Un réentraînement doit être demandé explicitement avec
`load_corpus(..., retrain_tokenizer=True)` sur une nouvelle instance GPT, car
ses IDs font partie du contrat du checkpoint. La séquence d'apprentissage
commence par BOS et le préfixe exact `Q: {question} R:`; la perte porte par
défaut sur la réponse et EOS, pas sur le prompt. `GPT.fit(...)` entraîne le
modèle sans masquer `nn.Module.train()`; le chat reçoit la question brute et
renvoie uniquement la réponse.

Les exemples du corpus ne sont pas réécrits automatiquement au lancement de
l'application. Les corrections validées sont ajoutées au corpus actif par
l'interface et nécessitent un ré-entraînement pour être apprises. Les poids du
meilleur checkpoint sont sauvegardés atomiquement et restaurés après
l'entraînement ou son arrêt.

Auditer les lignes potentiellement suspectes et les questions ayant de
nombreuses réponses distinctes, sans modifier le corpus :

```powershell
python -m Scripts.corpus_audit
```

Le checkpoint existant `Models/Reason.pth` utilise l'ancienne architecture.
Il n'est pas chargé par la nouvelle architecture; sa copie est conservée sous
`Models/Reason-legacy.pth` avant tout entraînement depuis zéro.

## Vérifications

```powershell
python -m unittest discover -s tests
```

## Documentation IA et agents

- [Référence IA Quark et journal des changements](docs/QUARK_AI_RESEARCH.md)
- [Skill Copilot pour les travaux IA sur Quark](.github/skills/quark-ai-research/SKILL.md)
