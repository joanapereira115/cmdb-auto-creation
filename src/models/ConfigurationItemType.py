# -*- coding: utf-8 -*-

import itertools
from normalization import normalization


class ConfigurationItemType:
    """Represents the type of a configuration item.

    Attributes:
        id_iter         The iterator used to generate the configuration item type identifier.
        title            The title of the type of the configuration item.
    """

    id_iter = itertools.count()
    title = ""

    def __init__(self, title):
        """Initialize the configuration item type with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.title = normalization.parse_text_to_store(title)

    def get_id(self):
        """Get the configuration item type identifier."""
        return self.id

    def get_title(self):
        """Get the configuration item type title."""
        return self.title

    def set_title(self, title):
        """Sets the configuration item type title."""
        if title != None and title != "":
            self.title = normalization.parse_text_to_store(title)
