#!/usr/bin/env python3
"""
IAM - Interface d'Apprentissage Machine
Version optimisée avec interface graphique et système de feedback
"""

import os
import sys
import time
import inspect
import threading
import queue
import logging
import shutil
from math import cos, radians, sin
import tkinter as tk
from tkinter import ttk, scrolledtext, Scrollbar,messagebox, font as tkfont
import torch
import psutil
import pyttsx3

# ============================================================================
# CONFIGURATION
# ============================================================================
if __package__:
    from .config import (
        MODELS_DIR, DATA_DIR, MAIN_MODEL, CORPUS_MAIN,
        TRAINING_PARAMS, GUI_SETTINGS, COLORS, CORRECTIONS_FILE, LOG_FILE
    )
    from .corpus import append_qa_record, normalize_text
else:
    from config import (
        MODELS_DIR, DATA_DIR, MAIN_MODEL, CORPUS_MAIN,
        TRAINING_PARAMS, GUI_SETTINGS, COLORS, CORRECTIONS_FILE, LOG_FILE
    )
    from corpus import append_qa_record, normalize_text


# Vérifier que les dossiers existent
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Configurer le logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# IMPORTS DYNAMIQUES (chargement différé)
# ============================================================================

# Ces imports seront chargés uniquement quand nécessaire
_AI_MODULE = None
_MEMOIRES_MODULE = None


def get_AI():
    """Charge le module pyAI de manière différée"""
    global _AI_MODULE
    if _AI_MODULE is None:
        try:
            if __package__:
                from . import pyAI as AI
            else:
                import pyAI as AI
            _AI_MODULE = AI
        except ImportError as e:
            messagebox.showerror("Erreur", f"Impossible de charger pyAI: {e}")
            sys.exit(1)
    return _AI_MODULE


def get_memories():
    """Charge le module memories de manière différée"""
    global _MEMOIRES_MODULE
    if _MEMOIRES_MODULE is None:
        try:
            if __package__:
                from . import memories
            else:
                import memories
            _MEMOIRES_MODULE = memories
        except ImportError:
            # Si memories n'est pas disponible, on utilise une implémentation basique
            _MEMOIRES_MODULE = type('MockMemories', (), {
                'Memory': type('MockMemory', (), {
                    'get_memory': lambda self, key: f"Mémoire non disponible pour: {key}",
                    'set_memory': lambda self, key, value: f"Mémoire enregistrée: {key}={value}",
                    'delete_memory': lambda self, key: f"Mémoire supprimée: {key}"
                })()
            })()
    return _MEMOIRES_MODULE


