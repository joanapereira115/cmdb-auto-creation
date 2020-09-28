# -*- coding: utf-8 -*-

import itertools


class Attribute:
    """Represents an attribute of a configuration item or relationship.

    Attributes:
        id_iter         The iterator used to generate the attribute identifier.
        name            The name of the attribute.
        value           The value of the attribute.
    """

    id_iter = itertools.count()
    name = ""
    value = ""

    def __init__(self, name, value):
        """Initialize the attribute with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.name = name
        self.value = value

    def get_id(self):
        """Get the attribute identifier."""
        return self.id

    def get_name(self):
        """Get the attribute name."""
        return self.name

    def get_value(self):
        """Get the attribute value."""
        return self.value
