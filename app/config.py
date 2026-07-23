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

    UPLOAD_FOLDER = "uploads"

    OUTPUT_FOLDER = "outputs"