class RoundedButton(tk.Canvas):
    """Bouton arrondi avec contour dégradé dessiné sur un canevas."""

    def __init__(
        self, master, text, command, font, parent_background,
        background, hover_background, foreground="white",
        state=tk.NORMAL, height=38
    ):
        self._command = command
        self._font = tkfont.Font(master=master, font=font)
        self._background = background
        self._hover_background = hover_background
        self._foreground = foreground
        self._outline_colors = COLORS.get(
            "button_outline", ("#FFFFFF", "#DCCBFF", "#85818F")
        )
        self._disabled_outline = COLORS.get("button_outline_disabled", "#514B5B")
        self._disabled = state == tk.DISABLED
        self._hovered = False
        width = self._font.measure(text) + 42

        super().__init__(
            master,
            width=width,
            height=height,
            background=parent_background,
            borderwidth=0,
            highlightthickness=0,
            takefocus=True,
            cursor="" if self._disabled else "hand2",
        )
        self._shape = self._draw_rounded_shape(width, height)
        self._outline_items = self._draw_gradient_outline(width, height)
        self._label = self.create_text(
            width / 2, height / 2,
            text=text,
            font=self._font,
            fill=self._foreground,
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<space>", self._on_key)
        self.bind("<Return>", self._on_key)
        self._update_appearance()

    def _draw_rounded_shape(self, width, height):
        inset = 2
        radius = (height - inset * 2) / 2
        points = []
        for center_x, center_y, start_angle in (
            (width - inset - radius, inset + radius, -90),
            (width - inset - radius, height - inset - radius, 0),
            (inset + radius, height - inset - radius, 90),
            (inset + radius, inset + radius, 180),
        ):
            for step in range(7):
                angle = start_angle + step * 15
                points.extend((
                    center_x + radius * cos(radians(angle)),
                    center_y + radius * sin(radians(angle)),
                ))
        return self.create_polygon(
            points, smooth=True, splinesteps=12, outline="", tags="button"
        )

    def _outline_color(self, progress):
        stops = self._outline_colors
        segment_position = progress * (len(stops) - 1)
        segment = min(int(segment_position), len(stops) - 2)
        amount = segment_position - segment
        start = tuple(int(stops[segment][index:index + 2], 16) for index in (1, 3, 5))
        end = tuple(int(stops[segment + 1][index:index + 2], 16) for index in (1, 3, 5))
        channels = tuple(round(a + (b - a) * amount) for a, b in zip(start, end))
        return f"#{channels[0]:02X}{channels[1]:02X}{channels[2]:02X}"

    def _draw_gradient_outline(self, width, height):
        inset = 2
        radius = (height - inset * 2) / 2
        points = []
        for center_x, center_y, start_angle in (
            (width - inset - radius, inset + radius, -90),
            (width - inset - radius, height - inset - radius, 0),
            (inset + radius, height - inset - radius, 90),
            (inset + radius, inset + radius, 180),
        ):
            for step in range(7):
                angle = start_angle + step * 15
                points.append((
                    center_x + radius * cos(radians(angle)),
                    center_y + radius * sin(radians(angle)),
                ))

        top_left = points[-1]
        top_right = points[0]
        points.extend(
            (
                top_left[0] + (top_right[0] - top_left[0]) * step / 8,
                top_left[1] + (top_right[1] - top_left[1]) * step / 8,
            )
            for step in range(1, 8)
        )
        points.append(points[0])

        outline_items = []
        segment_count = len(points) - 1
        for index, (start, end) in enumerate(zip(points, points[1:])):
            outline_items.append(self.create_line(
                *start, *end,
                fill=self._outline_color(index / segment_count),
                width=2,
                capstyle=tk.ROUND,
                tags="button-outline",
            ))
        return outline_items

    def _update_appearance(self):
        fill = self._background
        if self._disabled:
            fill = "#555555"
        elif self._hovered:
            fill = self._hover_background
        self.itemconfigure(self._shape, fill=fill)
        self.itemconfigure(
            self._label,
            fill=self._disabled_outline if self._disabled else self._foreground,
        )
        for index, item in enumerate(self._outline_items):
            self.itemconfigure(
                item,
                fill=self._disabled_outline if self._disabled else self._outline_color(
                    index / len(self._outline_items)
                ),
                width=3 if self._hovered and not self._disabled else 2,
            )
        self.configure(cursor="" if self._disabled else "hand2")

    def set_state(self, state):
        self._disabled = state == tk.DISABLED
        self._update_appearance()

    def _on_enter(self, _event):
        self._hovered = True
        self._update_appearance()

    def _on_leave(self, _event):
        self._hovered = False
        self._update_appearance()

    def _on_click(self, _event):
        if not self._disabled:
            self._command()

    def _on_key(self, _event):
        if not self._disabled:
            self._command()
            return "break"


# ============================================================================
# GESTION DU MODÈLE
# ============================================================================

class ModelManager:
    """Gère le chargement, l'entraînement et l'utilisation du modèle"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.is_training = False
        self.training_error = None
        self.training_stopped = False
        self.training_supports_stop = False
        self.training_thread = None
        self.message_queue = queue.Queue()
        self.stop_training_event = threading.Event()
        self.load_error = None
        
        # Initialiser le modèle
        self._init_model()
    
    def _init_model(self):
        """Initialise le modèle GPT"""
        try:
            AI = get_AI()
            self.model = AI.GPT(MODELS_DIR, self.device)
            print(f"Modèle initialisé sur: {self.device.type}")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du modèle: {e}")
            messagebox.showerror("Erreur", f"Impossible d'initialiser le modèle: {e}")
    
    def load_model(self):
        """Charge le modèle et le corpus"""
        if self.model is None:
            self._init_model()
        
        try:
            self.model.load_corpus(CORPUS_MAIN)
            self.model.load_model(MAIN_MODEL)
            self.load_error = None
            return True
        except Exception as e:
            self.load_error = str(e)
            print(f"Erreur lors du chargement du modèle: {e}")
            return False
    
    def train_model(self, on_progress=None,removeOldmodel=True):
        """Entraîne le modèle sans supprimer le checkpoint précédent."""
        if self.is_training:
            raise RuntimeError("Un entraînement est déjà en cours.")
        if self.model is None:
            raise RuntimeError("Le modèle GPT n'a pas pu être initialisé.")

        self.stop_training_event.clear()
        self.training_error = None
        self.training_stopped = False
        self.training_supports_stop = False
        train_method = self.model.fit
        try:
            train_parameters = inspect.signature(train_method).parameters
        except (TypeError, ValueError, OSError) as error:
            train_parameters = {}
            logging.warning("Impossible d'inspecter GPT.fit: %s", error)
        accepts_extra_keywords = any(
            parameter.kind is inspect.Parameter.VAR_KEYWORD
            for parameter in train_parameters.values()
        )
        self.training_supports_stop = (
            "stop_event" in train_parameters or accepts_extra_keywords
        )
        self.is_training = True
        
        def _train():
            try:
                checkpoint_path = os.path.join(MODELS_DIR, f"{MAIN_MODEL}.pth")
                if on_progress:
                    on_progress("Chargement du corpus...")
                self.model.load_corpus(CORPUS_MAIN)

                def archive_checkpoint():
                    if not os.path.isfile(checkpoint_path):
                        return None
                    legacy_path = os.path.join(
                        MODELS_DIR, f"{MAIN_MODEL}-legacy.pth"
                    )
                    if os.path.exists(legacy_path):
                        legacy_path = os.path.join(
                            MODELS_DIR,
                            f"{MAIN_MODEL}-legacy-{time.strftime('%Y%m%d-%H%M%S')}.pth",
                        )
                    shutil.copy2(checkpoint_path, legacy_path)
                    return legacy_path

                if removeOldmodel:
                    archived_path = archive_checkpoint()
                    self.model.reset_parameters()
                    self.model.loaded_model = MAIN_MODEL
                    if archived_path and on_progress:
                        on_progress(f"Ancien checkpoint conservé sous {archived_path}")
                else:
                    try:
                        self.model.load_model(MAIN_MODEL)
                    except (FileNotFoundError, RuntimeError) as error:
                        archived_path = archive_checkpoint()
                        self.model.reset_parameters()
                        self.model.loaded_model = MAIN_MODEL
                        message = (
                            "Checkpoint absent ou incompatible; entraînement depuis zéro."
                        )
                        if archived_path:
                            message += f" Copie conservée sous {archived_path}."
                        logging.warning("%s Cause: %s", message, error)
                        if on_progress:
                            on_progress(message)
                
                if on_progress:
                    on_progress("Entraînement en cours...")
                
                train_options = {}

                if "on_progress" in train_parameters or accepts_extra_keywords:
                    train_options["on_progress"] = on_progress
                else:
                    model_module = sys.modules.get(type(self.model).__module__)
                    model_path = getattr(model_module, "__file__", "module non résolu")
                    logging.warning(
                        "Le moteur GPT chargé (%s) ne prend pas en charge on_progress; "
                        "redémarrez l'application pour charger la version à jour.",
                        model_path
                    )
                    if on_progress:
                        on_progress(
                            "Entraînement en cours — progression détaillée indisponible "
                            "(redémarrez l'application pour la réactiver)"
                        )

                if self.training_supports_stop:
                    train_options["stop_event"] = self.stop_training_event

                self.training_stopped = self.model.fit(
                    **TRAINING_PARAMS, **train_options
                )
                
            except Exception as e:
                self.training_error = str(e)
                self.message_queue.put(f"Erreur lors de l'entraînement: {e}")
                logging.exception("Erreur lors de l'entraînement")
            finally:
                self.is_training = False
        
        self.training_thread = threading.Thread(target=_train, daemon=True)
        try:
            self.training_thread.start()
        except Exception:
            self.is_training = False
            raise
    
    def stop_training(self):
        """Arrête l'entraînement en cours"""
        if self.is_training and self.training_supports_stop:
            self.stop_training_event.set()
            return True
        return False
    
    def chat(self, question):
        """Pose une question au modèle et retourne la réponse"""
        if self.model is None or self.is_training:
            return "Modèle non chargé ou entraînement en cours..."
        
        try:
            return self.model.chat(question)
        except Exception as e:
            print(f"Erreur lors du chat: {e}")
            return f"Erreur: {e}"
    
    def add_to_corpus(self, question, answer):
        """Ajoute une nouvelle question/réponse au corpus et au fichier de corrections"""
        try:
            question = normalize_text(question)
            answer = normalize_text(answer)

            # Ajouter au corpus principal
            append_qa_record(CORPUS_MAIN, question, answer)
            
            # Sauvegarder aussi dans le fichier de corrections
            with open(CORRECTIONS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Q: {question} R: {answer}\n")
            
            logging.info(f"Ajout au corpus: Q: {question} R: {answer}")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout au corpus: {e}")
            return False


# ============================================================================
# GESTION DE LA MÉMOIRE
# ============================================================================

class MemoryManager:
    """Gère les opérations de mémoire"""
    
    def __init__(self):
        self.memories = get_memories()
    
    def get_memory(self, key):
        """Récupère une mémoire"""
        try:
            return self.memories.Memory().get_memory(key)
        except Exception as e:
            return f"Erreur: {e}"
    
    def set_memory(self, key, value):
        """Enregistre une mémoire"""
        try:
            return self.memories.Memory().set_memory(key, value)
        except Exception as e:
            return f"Erreur: {e}"
    
    def delete_memory(self, key):
        """Supprime une mémoire"""
        try:
            return self.memories.Memory().delete_memory(key)
        except Exception as e:
            return f"Erreur: {e}"


# ============================================================================
# GESTION SYSTÈME
# ============================================================================

class SystemMonitor:
    """Surveille l'utilisation du CPU et de la RAM"""
    
    @staticmethod
    def get_status():
        """Récupère l'utilisation actuelle du CPU et de la RAM"""
        try:
            ram = psutil.virtual_memory()
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage_percent = ram.percent
            ram_used_gb = round(ram.used / 1e9, 2)
            return f"CPU: {cpu_usage}% | RAM: {ram_usage_percent}% ({ram_used_gb} Go)"
        except Exception as e:
            return f"Erreur: {e}"


# ============================================================================
# SYNTHÈSE VOCALE
# ============================================================================

class VoiceSynthesizer:
    """Gère la synthèse vocale"""
    
    def __init__(self):
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialise le moteur de synthèse vocale"""
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            print(f"Impossible d'initialiser la synthèse vocale: {e}")
            self.engine = None
    
    def say(self, text):
        """Lit un texte à voix haute"""
        if self.engine is None:
            return
        try:
            self._init_engine()
            self.engine.say(str(text))
            self.engine.runAndWait()
        except Exception as e:
            print(f"Erreur lors de la synthèse vocale: {e}")


# ============================================================================
# INTERFACE GRAPHIQUE
# ============================================================================

class IAMGUI:
    """Interface graphique principale"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_SETTINGS.get('title', 'IAM // Neural Interface'))
        self.root.geometry(GUI_SETTINGS.get('geometry', '1120x780'))
        min_size = GUI_SETTINGS.get('min_size', (800, 600))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        available_width = max(320, screen_width - 40)
        available_height = max(300, screen_height - 80)
        minimum_width = min(max(min_size[0], 480), available_width)
        minimum_height = min(max(min_size[1], 560), available_height)
        self.root.minsize(minimum_width, minimum_height)
        self.root.update_idletasks()
        self.root.geometry(
            f"{min(self.root.winfo_width(), available_width)}x"
            f"{min(self.root.winfo_height(), available_height)}"
        )
        
        # Configuration du thème
        self.configure_style()
        
        # Initialisation des managers
        self.model_manager = ModelManager()
        self.memory_manager = MemoryManager()
        self.voice = VoiceSynthesizer()
        self.system_monitor = SystemMonitor()
        
        # Variables
        self.is_training = False
        self.model_loaded = False
        self.training_progress_queue = queue.Queue()
        
        # Création de l'interface
        self.create_widgets()
        
        # Charger le modèle au démarrage
        self.load_model()
    
    def configure_style(self):
        """Configure le thème sombre violet de l'interface."""
        style = ttk.Style()
        style.theme_use('clam')

        bg_color = COLORS.get('bg', '#09070F')
        frame_color = COLORS.get('frame', '#110E19')
        surface_color = COLORS.get('surface', '#171320')
        input_color = COLORS.get('input', '#0D0B13')
        text_color = COLORS.get('text', '#F2EEF9')
        muted_color = COLORS.get('muted', '#A69FB5')
        accent_color = COLORS.get('accent', '#DCCBFF')

        self.root.configure(bg=bg_color)

        style.configure('TFrame', background=frame_color)
        style.configure('TLabel', background=frame_color, foreground=text_color)
        style.configure('Card.TFrame', background=surface_color)
        style.configure(
            'Header.TLabel',
            background=surface_color,
            foreground=text_color,
            font=GUI_SETTINGS.get('heading_font', ('Bahnschrift', 22, 'bold')),
        )
        style.configure(
            'Eyebrow.TLabel',
            background=surface_color,
            foreground=accent_color,
            font=('Cascadia Code', 9, 'bold'),
        )
        style.configure(
            'Muted.TLabel',
            background=surface_color,
            foreground=muted_color,
            font=GUI_SETTINGS.get('font', ('Cascadia Code', 10)),
        )
        style.configure(
            'Status.TLabel',
            background=surface_color,
            foreground=accent_color,
            font=('Cascadia Code', 10, 'bold'),
            padding=(10, 8),
        )
        style.configure(
            'System.TLabel',
            background=surface_color,
            foreground=muted_color,
            font=('Cascadia Code', 9),
            padding=(10, 8),
        )
        style.configure(
            'TEntry',
            fieldbackground=input_color,
            foreground=text_color,
            bordercolor=COLORS.get('muted', '#A69FB5'),
            lightcolor=surface_color,
            darkcolor=surface_color,
            padding=(10, 8),
        )
        style.map(
            'TEntry',
            fieldbackground=[('focus', input_color)],
            foreground=[('disabled', muted_color)],
        )
        style.configure(
            'Vertical.TScrollbar',
            background=surface_color,
            troughcolor=bg_color,
            bordercolor=bg_color,
            arrowcolor=accent_color,
        )

    def create_rounded_button(
        self, parent, text, command, background=None, foreground=None,
        state=tk.NORMAL
    ):
        """Crée un bouton au contour dégradé du thème."""
        return RoundedButton(
            parent,
            text=text,
            command=command,
            font=GUI_SETTINGS.get('button_font', ('Bahnschrift', 10, 'bold')),
            parent_background=COLORS.get('surface', '#171320'),
            background=background or COLORS.get('button', '#171320'),
            hover_background=COLORS.get('button_hover', '#211A2D'),
            foreground=foreground or COLORS.get('text', '#F2EEF9'),
            state=state,
            height=42,
        )
    
    def create_widgets(self):
        """Crée les widgets de l'interface."""
        self.main_frame = ttk.Frame(self.root, padding=18)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame = self.main_frame

        hero_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=(18, 14))
        hero_frame.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(
            hero_frame,
            text="IAM  /  NEURAL SYSTEM",
            style='Eyebrow.TLabel',
        ).pack(anchor=tk.W)
        ttk.Label(
            hero_frame,
            text="INTERFACE D'APPRENTISSAGE",
            style='Header.TLabel',
        ).pack(anchor=tk.W, pady=(3, 0))
        ttk.Label(
            hero_frame,
            text="CONSOLE DE DIALOGUE  •  MODÈLE REASON",
            style='Muted.TLabel',
        ).pack(anchor=tk.W, pady=(2, 0))

        control_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=(14, 12))
        control_frame.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(
            control_frame, text="COMMANDES DU MODÈLE", style='Eyebrow.TLabel'
        ).pack(anchor=tk.W, padx=4, pady=(0, 8))

        self.primary_actions = ttk.Frame(control_frame, style='Card.TFrame')
        primary_actions = self.primary_actions
        primary_actions.pack(fill=tk.X)
        self.retrain_button = self.create_rounded_button(
            primary_actions,
            text="Entraîner à nouveau le modèle ※",
            command=self.start_training_without_delete,
        )

        self.train_button = self.create_rounded_button(
            primary_actions,
            text="Entraîner le modèle ※",
            command=self.start_training,
        )

        self.stop_train_button = self.create_rounded_button(
            primary_actions,
            text="Arrêter l'entraînement ⏹",
            command=self.stop_training_thread,
            state=tk.DISABLED,
        )
        self.primary_buttons = (
            self.retrain_button,
            self.train_button,
            self.stop_train_button,
        )

        self.secondary_actions = ttk.Frame(control_frame, style='Card.TFrame')
        secondary_actions = self.secondary_actions
        secondary_actions.pack(fill=tk.X, pady=(8, 0))
        self.test_button = self.create_rounded_button(
            secondary_actions,
            text="Tester le modèle ↝",
            command=self.test_model,
        )

        self.load_button = self.create_rounded_button(
            secondary_actions,
            text="Recharger le modèle ↻",
            command=self.load_model,
        )
        self.secondary_buttons = (self.test_button, self.load_button)

        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=(8, 4))
        status_frame.pack(fill=tk.X, pady=(0, 12))
        self.status_label = ttk.Label(
            status_frame, text="STATUT  /  PRÊT", style='Status.TLabel', anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.system_label = ttk.Label(
            status_frame,
            text="SYSTÈME  /  INITIALISATION",
            style='System.TLabel',
            anchor=tk.E,
        )
        self.system_label.pack(side=tk.RIGHT)

        dialogue_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=12)
        dialogue_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.chat_display = scrolledtext.ScrolledText(
            dialogue_frame,
            width=1,
            height=1,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=GUI_SETTINGS.get('chat_font', ('Cascadia Code', 10)),
            fg=COLORS.get('text', '#F2EEF9'),
            insertbackground=COLORS.get('accent', '#DCCBFF'),
            selectbackground=COLORS.get('accent', '#DCCBFF'),
            selectforeground=COLORS.get('bg', '#09070F'),
            padx=14,
            pady=10,
            bg=COLORS.get('input', '#0D0B13'),
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=COLORS.get('frame', '#110E19'),
            highlightcolor=COLORS.get('accent', '#DCCBFF'),
        )
        chat_font_family = GUI_SETTINGS.get('chat_font', ('Cascadia Code', 10))[0]
        self.chat_display.tag_configure(
            'sender_user',
            foreground=COLORS.get('chat_user', '#DCCBFF'),
            font=(chat_font_family, 10, 'bold'),
        )
        self.chat_display.tag_configure(
            'sender_assistant',
            foreground=COLORS.get('accent', '#DCCBFF'),
            font=(chat_font_family, 10, 'bold'),
        )
        self.chat_display.tag_configure(
            'sender_system',
            foreground=COLORS.get('chat_system', '#A69FB5'),
            font=(chat_font_family, 10, 'bold'),
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        input_frame = ttk.Frame(dialogue_frame, style='Card.TFrame')
        input_frame.pack(fill=tk.X, pady=(10, 0))

        self.user_input = ttk.Entry(input_frame, font=GUI_SETTINGS.get('font'))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", lambda e: self.send_message())

        self.send_button = self.create_rounded_button(
            input_frame,
            text="Envoyer ⇾",
            command=self.send_message,
        )
        self.send_button.pack(side=tk.LEFT)

        validation_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=(10, 8))
        validation_frame.pack(fill=tk.X, pady=(0, 10))
        self.feedback_label = ttk.Label(
            validation_frame, text="FEEDBACK / APPRENTISSAGE", style='Eyebrow.TLabel'
        )
        self.validate_button = self.create_rounded_button(
            validation_frame,
            text="Valider la réponse ✓",
            command=self.validate_response,
            background=COLORS.get('button', '#171320'),
            foreground=COLORS.get('validate', '#DCCBFF'),
        )
        self.validate_button.pack(side=tk.LEFT, padx=5)

        self.correct_button = self.create_rounded_button(
            validation_frame,
            text="Corriger la réponse ✕",
            command=self.correct_response,
            background=COLORS.get('button', '#171320'),
            foreground=COLORS.get('correct', '#B6AEC5'),
        )
        self.correct_button.pack(side=tk.LEFT, padx=5)

        self.correction_frame = ttk.Frame(
            main_frame, style='Card.TFrame', padding=(10, 8)
        )
        self.correction_label = ttk.Label(
            self.correction_frame, text="CORRECTION", style='Eyebrow.TLabel'
        )
        self.correction_entry = ttk.Entry(self.correction_frame, width=24)
        self.correction_ok_button = self.create_rounded_button(
            self.correction_frame,
            text="OK",
            command=self.save_correction,
        )
        self.correction_frame.pack_forget()

        self.root.bind("<Configure>", self._on_root_resize)
        self._layout_mode = None
        self._apply_responsive_layout(self.root.winfo_width())
        self.update_system_status()
        self.root.after(100, self.update_system_status)

    def _on_root_resize(self, event):
        if event.widget is self.root:
            self._apply_responsive_layout(event.width)

    @staticmethod
    def _forget_geometry(widget):
        manager = widget.winfo_manager()
        if manager == "pack":
            widget.pack_forget()
        elif manager == "grid":
            widget.grid_forget()

    def _layout_buttons(self, frame, buttons, columns):
        for button in buttons:
            self._forget_geometry(button)

        for column in range(3):
            frame.columnconfigure(column, weight=1 if column < columns else 0)
        for index, button in enumerate(buttons):
            button.grid(
                row=index // columns,
                column=index % columns,
                padx=5,
                pady=4,
            )

    def _apply_responsive_layout(self, width):
        mode = "compact" if width < 700 else "medium" if width < 980 else "wide"
        if mode == self._layout_mode:
            return

        self._layout_mode = mode
        compact = mode == "compact"
        self.main_frame.configure(padding=10 if compact else 18)
        columns = 1 if compact else 2 if mode == "medium" else 3
        self._layout_buttons(self.primary_actions, self.primary_buttons, columns)
        self._layout_buttons(
            self.secondary_actions, self.secondary_buttons, min(columns, 2)
        )

        self._forget_geometry(self.status_label)
        self._forget_geometry(self.system_label)
        if compact:
            self.status_label.pack(fill=tk.X, anchor=tk.W)
            self.system_label.pack(fill=tk.X, anchor=tk.W)
        else:
            self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.system_label.pack(side=tk.RIGHT)

        feedback_widgets = (
            self.feedback_label,
            self.validate_button,
            self.correct_button,
        )
        for widget in feedback_widgets:
            self._forget_geometry(widget)
        if compact:
            for widget in feedback_widgets:
                widget.pack(fill=tk.X, padx=5, pady=3)
        elif mode == "medium":
            self.feedback_label.pack(anchor=tk.W, padx=4, pady=(0, 4))
            self.validate_button.pack(side=tk.LEFT, padx=5)
            self.correct_button.pack(side=tk.LEFT, padx=5)
        else:
            self.feedback_label.pack(side=tk.LEFT, padx=(4, 12))
            self.validate_button.pack(side=tk.LEFT, padx=5)
            self.correct_button.pack(side=tk.LEFT, padx=5)

        correction_widgets = (
            self.correction_label,
            self.correction_entry,
            self.correction_ok_button,
        )
        for widget in correction_widgets:
            self._forget_geometry(widget)
        if compact:
            for widget in correction_widgets:
                widget.pack(fill=tk.X, padx=5, pady=3)
        else:
            self.correction_label.pack(side=tk.LEFT, padx=5)
            self.correction_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.correction_ok_button.pack(side=tk.LEFT, padx=5)

    def load_model(self):
        """Charge le modèle"""
        self.status_label.config(text="Statut: Chargement du modèle...")
        self.root.update()
        
        def _load():
            success = self.model_manager.load_model()
            if success:
                self.model_loaded = True
                self.status_label.config(text="Statut: Modèle chargé ✅")
            else:
                self.model_loaded = False
                self.status_label.config(
                    text=f"Statut: Modèle à entraîner depuis zéro — "
                    f"{self.model_manager.load_error or 'chargement impossible'}"
                )
        
        threading.Thread(target=_load, daemon=True).start()
    
    def start_training(self):
        """Démarre l'entraînement du modèle"""
        if self.is_training:
            messagebox.showinfo("Info", "Un entraînement est déjà en cours.")
            return
        
        self.is_training = True
        self.status_label.config(text="Statut: Entraînement en cours...")
        self.train_button.set_state(tk.DISABLED)
        self.retrain_button.set_state(tk.DISABLED)
        self.stop_train_button.set_state(tk.NORMAL)
        
        def on_progress(message):
            self.training_progress_queue.put(message)
        
        try:
            self.model_manager.train_model(on_progress=on_progress)
        except Exception as error:
            self.is_training = False
            self.train_button.set_state(tk.NORMAL)
            self.retrain_button.set_state(tk.NORMAL)
            self.stop_train_button.set_state(tk.DISABLED)
            self.status_label.config(text="Statut: Échec du démarrage de l'entraînement ❌")
            messagebox.showerror("Erreur", f"Impossible de démarrer l'entraînement: {error}")
            return
        
        # Vérifier régulièrement si l'entraînement est terminé
        self.check_training_status()

    def start_training_without_delete(self):
            """Démarre l'entraînement du modèle"""
            if self.is_training:
                messagebox.showinfo("Info", "Un entraînement est déjà en cours.")
                return
            
            self.is_training = True
            self.status_label.config(text="Statut: Entraînement en cours...")
            self.train_button.set_state(tk.DISABLED)
            self.retrain_button.set_state(tk.DISABLED)
            self.stop_train_button.set_state(tk.NORMAL)
            
            def on_progress(message):
                self.training_progress_queue.put(message)
            
            try:
                self.model_manager.train_model(on_progress=on_progress,removeOldmodel=False)
            except Exception as error:
                self.is_training = False
                self.train_button.set_state(tk.NORMAL)
                self.retrain_button.set_state(tk.NORMAL)
                self.stop_train_button.set_state(tk.DISABLED)
                self.status_label.config(text="Statut: Échec du démarrage de l'entraînement ❌")
                messagebox.showerror("Erreur", f"Impossible de démarrer l'entraînement: {error}")
                return
            
            # Vérifier régulièrement si l'entraînement est terminé
            self.check_training_status()
    
    def stop_training_thread(self):
        """Arrête l'entraînement en cours"""
        if self.model_manager.stop_training():
            self.status_label.config(text="Statut: Arrêt de l'entraînement demandé...")
            self.stop_train_button.set_state(tk.DISABLED)
    
    def check_training_status(self):
        """Vérifie si l'entraînement est terminé"""
        while True:
            try:
                progress = self.training_progress_queue.get_nowait()
            except queue.Empty:
                break
            self.status_label.config(text=f"Statut: {progress}")

        if self.model_manager.is_training:
            self.root.after(1000, self.check_training_status)
        else:
            self.is_training = False
            self.train_button.set_state(tk.NORMAL)
            self.retrain_button.set_state(tk.NORMAL)
            self.stop_train_button.set_state(tk.DISABLED)

            if self.model_manager.training_error:
                error = self.model_manager.training_error
                self.model_loaded = False
                self.status_label.config(text="Statut: Échec de l'entraînement ❌")
                messagebox.showerror("Erreur d'entraînement", error)
            elif self.model_manager.training_stopped:
                self.status_label.config(
                    text="Statut: Entraînement arrêté; meilleur checkpoint conservé"
                )
                self.model_loaded = True
            else:
                self.status_label.config(text="Statut: Entraînement terminé ✅")
                self.model_loaded = True
    
    def test_model(self):
        """Teste le modèle avec une question de test"""
        if not self.model_loaded:
            messagebox.showwarning("Avertissement", "Veuillez d'abord charger le modèle.")
            return
        
        test_questions = [
            "Quelle est la capitale de la France ?",
            "Combien font 2 + 2 ?",
            "Qu'est-ce que l'intelligence artificielle ?",
            "Qui a écrit Roméo et Juliette ?"
        ]
        
        for question in test_questions:
            answer = self.model_manager.chat(question)
            self.display_message("Test", question)
            self.display_message("IA", answer)
            self.display_message("-", "-" * 50)
    
    def send_message(self):
        """Envoie un message et reçoit une réponse"""
        question = self.user_input.get()
        if not question:
            return
        
        # Effacer l'entrée
        self.user_input.delete(0, tk.END)
        
        # Afficher la question
        self.display_message("Vous", question)
        
        # Si le modèle est en entraînement
        if self.model_manager.is_training:
            self.display_message("IA", "Entraînement en cours, veuillez patienter...")
            return
        
        # Si le modèle n'est pas chargé
        if not self.model_loaded:
            self.display_message("IA", "Modèle non chargé. Veuillez d'abord charger le modèle.")
            return
        
        # Obtenir la réponse
        answer = self.model_manager.chat(question)
        
        # Afficher la réponse
        self.display_message("IA", answer)
        
        # Sauvegarder la question et la réponse pour validation
        self.last_question = question
        self.last_answer = answer
        
        # Lire la réponse à voix haute
        self.voice._init_engine()
        self.voice.say(answer)
    
    def display_message(self, sender, message):
        """Affiche un message dans la zone de chat"""
        self.chat_display.config(state=tk.NORMAL)
        sender_style = {
            "vous": "sender_user",
            "ia": "sender_assistant",
            "système": "sender_system",
        }.get(sender.casefold(), "sender_system")
        self.chat_display.insert(tk.END, f"{sender}: ", sender_style)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def validate_response(self):
        """Valide la dernière réponse de l'IA"""
        if not hasattr(self, 'last_question') or not hasattr(self, 'last_answer'):
            messagebox.showinfo("Info", "Aucune réponse à valider.")
            return
        
        # Ajouter au corpus
        success = self.model_manager.add_to_corpus(self.last_question, self.last_answer)
        if success:
            self.display_message(
                "Système",
                "✅ Réponse validée et ajoutée au corpus. "
                "Un ré-entraînement est nécessaire pour l'intégrer au modèle.",
            )
        else:
            self.display_message("Système", "❌ Erreur lors de l'ajout au corpus.")
        
        # Réinitialiser
        del self.last_question
        del self.last_answer
    
    def correct_response(self):
        """Demande une correction pour la dernière réponse"""
        if not hasattr(self, 'last_question') or not hasattr(self, 'last_answer'):
            messagebox.showinfo("Info", "Aucune réponse à corriger.")
            return
        
        # Afficher le frame de correction
        self.correction_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pré-remplir avec la réponse actuelle
        self.correction_entry.delete(0, tk.END)
        self.correction_entry.insert(0, self.last_answer)
        self.correction_entry.focus()
    
    def save_correction(self):
        """Sauvegarde la correction"""
        if not hasattr(self, 'last_question'):
            return
        
        corrected_answer = self.correction_entry.get()
        if not corrected_answer:
            messagebox.showwarning("Avertissement", "Veuillez entrer une correction.")
            return
        
        # Ajouter la correction au corpus
        success = self.model_manager.add_to_corpus(self.last_question, corrected_answer)
        if success:
            self.display_message(
                "Système",
                "✅ Correction enregistrée. "
                "Un ré-entraînement est nécessaire pour l'intégrer au modèle.",
            )
        else:
            self.display_message("Système", "❌ Erreur lors de l'enregistrement de la correction.")
        
        # Cacher le frame de correction
        self.correction_frame.pack_forget()
        
        # Réinitialiser
        del self.last_question
        del self.last_answer
    
    def update_system_status(self):
        """Met à jour l'affichage du statut système"""
        status = self.system_monitor.get_status()
        self.system_label.config(text=status)
        self.root.after(5000, self.update_system_status)


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

def main():
    # Vérifier les dépendances
    try:
        import torch
        import pyttsx3
        import psutil
        if sys.platform == "win32":
            import comtypes.client
    except ImportError as e:
        messagebox.showerror("Erreur", f"Dépendance manquante: {e}")
        sys.exit(1)
    
    # Créer l'interface graphique
    root = tk.Tk()
    app = IAMGUI(root)
    
    # Configurer l'icône (si disponible)
    icon_path = os.path.join(os.path.dirname(__file__), "iam.ico")
    if os.path.isfile(icon_path):
        try:
            root.iconbitmap(default=icon_path)
        except tk.TclError as error:
            logging.warning("Impossible de charger l'icône %s: %s", icon_path, error)
    
    # Démarrer la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()
