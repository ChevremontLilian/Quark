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

Les exemples du corpus ne sont pas réécrits automatiquement au lancement de
l'application. Les corrections validées sont ajoutées au corpus actif par
l'interface.

## Vérifications

```powershell
python -m unittest discover -s tests
```

## Documentation IA et agents

- [Référence IA Quark et journal des changements](docs/QUARK_AI_RESEARCH.md)
- [Skill Copilot pour les travaux IA sur Quark](.github/skills/quark-ai-research/SKILL.md)
