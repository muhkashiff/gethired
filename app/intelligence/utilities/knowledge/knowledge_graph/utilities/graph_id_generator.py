"""
Enterprise Graph ID Generator

Generates deterministic IDs for every graph object.

Purpose
-------
Guarantees:

• Stable IDs
• No duplicates
• Reproducible graph builds

Enterprise V7
"""

import hashlib


class GraphIDGenerator:

    """
    Enterprise deterministic ID generator.
    """

    ####################################################################
    # NODE ID
    ####################################################################

    def node_id(

        self,

        entity_type: str,

        entity_id: str,

    ) -> str:

        """
        Generates deterministic node ID.

        Example

            action::implement_haccp
        """

        entity_type = str(

            entity_type,

        ).strip().lower()

        entity_id = str(

            entity_id,

        ).strip().lower()

        return f"{entity_type}::{entity_id}"

    ####################################################################
    # EDGE ID
    ####################################################################

    def edge_id(

        self,

        source_id: str,

        relation: str,

        target_id: str,

    ) -> str:

        """
        Deterministic edge identifier.

        Example

            edge::ab92f0......
        """

        key = (

            f"{source_id}|"

            f"{relation.upper()}|"

            f"{target_id}"

        )

        return (

            "edge::"

            +

            hashlib.sha1(

                key.encode(

                    "utf-8",

                )

            ).hexdigest()

        )

    ####################################################################
    # SUBGRAPH ID
    ####################################################################

    def subgraph_id(

        self,

        name: str,

    ) -> str:

        """
        Generates subgraph ID.

        Example

            cluster::quality_management
        """

        name = (

            str(name)

            .strip()

            .lower()

            .replace(

                " ",

                "_",

            )

        )

        return f"cluster::{name}"

    ####################################################################
    # REASONING ID
    ####################################################################

    def reasoning_id(

        self,

        stage: str,

        entity_id: str,

    ) -> str:

        """
        Used by reasoning pipeline.

        Example

            reasoning::skill_reasoner::skill::python
        """

        stage = (

            str(stage)

            .strip()

            .lower()

        )

        entity_id = (

            str(entity_id)

            .strip()

            .lower()

        )

        return (

            f"reasoning::"

            f"{stage}::"

            f"{entity_id}"

        )

    ####################################################################
    # HASH
    ####################################################################

    def hash(

        self,

        value: str,

    ) -> str:

        """
        Generic SHA1 hash.
        """

        return hashlib.sha1(

            str(value)

            .encode(

                "utf-8",

            )

        ).hexdigest()