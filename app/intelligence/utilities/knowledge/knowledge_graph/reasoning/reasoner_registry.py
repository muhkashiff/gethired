"""
Enterprise Reasoner Registry

Enterprise V7

Purpose
-------
Central registry for every enterprise reasoner.

The pipeline never directly creates reasoners.

Instead it executes the registry.

Benefits

✔ Open/Closed Principle

✔ Easy plugin architecture

✔ Dynamic execution order

✔ Easy enable/disable

✔ Future extensions
"""

from typing import List


class ReasonerRegistry:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self._reasoners = []

    ####################################################################
    # REGISTER
    ####################################################################

    def register(

        self,

        reasoner,

    ):

        """
        Register a reasoner.

        Duplicate registration is ignored.
        """

        if reasoner not in self._reasoners:

            self._reasoners.append(

                reasoner

            )

    ####################################################################
    # REGISTER MANY
    ####################################################################

    def register_many(

        self,

        reasoners,

    ):

        for reasoner in reasoners:

            self.register(

                reasoner

            )

    ####################################################################
    # REMOVE
    ####################################################################

    def unregister(

        self,

        reasoner,

    ):

        if reasoner in self._reasoners:

            self._reasoners.remove(

                reasoner

            )

    ####################################################################
    # CLEAR
    ####################################################################

    def clear(self):

        self._reasoners.clear()

    ####################################################################
    # ENABLE
    ####################################################################

    def enable(

        self,

        reasoner_name,

    ):

        for reasoner in self._reasoners:

            if reasoner.name == reasoner_name:

                reasoner.enabled = True

    ####################################################################
    # DISABLE
    ####################################################################

    def disable(

        self,

        reasoner_name,

    ):

        for reasoner in self._reasoners:

            if reasoner.name == reasoner_name:

                reasoner.enabled = False

    ####################################################################
    # ITERATOR
    ####################################################################

    def get_reasoners(

        self,

    ) -> List:

        """
        Returns enabled reasoners
        in registration order.
        """

        return [

            reasoner

            for reasoner in self._reasoners

            if getattr(

                reasoner,

                "enabled",

                True,

            )

        ]

    ####################################################################
    # LENGTH
    ####################################################################

    def __len__(self):

        return len(

            self._reasoners

        )

    ####################################################################
    # STRING
    ####################################################################

    def __repr__(self):

        names = [

            reasoner.name

            for reasoner in self._reasoners

        ]

        return (

            f"ReasonerRegistry({names})"

        )