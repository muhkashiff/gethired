import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "ProjectJob123"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///gethired.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 25 * 1024 * 1024

    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    OUTPUT_FOLDER = BASE_DIR / "outputs"
