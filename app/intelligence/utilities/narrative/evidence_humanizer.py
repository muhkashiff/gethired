"""
Evidence Humanizer

Converts resume evidence into
natural narrative language.
"""

import json
from pathlib import Path


class EvidenceHumanizer:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent
            / "narrative_knowledge"
            / "data"
            / "humanizer_rules.json"

        )

        with open(path, encoding="utf8") as f:

            rules = json.load(f)

        self.verbs = rules["verb_replacements"]

        self.phrases = rules["phrase_replacements"]

        self.cleanup = rules["cleanup"]

    # ----------------------------------------------------------

    def humanize(self, sentence):

        sentence = sentence.strip()

        if self.cleanup["remove_period"]:

            sentence = sentence.rstrip(".")

        # Replace first verb

        for verb, replacement in self.verbs.items():

            if sentence.startswith(verb + " "):

                sentence = sentence.replace(

                    verb,

                    replacement,

                    1

                )

                break

        # Replace phrases

        for phrase, replacement in self.phrases.items():

            sentence = sentence.replace(

                phrase,

                replacement

            )

        if self.cleanup["capitalize"]:

            sentence = sentence.capitalize()

        return sentence

    # ----------------------------------------------------------

    def humanize_list(self, evidence):

        return [

            self.humanize(item)

            for item in evidence

        ]