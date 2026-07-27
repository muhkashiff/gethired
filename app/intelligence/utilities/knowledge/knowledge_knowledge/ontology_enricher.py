"""
Ontology Enricher

Adds ontology metadata to extracted knowledge.
"""

from copy import deepcopy

from app.intelligence.utilities.knowledge.knowledge_linker.entity_linker import (
    EntityLinker,
)


class OntologyEnricher:

    def __init__(self):

        self.linker = EntityLinker()

    # -------------------------------------------------------------
    # Public
    # -------------------------------------------------------------

    from copy import deepcopy

    def enrich(self, document):

            
            document = deepcopy(document)

            enriched = []

            for fact in document.facts:

                enriched.append(self._enrich_fact(fact))

            document.facts = enriched

            return document

    # -------------------------------------------------------------
    # Private
    # -------------------------------------------------------------

    def _attach(self, obj, text):

        if not text:
            return obj

        linked = self.linker.link(text)

        if not linked.found:
            return obj

        if hasattr(obj, "entity_id"):
            obj.entity_id = linked.entity_id

        if hasattr(obj, "business_area"):
            obj.business_area = linked.business_area

        if hasattr(obj, "source"):
            obj.source = linked.source

        if hasattr(obj, "metadata"):
            obj.metadata = linked.metadata

        return obj

    # -------------------------------------------------------------

    def _enrich_fact(self, fact):

        fact = deepcopy(fact)

        interpretation = fact.interpretation

        # -----------------------------------
        # Action
        # -----------------------------------

        if interpretation.action.found:

            self._attach(

                interpretation.action,

                interpretation.action.base

            )

        # -----------------------------------
        # Object
        # -----------------------------------

        if interpretation.object.found:

            self._attach(

                interpretation.object,

                interpretation.object.canonical

            )

        # -----------------------------------
        # Metric
        # -----------------------------------

        if interpretation.metric.found:

            self._attach(

                interpretation.metric,

                interpretation.metric.canonical

            )

        # -----------------------------------
        # Domain
        # -----------------------------------

        if interpretation.domain.found:

            self._attach(

                interpretation.domain,

                interpretation.domain.domain

            )

        return fact