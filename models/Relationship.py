# -*- coding: utf-8 -*-

import json
import itertools


class Relationship:
    """Represents the relationship between two organization's infrastructure components.

    Attributes:
        id_iter         The iterator used to generate the relationship identifier.
        title            The label of the relationship.
        type_id         The identifier of the relationship type.
        source_id       The identifier of the configuration item that plays yhe role of source/master in the relationship.
        target_id       The identifier of the configuration item that plays yhe role of target/slave in the relationship.
        attributes      The list of identifiers of the relationship attributes.
    """

    id_iter = itertools.count()
    title = ""
    type_id = 0
    source_id = 0
    target_id = 0
    attributes = []

    def __init__(self):
        """Initialize the relationship with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.title = ""
        self.type_id = 0
        self.source_id = 0
        self.target_id = 0
        self.attributes = []

    def get_id(self):
        """Get the relationship identifier."""
        return self.id

    def get_title(self):
        """Get the relationship title."""
        return self.title

    def get_type(self):
        """Get the relationship type identifier."""
        return self.type_id

    def get_source_id(self):
        """Get the source configuration item identifier."""
        return self.source_id

    def set_source_id(self, s_id):
        """."""
        self.source_id = s_id

    def get_target_id(self):
        """Get the target configuration item identifier."""
        return self.target_id

    def set_target_id(self, t_id):
        """."""
        self.target_id = t_id

    def get_attributes(self):
        """Get the list of attributes identifiers of the relationship."""
        return self.attributes

    def add_attribute(self, attribute_id):
        """Adds a new attribute identifier to the list of the relationship attributes."""
        self.attributes.append(attribute_id)

    # TODO: não é necessário
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
