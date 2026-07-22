"""
gethired

Application Entry Point
"""

import customtkinter as ctk

from config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    APPEARANCE_MODE,
    COLOR_THEME
)

from core.folder_manager import FolderManager


class ResumeCustomizerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.initialize_window()

    def initialize_window(self):

        self.title(APP_NAME)

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.minsize(1200, 700)

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # Temporary startup label
        startup_label = ctk.CTkLabel(
            self,
            text="gethired\n\nPhase 1 Foundation Loaded",
            font=("Segoe UI", 24, "bold")
        )

        startup_label.pack(
            expand=True
        )


def main():

    FolderManager.create_required_folders()

    ctk.set_appearance_mode(
        APPEARANCE_MODE
    )

    ctk.set_default_color_theme(
        COLOR_THEME
    )

    app = ResumeCustomizerApp()

    app.mainloop()


if __name__ == "__main__":
    main()