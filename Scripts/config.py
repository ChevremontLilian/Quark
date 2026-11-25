"""
Configuration pour IAM
"""

from pathlib import Path

# Chemins
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = str(PROJECT_ROOT)
DIR = BASE_DIR
MODELS_DIR = str(PROJECT_ROOT / "Models")
DATA_DIR = str(PROJECT_ROOT / "data")

# Modèle
MAIN_MODEL = "Reason"
CORPUS_MAIN = str(Path(DATA_DIR) / "corpus_principal.txt")
CORRECTIONS_FILE = str(Path(DATA_DIR) / "corrections.txt")
MEMORY_FILE = str(Path(DATA_DIR) / "memories.json")
LOG_FILE = str(PROJECT_ROOT / "iam.log")

# Paramètres d'entraînement
TRAINING_PARAMS = {
    "convergence_threshold": 1,
    "patience": 8,
    "batch_size": 8,
    "eval_interval": 250,
    "max_steps": 10000,
    "eval_iterations": 50
}

# Paramètres de l'interface
GUI_SETTINGS = {
    "title": "IAM // Neural Interface",
    "geometry": "1120x1000",
    "min_size": (112, 100),
    "font": ("Cascadia Code", 10),
    "chat_font": ("Cascadia Code", 10),
    "heading_font": ("Bahnschrift", 22, "bold"),
    "button_font": ("Bahnschrift", 10, "bold")
}

# Couleurs
COLORS = {
    "bg": "#09070F",
    "frame": "#110E19",
    "surface": "#171320",
    "input": "#0D0B13",
    "text": "#F2EEF9",
    "muted": "#A69FB5",
    "accent": "#DCCBFF",
    "accent_hover": "#E8DDFF",
    "button": "#171320",
    "button_hover": "#211A2D",
    "button_outline": ("#FFFFFF", "#DCCBFF", "#85818F"),
    "button_outline_disabled": "#514B5B",
    "validate": "#DCCBFF",
    "correct": "#B6AEC5",
    "chat_user": "#DCCBFF",
    "chat_assistant": "#F2EEF9",
    "chat_system": "#A69FB5"
}

