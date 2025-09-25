# backend/config.py
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_SAVE_DIR = os.path.join(BASE_DIR, 'default_storage')
AUTO_COMMIT_MESSAGE = "Auto-commit from Notepad Tracker"
