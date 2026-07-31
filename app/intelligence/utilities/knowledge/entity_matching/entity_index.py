"""
Entity Index


Loads every ontology dictionary into one searchable index.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.repository.repository import Repository


class EntityIndex:

    def __init__(self):

        self.repository = Repository()

        self.index = {}

        self._load()

    # --------------------------------------------------

    def _load_dictionary(self, dictionary_name, entity_type):

        dictionary = self.repository.get_dictionary(dictionary_name)

        if dictionary is None:
            return

        for key in dictionary.keys():

            entity = None

            if entity_type == "action":
                entity = self.repository.get_action(key)

            elif entity_type == "object":
                entity = self.repository.get_object(key)

            elif entity_type == "metric":
                entity = self.repository.get_metric(key)

            elif entity_type == "kpi":
                entity = self.repository.get_business_kpi(key)

            elif entity_type == "domain":
                entity = self.repository.get_domain(key)

            elif entity_type == "certificate":
                entity = self.repository.get_certification(key)

            elif entity_type == "technology":
                entity = self.repository.get_technology(key)

            elif entity_type == "methodology":
                entity = self.repository.get_methodology(key)

            elif entity_type == "skill":
                entity = self.repository.get_skill(key)

            elif entity_type == "standard":
                            entity = self.repository.get_standard(key)

            if entity is None:
                continue

            # --------------------------------------------------
            # Build all searchable terms
            # --------------------------------------------------

            search_terms = set()

            # Original JSON key
            search_terms.add(key)

            # Canonical name
            if entity.canonical:
                search_terms.add(entity.canonical)

            # Aliases from ontology
            if entity.aliases:
                for alias in entity.aliases:
                    if alias:
                        search_terms.add(alias)

            # Automatically generate normalized variants
            expanded_terms = set()

            for term in search_terms:

                term = term.strip()

                if not term:
                    continue

                expanded_terms.add(term.lower())

                # Remove spaces
                expanded_terms.add(
                    term.replace(" ", "").lower()
                )

                # Remove hyphens
                expanded_terms.add(
                    term.replace("-", "").lower()
                )

                # Remove both spaces and hyphens
                expanded_terms.add(
                    term.replace(" ", "")
                        .replace("-", "")
                        .lower()
                )

                # Hyphen -> space
                expanded_terms.add(
                    term.replace("-", " ").lower()
                )

            # Insert every searchable variant into the index
            for searchable in expanded_terms:

                self.index[searchable] = {
                    "entity_type": entity_type,
                    "entity": entity,
                }

    # --------------------------------------------------

    def _load(self):

        self._load_dictionary("actions", "action")

        self._load_dictionary("objects", "object")

        self._load_dictionary("metrics", "metric")

        self._load_dictionary("business_kpis", "kpi")

        self._load_dictionary("domains", "domain")

        self._load_dictionary("certifications", "certification")

        self._load_dictionary("technologies", "technology")

        self._load_dictionary("methodologies", "methodology")

        self._load_dictionary("skills", "skill")

        self._load_dictionary("standards", "standard")

    def keys(self):
    
                return self.index.keys()
    
            # --------------------------------------------------
    
    def get(self, key):
    
                return self.index.get(key.lower())            
        
    # --------------------------------------------------# --------------------------------------------------
    # Debug
    # --------------------------------------------------

if __name__ == "__main__":

    print("Creating EntityIndex...")

    index = EntityIndex()

    print("Loaded", len(index.index), "search terms")

    print("gmp:", index.get("gmp"))
    print("iso9001:", index.get("iso9001"))
    print("fssc22000:", index.get("fssc22000"))

        

        
