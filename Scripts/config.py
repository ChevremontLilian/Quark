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

# Paramètres du modèle
MODEL_PARAMS = {
    "block_size": 256,
    "embedding_dim": 256,
    "num_heads": 8,
    "num_layers": 4,
    "dropout": 0.1,
    "vocab_size": 2048,
    "learning_rate": 5e-4,
    "memory_size": 64,
    "num_reflection_tokens": 4,
    "loss_on_prompt": False,
}

# Paramètres d'entraînement
TRAINING_PARAMS = {
    "convergence_threshold": 0.1,
    "patience": 6,
    "batch_size": 32,
    "eval_interval": 250,
    "max_steps": 6000,
    "eval_iterations": 20
}

GENERATION_PARAMS = {
    "max_new_tokens": 160,
    "temperature": 0.7,
    "top_k": 40,
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

