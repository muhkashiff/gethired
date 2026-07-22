"""
GetHired Configuration
"""

from pathlib import Path


class Config:

    # -----------------------------
    # APP INFO
    # -----------------------------

    APP_NAME = "GetHired"

    APP_VERSION = "1.0.0"

    COMPANY = "GetHired"

    # -----------------------------
    # WINDOW
    # -----------------------------

    WIDTH = 1450

    HEIGHT = 900

    MIN_WIDTH = 1200

    MIN_HEIGHT = 700

    # -----------------------------
    # THEME
    # -----------------------------

    APPEARANCE = "dark"

    COLOR_THEME = "blue"

    FONT = "Segoe UI"

    # -----------------------------
    # DIRECTORIES
    # -----------------------------

    ROOT = Path(__file__).parent

    ASSETS = ROOT / "assets"

    OUTPUTS = ROOT / "outputs"

    UPLOADS = ROOT / "uploads"

    LOGS = ROOT / "logs"

    TEMP = ROOT / "temp"

    # -----------------------------
    # FILE TYPES
    # -----------------------------

    RESUME_TYPES = (
        ".pdf",
        ".docx"
    )

    JD_TYPES = (
        ".pdf",
        ".docx",
        ".txt"
    )