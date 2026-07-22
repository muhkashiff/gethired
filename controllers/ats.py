"""
Creates required folders automatically
"""

from pathlib import Path

from config import (
    UPLOADS_DIR,
    OUTPUTS_DIR,
    LOGS_DIR,
    TEMP_DIR,
    ASSETS_DIR
)


class FolderManager:

    @staticmethod
    def create_required_folders():

        folders = [
            UPLOADS_DIR,
            OUTPUTS_DIR,
            LOGS_DIR,
            TEMP_DIR,
            ASSETS_DIR
        ]

        for folder in folders:
            Path(folder).mkdir(
                parents=True,
                exist_ok=True
            )

        print("All required folders created.")