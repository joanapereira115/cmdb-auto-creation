# -*- coding: utf-8 -*-

import json
import itertools

from . import Relationship
from . import ConfigurationItem
from .objects import objects
# TODO: mudar
from semantic_matching import semantic_matching
from similarity import similarity
from reconciliation import reconciliation


def get_ci_type_title_from_id(id):
    """
    Get the title of the configuration item type based on its identifier.

    Goes through the existing configuration item types until it finds the type identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the configuration item type.

    Returns
    -------
    string
        title of the configuration item type.

    """
    ci_types = objects["configuration_item_types"]
    for ci_type in ci_types:
        type_id = ci_type.get_id()
        if type_id == id:
            return ci_type.get_title()
    return None


def get_relationship_type_title_from_id(id):
    """
    Get the title of the relationship type based on its identifier.

    Goes through the existing relationship types until it finds the type identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the relationship type.

    Returns
    -------
    string
        title of the relationship type.

    """
    rel_types = objects["relationship_types"]
    for rel_type in rel_types:
        type_id = rel_type.get_id()
        if type_id == id:
            return rel_type.get_title()
    return None


def get_attribute_from_id(id):
    """
    Get the attribute based on its identifier.

    Goes through the existing attributes until it finds the attribute identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the attribute.

    Returns
    -------
    Attribute
        The attribute.

    """
    attributes = objects["attributes"]
    for atr in attributes:
        type_id = atr.get_id()
        if type_id == id:
            return atr
    return None


def get_attribute_title_from_id(id):
    """
    Get the title of the attribute based on its identifier.

    Goes through the existing attributes until it finds the attribute identified by the requested id.

    Parameters
    ----------
    id : int
        Identifier of the attribute.

    Returns
    -------
    string
        title of the attribute.

    """
    attributes = objects["attributes"]
    for atr in attributes:
        type_id = atr.get_id()
        if type_id == id:
            return atr.get_title()
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


def find_most_similar_attribute(at_title, attributes):
    """
    From a list of attributes, selects the one that has the most similar title to the requested attribute title.

    Parameters
    ----------
    at_title : string
        The attribute title.

    attribues: [int]
        The list of attributes identifiers.

    Returns
    -------
    int
        Returns the identifier of the most similar attribute from the list.

    """
    attributes_titles = {}
    for at_id in attributes:
        attributes_titles[at_id] = get_attribute_title_from_id(at_id)
    res = 0
    max = 0
    for at in attributes_titles:
        at_title2 = attributes_titles.get(at)
        if at_title2 != None and at_title != None:
            attribute_similarity = semantic_matching.semantic_coeficient(
                at_title, at_title2)
        else:
            attribute_similarity = 0
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
    ci_type = get_ci_type_title_from_id(ci_type_id)

    for existing_ci in existing_cis:
        existing_ci_type_id = existing_ci.get_type()
        existing_ci_type = get_ci_type_title_from_id(existing_ci_type_id)
        type_similarity = semantic_matching.semantic_coeficient(
            ci_type, existing_ci_type)

        if type_similarity >= 0.5:
            attributes = ci.get_attributes()
            existing_attributes = existing_ci.get_attributes()
            total_attributes = len(attributes)
            equal_attributes = 0

            for at_id in attributes:
                at_title = get_attribute_title_from_id(at_id)
                ex_at_id = find_most_similar_attribute(
                    at_title, existing_attributes)
                ex_at_title = get_attribute_title_from_id(ex_at_id)
                attribute_similarity = semantic_matching.semantic_coeficient(
                    at_title, ex_at_title)

                if attribute_similarity >= 0.5:
                    at_value = get_attribute_value_from_id(at_id)
                    ex_at_value = get_attribute_value_from_id(ex_at_id)
                    value_similarity = semantic_matching.semantic_coeficient(
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

    existing_rels = objects.get("relationships")
    rel_type_id = rel.get_type()
    rel_type = get_relationship_type_title_from_id(rel_type_id)
    source_id = rel.get_source_id()
    target_id = rel.get_target_id()

    for existing_rel in existing_rels:
        existing_source_id = existing_rel.get_source_id()
        existing_target_id = existing_rel.get_target_id()

        if existing_source_id == source_id and existing_target_id == target_id:
            existing_rel_type_id = existing_rel.get_type()
            existing_rel_type = get_relationship_type_title_from_id(
                existing_rel_type_id)
            type_similarity = semantic_matching.semantic_coeficient(
                rel_type, existing_rel_type)
            if type_similarity >= 0.5 and type_similarity < 0.9:
                attributes = rel.get_attributes()
                existing_attributes = existing_rel.get_attributes()
                total_attributes = len(attributes)
                equal_attributes = 0

                for at_id in attributes:
                    at_title = get_attribute_title_from_id(at_id)
                    ex_at_id = find_most_similar_attribute(
                        at_title, existing_attributes)
                    ex_at_title = get_attribute_title_from_id(ex_at_id)
                    attribute_similarity = semantic_matching.semantic_coeficient(
                        at_title, ex_at_title)

                    if attribute_similarity >= 0.5:
                        at_value = get_attribute_value_from_id(at_id)
                        ex_at_value = get_attribute_value_from_id(ex_at_id)
                        value_similarity = semantic_matching.semantic_coeficient(
                            at_value, ex_at_value)

                        if value_similarity >= 0.8:
                            equal_attributes += 1

                if total_attributes > 0:
                    ratio = (equal_attributes*100)/total_attributes
                else:
                    ratio = type_similarity * 100
                if ratio > max_ratio:
                    max_ratio = ratio
                    equal_rel = existing_rel
            elif type_similarity > 0.9:
                ratio = type_similarity * 100
                if ratio > max_ratio:
                    max_ratio = ratio
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


def ci_type_already_exists(title):
    equal = None
    max_ratio = 0
    existing_types = objects["configuration_item_types"]

    for t in existing_types:
        t_name = t.get_title()
        sim = similarity.calculate_similarity(t_name, title)
        if sim > max_ratio:
            max_ratio = sim
            equal = t

    if max_ratio > 0.9:
        return equal
    else:
        return None


def rel_type_already_exists(title):
    equal = None
    max_ratio = 0
    existing_types = objects["relationship_types"]

    for t in existing_types:
        t_name = t.get_title()
        sim = similarity.calculate_similarity(t_name, title)
        if sim > max_ratio:
            max_ratio = sim
            equal = t

    if max_ratio > 0.9:
        return equal
    else:
        return None


def add_ci(ci):
    # TODO: verificar se já existe
    objects["configuration_items"].append(ci)


def add_rel(rel):
    print("Adding rel: " + str(rel.get_title()))
    if rel != None:
        exists = relationship_already_exists(rel)
        print("Existing one: " + str(exists))
        if exists != None:
            new = reconciliation.reconcile_relationships(rel, exists)
            delete_relationship(exists)
            objects["relationships"].append(new)
        else:
            objects["relationships"].append(rel)


def add_ci_type(ci_type):
    if ci_type != None:
        objects["configuration_item_types"].append(ci_type)


def add_rel_type(rel_type):
    if rel_type != None:
        objects["relationship_types"].append(rel_type)


def add_attribute(attr):
    if attr != None:
        objects["attributes"].append(attr)
