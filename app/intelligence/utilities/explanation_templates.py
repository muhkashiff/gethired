"""
Loads explanation templates
"""

import json
from pathlib import Path


class ExplanationTemplates:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "exp_knowledge"
            / "data"
            / "explanation_templates.json"
        )

        with open(path, encoding="utf8") as f:

            self.templates = json.load(f)

    def get(self, section, level):

        return self.templates[section][level]