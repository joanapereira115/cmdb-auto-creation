# -*- coding: utf-8 -*-

import itertools


class ConfigurationItemType:
    """Represents the type of a configuration item.

    Attributes:
        id_iter         The iterator used to generate the configuration item type identifier.
        name            The name of the type of the configuration item.
    """

    id_iter = itertools.count()
    name = ""

    def __init__(self, name):
        """Initialize the configuration item type with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.name = name

    def get_id(self):
        """Get the configuration item type identifier."""
        return self.id

    def get_name(self):
        """Get the configuration item type name."""
        return self.name
