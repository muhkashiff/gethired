import json

from .repository_entity import RepositoryEntity


class RepositoryLoader:

    ############################################################

    def load(

        self,

        ontology_name,

        path,

    ):

        with open(

            path,

            "r",

            encoding="utf8",

        ) as f:

            raw = json.load(f)

        entities = []

        ########################################################
        # support both
        #
        # {
        #   "gmp": {...},
        #   "haccp": {...}
        # }
        #
        # and
        #
        # [
        #   {...},
        #   {...}
        # ]
        ########################################################

        iterator = raw.values() if isinstance(raw, dict) else raw

        ########################################################

        for item in iterator:

            entity = RepositoryEntity(

                ################################################
                # identity
                ################################################

                entity_id=item.get("entity_id", ""),

                canonical=item.get("canonical", ""),

                normalized=item.get(

                    "normalized",

                    item.get("canonical", "").lower(),

                ),

                aliases=item.get("aliases", []),

                ################################################
                # linguistic
                ################################################

                base=item.get("base", ""),

                past=item.get("past", ""),

                gerund=item.get("gerund", ""),

                plural=item.get("plural", ""),

                singular=item.get("singular", ""),

                abbreviation=item.get("abbreviation", ""),

                short_name=item.get("short_name", ""),

                ################################################
                # classification
                ################################################

                category=item.get("category", ""),

                entity_type=item.get(

                    "entity_type",

                    ontology_name[:-1]
                    if ontology_name.endswith("s")
                    else ontology_name,

                ),

                ontology_name=ontology_name,

                ################################################
                # business
                ################################################

                domain=item.get("domain", ""),

                business_area=item.get(

                    "business_area",

                    "",

                ),

                description=item.get(

                    "description",

                    "",

                ),

                ################################################
                # behaviour
                ################################################

                impact_weight=item.get(

                    "impact_weight",

                    1.0,

                ),

                business_meaning=item.get(

                    "business_meaning",

                    "",

                ),

                preferred_direction=item.get(

                    "preferred_direction",

                    "",

                ),

                preferred_unit=item.get(

                    "preferred_unit",

                    "",

                ),

                higher_is_better=item.get(

                    "higher_is_better",

                    True,

                ),

                ################################################
                # search
                ################################################

                searchable=item.get(

                    "searchable",

                    True,

                ),

                active=item.get(

                    "active",

                    True,

                ),

                ################################################
                # source
                ################################################

                source=item.get(

                    "source",

                    ontology_name,

                ),

                metadata=item.get(

                    "metadata",

                    {},

                ),

            )

            entities.append(entity)

        return entities