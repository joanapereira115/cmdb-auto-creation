# -*- coding: utf-8 -*-

import json
from similarity import similarity
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


def get_ci_type_name_from_id(id):
    """
    Get the name of the configuration item type based on its identifier.

    Goes through the existing configuration item types until it finds the type identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the configuration item type.

    Returns
    -------
    string
        Name of the configuration item type.

    """
    ci_types = objects["configuration_item_types"]
    for ci_type in ci_types:
        type_id = ci_type.get_id()
        if type_id == id:
            return ci_type.get_name()
    return None


def get_relationship_type_name_from_id(id):
    """
    Get the name of the relationship type based on its identifier.

    Goes through the existing relationship types until it finds the type identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the relationship type.

    Returns
    -------
    string
        Name of the relationship type.

    """
    rel_types = objects["relationship_types"]
    for rel_type in rel_types:
        type_id = rel_type.get_id()
        if type_id == id:
            return rel_type.get_name()
    return None


def get_attribute_name_from_id(id):
    """
    Get the name of the attribute based on its identifier.

    Goes through the existing attributes until it finds the attribute identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the attribute.

    Returns
    -------
    string
        Name of the attribute.

    """
    attributes = objects["attributes"]
    for atr in attributes:
        type_id = atr.get_id()
        if type_id == id:
            return atr.get_name()
    return None


def get_attribute_value_from_id(id):
    """
    Get the value of the attribute based on its identifier.

    Goes through the existing attributes until it finds the attribute identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the attribute.

    Returns
    -------
    string
        Value of the attribute.

    """
    attributes = objects["attributes"]
    for atr in attributes:
        type_id = atr.get_id()
        if type_id == id:
            return atr.get_value()
    return None


def delete_configuration_item(ci):
    """
    Removes a configuration item object, in case it exists.

    Parameters
    ----------
    ci : ConfigurationItem
        The configuration item object.

    Returns
    -------
    boolean
        Returns true if the object was removed successfully, and false if it doesn't.

    """
    if ci in objects["configuration_items"]:
        objects["configuration_items"].remove(ci)
        return True
    else:
        return False


def delete_relationship(rel):
    """
    Removes a relationship object, in case it exists.

    Parameters
    ----------
    ci : Relationship
        The relationship object.

    Returns
    -------
    boolean
        Returns true if the object was removed successfully, and false if it doesn't.

    """
    if rel in objects["relationships"]:
        objects["relationships"].remove(rel)
        return True
    else:
        return False


def delete_object(obj):
    """
    Removes an object, in case it exists.

    Parameters
    ----------
    obj : ConfigurationItem or Relationship
        The object.

    Returns
    -------
    boolean
        Returns true if the object was removed successfully, and false if it doesn't.

    """
    if type(obj) == ConfigurationItem:
        return delete_configuration_item(obj)
    elif type(obj) == Relationship:
        return delete_relationship(obj)
    else:
        return False


def find_most_similar_attribute(at_name, attributes):
    """
    From a list of attributes, selects the one that has the most similar name to the requested attribute name.

    Parameters
    ----------
    at_name : string
        The attribute name.

    attribues: [int]
        The list of attributes identifiers.

    Returns
    -------
    int
        Returns the identifier of the most similar attribute from the list.

    """
    attributes_names = {}
    for at_id in attributes:
        attributes_names[at_id] = get_attribute_name_from_id(at_id)
    res = 0
    max = 0
    for at in attributes_names:
        attribute_similarity = similarity.similarity_degree(
            at_name, attributes_names[at])
        if attribute_similarity > max:
            res = at
    return res


