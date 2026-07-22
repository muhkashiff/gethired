"""
Application Configuration
"""

from pathlib import Path

# --------------------------------------------------
# Application Information
# --------------------------------------------------

APP_NAME = "gethired"
APP_VERSION = "1.0.0"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

# --------------------------------------------------
# Theme
# --------------------------------------------------

APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# --------------------------------------------------
# Base Directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"

# --------------------------------------------------
# Supported Files
# --------------------------------------------------

SUPPORTED_RESUME_TYPES = [
    ".pdf",
    ".docx"
]

SUPPORTED_JD_TYPES = [
    ".pdf",
    ".docx",
    ".txt"
]