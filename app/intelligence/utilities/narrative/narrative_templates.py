"""
Narrative Block Library
"""

import json
import random

from pathlib import Path


class NarrativeTemplates:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent

            / "narrative_knowledge"

            / "data"

            / "narrative_blocks.json"

        )

        with open(path, encoding="utf8") as f:

            self.blocks = json.load(f)

    # -----------------------------------------------------

    def intro(self, section):

        return random.choice(

            self.blocks[section]["intro"]

        )

    # -----------------------------------------------------

    def ending(self, section):

        return random.choice(

            self.blocks[section]["ending"]

        )