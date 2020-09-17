import json
from objects import objects
import itertools

"""
=============
FOUND OBJECTS
=============
"""

objects = {
    "configuration_items": [],
    "relationships": [],
    "configuration_item_types": [],
    "relationship_types": [],
    "attributes": []
}

"""
==============
OBJECT CLASSES
==============
"""


class ConfigurationItem:
    """Represents an organization's infrastructure component.

    Attributes:
        id_iter         The iterator used to generate the item identifier.
        type_id         The identifier of the item type.
        attributes      The list of identifiers of the item attributes.
    """

    id_iter = itertools.count()
    type_id = 0
    attributes = []

    def __init__(self):
        """Initialize the configuration item with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the configuration item identifier."""
        return self.id

    def get_type(self):
        """Get the configuration item type identifier."""
        return self.type_id

    def get_attributes(self):
        """Get the list of attributes identifiers of the configuration item."""
        return self.attributes

    def add_attribute(self, attribute_id):
        """Adds a new attribute identifier to the list of configuration item attributes."""
        self.attributes.append(attribute_id)

    # TODO: não é necessário
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Relationship:
    """Represents the relationship between two organization's infrastructure components.

    Attributes:
        id_iter         The iterator used to generate the relationship identifier.
        type_id         The identifier of the relationship type.
        source_id       The identifier of the configuration item that plays yhe role of source/master in the relationship.
        target_id       The identifier of the configuration item that plays yhe role of target/slave in the relationship.
        attributes      The list of identifiers of the relationship attributes.
    """

    id_iter = itertools.count()
    type_id = 0
    source_id = 0
    target_id = 0
    attributes = []

    def __init__(self):
        """Initialize the relationship with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the relationship identifier."""
        return self.id

    def get_type(self):
        """Get the relationship type identifier."""
        return self.type_id

    def get_source_id(self):
        """Get the source configuration item identifier."""
        return self.id

    def get_target_id(self):
        """Get the target configuration item identifier."""
        return self.id

    def get_attributes(self):
        """Get the list of attributes identifiers of the relationship."""
        return self.attributes

    def add_attribute(self, attribute_id):
        """Adds a new attribute identifier to the list of the relationship attributes."""
        self.attributes.append(attribute_id)

    # TODO: não é necessário
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class ConfigurationItemType:
    """Represents the type of a configuration item.

    Attributes:
        id_iter         The iterator used to generate the configuration item type identifier.
        name            The name of the type of the configuration item.
    """

    id_iter = itertools.count()
    name = ""

    def __init__(self):
        """Initialize the configuration item type with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the configuration item type identifier."""
        return self.id

    def get_name(self):
        """Get the configuration item type name."""
        return self.name


class RelationshipType:
    """Represents the type of a relationship.

    Attributes:
        id_iter         The iterator used to generate the relationship identifier.
        name            The name of the type of the relationship.
    """

    id_iter = itertools.count()
    name = ""

    def __init__(self):
        """Initialize the relationship type with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the relationship type identifier."""
        return self.id

    def get_name(self):
        """Get the relationship type name."""
        return self.name


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

    def __init__(self):
        """Initialize the attribute with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the attribute identifier."""
        return self.id

    def get_name(self):
        """Get the attribute name."""
        return self.name

    def get_value(self):
        """Get the attribute value."""
        return self.value


"""
==============
OBJECT METHODS
==============
"""


# TODO: desenvolver algoritmos


def already_exists():
    """"""
    pass


def get_ci_type_name_from_id(id):
    pass


def get_relationship_type_name_from_id(id):
    pass


def get_attribute_name_from_id(id):
    pass


def get_attribute_value_from_id(id):
    pass


def delete_object(obj):
    pass
    # objects.remove(obj)


"""
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
