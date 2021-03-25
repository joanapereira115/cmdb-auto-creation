# -*- coding: utf-8 -*-

import itertools
from normalization import normalization


class RelationshipType:
    """Represents the type of a relationship.

    Attributes:
        id_iter         The iterator used to generate the relationship identifier.
        title            The title of the type of the relationship.
    """

    id_iter = itertools.count()
    title = ""

    def __init__(self, title):
        """Initialize the relationship type with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.title = title

    def get_id(self):
        """Get the relationship type identifier."""
        return self.id

    def get_title(self):
        """Get the relationship type title."""
        return self.title

    def set_title(self, title):
        """Sets the relationship type title."""
        if title != None and title != "":
            self.title = title
