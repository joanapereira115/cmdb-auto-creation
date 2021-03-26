# -*- coding: utf-8 -*-

import itertools

from normalization import normalization


class Attribute:
    """Represents an attribute of a configuration item or relationship.

    Attributes:
        id_iter         The iterator used to generate the attribute identifier.
        title            The title of the attribute.
        value           The value of the attribute.
    """

    id_iter = itertools.count()
    title = ""
    value = ""

    def __init__(self, title, value):
        """Initialize the attribute with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.title = normalization.parse_text_to_store(title)
        self.value = normalization.parse_text_to_store(value)

    def get_id(self):
        """Get the attribute identifier."""
        return self.id

    def get_title(self):
        """Get the attribute title."""
        return self.title

    def get_value(self):
        """Get the attribute value."""
        return self.value

    def set_value(self, value):
        """Get the attribute value."""
        self.value = normalization.parse_text_to_store(value)
