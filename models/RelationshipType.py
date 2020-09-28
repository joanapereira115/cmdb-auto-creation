# -*- coding: utf-8 -*-

import itertools


class RelationshipType:
    """Represents the type of a relationship.

    Attributes:
        id_iter         The iterator used to generate the relationship identifier.
        name            The name of the type of the relationship.
    """

    id_iter = itertools.count()
    name = ""

    def __init__(self, name):
        """Initialize the relationship type with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.name = name

    def get_id(self):
        """Get the relationship type identifier."""
        return self.id

    def get_name(self):
        """Get the relationship type name."""
        return self.name
