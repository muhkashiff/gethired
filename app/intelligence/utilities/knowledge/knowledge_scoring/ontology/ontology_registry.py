"""
Enterprise Ontology Registry

Enterprise V12

Single source of truth
for every ontology object.
"""

from collections import defaultdict

from .ontology_models import OntologyItem


class OntologyRegistry:

    def __init__(self):

        self._items = {}

        self._aliases = {}

    # -------------------------------------------------

    def register(self, item: OntologyItem):

        key = item.canonical.lower()

        self._items[key] = item

        self._aliases[key] = key

        for alias in item.aliases:

            self._aliases[alias.lower()] = key

    # -------------------------------------------------

    def get(self, name: str):

        if not name:

            return None

        key = self._aliases.get(

            name.lower()

        )

        if key is None:

            return None

        return self._items.get(key)

    # -------------------------------------------------

    def capabilities(self, name: str):

        item = self.get(name)

        if item is None:

            return []

        return item.capabilities

    # -------------------------------------------------

    def all(self):

        return list(

            self._items.values()

        )

    # -------------------------------------------------

    def summary(self):

        categories = defaultdict(int)

        for item in self._items.values():

            categories[item.category] += 1

        return {

            "items": len(self._items),

            "categories": dict(categories),

        }


registry = OntologyRegistry()