def ci_already_exists(ci):
    """
    Finds out if a configuration item already exists.

    To understand if the configuration item already exists, goes through all the existing configuration items and compare 
    their type and attributes, and respective values, and if the most similar configuration item it discovers is at least 70% similar, 
    returns that object, otherwise, returns None.

    Parameters
    ----------
    ci : ConfigurationItem
        The configuration item object.

    Returns
    -------
    ConfigurationItem or None
        Returns the most similar configuration item that exists, if the similarity is superior than 70%, or None.

    """
    equal_ci = None
    max_ratio = 0

    existing_cis = objects["configuration_items"]
    ci_type_id = ci.get_type()
    ci_type = get_ci_type_name_from_id(ci_type_id)

    for existing_ci in existing_cis:
        existing_ci_type_id = existing_ci.get_type()
        existing_ci_type = get_ci_type_name_from_id(existing_ci_type_id)
        type_similarity = similarity.similarity_degree(
            ci_type, existing_ci_type)

        if type_similarity >= 0.5:
            attributes = ci.get_attributes()
            existing_attributes = existing_ci.get_attributes()
            total_attributes = len(attributes)
            equal_attributes = 0

            for at_id in attributes:
                at_name = get_attribute_name_from_id(at_id)
                ex_at_id = find_most_similar_attribute(
                    at_name, existing_attributes)
                ex_at_name = get_attribute_name_from_id(ex_at_id)
                attribute_similarity = similarity.similarity_degree(
                    at_name, ex_at_name)

                if attribute_similarity >= 0.5:
                    at_value = get_attribute_value_from_id(at_id)
                    ex_at_value = get_attribute_value_from_id(ex_at_id)
                    value_similarity = similarity.similarity_degree(
                        at_value, ex_at_value)

                    if value_similarity >= 0.8:
                        equal_attributes += 1

            ratio = (equal_attributes*100)/total_attributes

            if ratio > max_ratio:
                equal_ci = existing_ci

    if max_ratio > 70:
        return equal_ci

    else:
        return None


def relationship_already_exists(rel):
    """
    Finds out if a relationship already exists.

    To understand if the relationship already exists, goes through all the existing relationships and compares the configuration
    items involved, its type and attributes, and respective values, and if the most similar relationships it discovers is at least 
    70% similar, returns that object, otherwise, returns None.

    Parameters
    ----------
    rel : Relationship
        The relationship object.

    Returns
    -------
    ConfigurationItem or None
        Returns the most similar relationship that exists, if the similarity is superior than 70%, or None.

    """
    equal_rel = None
    max_ratio = 0

    existing_rels = objects["relationships"]
    rel_type_id = rel.get_type()
    rel_type = get_relationship_type_name_from_id(rel_type_id)
    source_id = rel.get_source_id()
    target_id = rel.get_target_id()

    for existing_rel in existing_rels:
        existing_source_id = existing_rel.get_source_id()
        existing_target_id = existing_rel.get_target_id()

        if existing_source_id == source_id and existing_target_id == target_id:
            existing_rel_type_id = existing_rel.get_type()
            existing_rel_type = get_relationship_type_name_from_id(
                existing_rel_type_id)
            type_similarity = similarity.similarity_degree(
                rel_type, existing_rel_type)

            if type_similarity >= 0.5:
                attributes = rel.get_attributes()
                existing_attributes = existing_rel.get_attributes()
                total_attributes = len(attributes)
                equal_attributes = 0

                for at_id in attributes:
                    at_name = get_attribute_name_from_id(at_id)
                    ex_at_id = find_most_similar_attribute(
                        at_name, existing_attributes)
                    ex_at_name = get_attribute_name_from_id(ex_at_id)
                    attribute_similarity = similarity.similarity_degree(
                        at_name, ex_at_name)

                    if attribute_similarity >= 0.5:
                        at_value = get_attribute_value_from_id(at_id)
                        ex_at_value = get_attribute_value_from_id(ex_at_id)
                        value_similarity = similarity.similarity_degree(
                            at_value, ex_at_value)

                        if value_similarity >= 0.8:
                            equal_attributes += 1

                ratio = (equal_attributes*100)/total_attributes

                if ratio > max_ratio:
                    equal_rel = existing_rel

    if max_ratio > 70:
        return equal_rel

    else:
        return None


def already_exists(obj):
    """
    Finds out if a configuration item or a relationship already exists.

    Parameters
    ----------
    obj : ConfigurationItem or Relationship
        The object.

    Returns
    -------
    ConfigurationItem or Relationship or None
        Returns the already existing object, in case it exists, or None.

    """
    if type(obj) == ConfigurationItem:
        return ci_already_exists(obj)
    elif type(obj) == Relationship:
        return relationship_already_exists(obj)
    else:
        return None
