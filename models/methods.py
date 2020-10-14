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
    max_ = 0
    for at in attributes_titles:
        at_title2 = attributes_titles.get(at)
        if at_title2 != None and at_title != None:
            attribute_similarity = semantic_matching.semantic_coeficient(
                at_title, at_title2)
        else:
            attribute_similarity = 0
        if attribute_similarity > max_:
            res = at
            max_ = attribute_similarity

    return res, max_


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

    ci_uuid = ci.get_uuid()
    ci_serial = ci.get_serial_number()
    ci_mac = ci.get_mac_address()

    existing_cis = objects.get("configuration_items")

    for existing_ci in existing_cis:

        ex_ci_uuid = existing_ci.get_uuid()
        ex_ci_serial = existing_ci.get_serial_number()
        ex_ci_mac = existing_ci.get_mac_address()

        if ci_uuid != None and ci_uuid != "" and ci_uuid == ex_ci_uuid:
            return existing_ci
        if ci_uuid != None and ci_uuid != "" and ex_ci_uuid != None and ex_ci_uuid != "" and ci_uuid != ex_ci_uuid:
            return None

        if ci_serial != None and ci_serial != "" and ci_serial == ex_ci_serial:
            return existing_ci
        if ci_serial != None and ci_serial != "" and ex_ci_serial != None and ex_ci_serial != "" and ci_serial != ex_ci_serial:
            return None

        if ci_mac != None and ci_mac != "" and ci_mac == ex_ci_mac:
            return existing_ci
        if ci_mac != None and ci_mac != "" and ex_ci_mac != None and ex_ci_mac != "" and ci_mac != ex_ci_mac:
            return None

        if (ci_uuid == "" or ci_uuid == None) and (ci_serial == "" or ci_serial == None) and (ci_mac == "" or ci_mac == None):
            ci_ipv4 = ci.get_ipv4_addresses()
            ci_ipv6 = ci.get_ipv6_addresses()

            ex_ci_ipv4 = existing_ci.get_ipv4_addresses()
            ex_ci_ipv6 = existing_ci.get_ipv6_addresses()

            total = len(ci_ipv4) + len(ci_ipv6)
            equal = 0

            for ip4 in ci_ipv4:
                if ip4 in ex_ci_ipv4:
                    equal += 1
            for ip6 in ci_ipv6:
                if ip6 in ex_ci_ipv6:
                    equal += 1

            if total > 0:
                ratio = (equal*100)/total

            else:
                total = 0
                equal = 0

                ci_title = ci.get_title()
                ex_ci_title = existing_ci.get_title()

                title_sim = similarity.calculate_similarity(
                    str(ci_title), str(ex_ci_title))
                total += 1

                if title_sim >= 0.9:
                    equal += 1

                    attributes = ci.get_attributes()
                    ex_attributes = existing_ci.get_attributes()

                    if len(attributes) > len(ex_attributes):
                        total += len(ex_attributes)
                    else:
                        total += len(attributes)

                    for at_id in attributes:
                        at_title = get_attribute_title_from_id(at_id)
                        ex_at_id, sim = find_most_similar_attribute(
                            at_title, ex_attributes)
                        ex_at_title = get_attribute_title_from_id(ex_at_id)
                        attribute_similarity = semantic_matching.semantic_coeficient(
                            at_title, ex_at_title)

                        if attribute_similarity >= 0.7:
                            total += 1
                            at_value = get_attribute_value_from_id(at_id)
                            ex_at_value = get_attribute_value_from_id(ex_at_id)
                            value_similarity = semantic_matching.semantic_coeficient(
                                at_value, ex_at_value)

                            if value_similarity >= 0.8:
                                equal += 1

                if total != 0:
                    ratio = (equal*100)/total
                else:
                    ratio = 0

            if ratio > max_ratio:
                equal_ci = existing_ci
                max_ratio = ratio

    if max_ratio > 80:
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
    rel_type = get_relationship_type_title_from_id(rel.get_type())
    source_id = rel.get_source_id()
    target_id = rel.get_target_id()

    for existing_rel in existing_rels:
        ex_source_id = existing_rel.get_source_id()
        ex_target_id = existing_rel.get_target_id()

        if ex_source_id == source_id and ex_target_id == target_id:
            ex_rel_type = get_relationship_type_title_from_id(
                existing_rel.get_type())

            type_similarity = semantic_matching.semantic_coeficient(
                rel_type, ex_rel_type)
            if type_similarity >= 0.9:
                if type_similarity > max_ratio:
                    max_ratio = type_similarity
                    equal_rel = existing_rel

    return equal_rel


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
    if ci != None:
        exists = ci_already_exists(ci)
        if exists != None:
            new = reconciliation.reconcile_configuration_items(ci, exists)
            delete_configuration_item(exists)
            objects["configuration_items"].append(new)
        else:
            objects["configuration_items"].append(ci)


def add_rel(rel):
    if rel != None:
        exists = relationship_already_exists(rel)
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
