# -*- coding: utf-8 -*-

from . import Relationship
from . import ConfigurationItem
from . import Attribute
from .objects import objects
from similarity import similarity
from reconciliation import reconciliation
from normalization import normalization


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
    Attribute, None
        The attribute, or None if the attribute does not exists.
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
    string, None
        The title of the attribute, or None if the attribute does not exists.
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
            attribute_similarity = similarity.calculate_similarity(
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

        if ci_serial != None and ci_serial != "" and ci_serial == ex_ci_serial:
            return existing_ci

        if ci_mac != None and ci_mac != "" and ci_mac == ex_ci_mac:
            return existing_ci

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

                print("Titles:")
                ci_title = ci.get_title()
                print(ci_title)
                ex_ci_title = existing_ci.get_title()
                print(ex_ci_title)

                title_sim = similarity.calculate_similarity(
                    str(ci_title), str(ex_ci_title))
                total += 1
                print(title_sim)

                if title_sim >= 0.9:
                    equal += 1

                    attributes = ci.get_attributes()
                    ex_attributes = existing_ci.get_attributes()

                    if len(attributes) > len(ex_attributes):
                        total += len(ex_attributes)
                    else:
                        total += len(attributes)

                    for at_id in attributes:
                        print("Attribute name:")
                        at_title = get_attribute_title_from_id(at_id)
                        ex_at_id, sim = find_most_similar_attribute(
                            at_title, ex_attributes)
                        ex_at_title = get_attribute_title_from_id(ex_at_id)
                        attribute_similarity = similarity.calculate_similarity(
                            at_title, ex_at_title)
                        print(at_title)
                        print(ex_at_title)
                        print(attribute_similarity)

                        if attribute_similarity >= 0.7:
                            print("Attribute value:")
                            total += 1
                            at_value = get_attribute_value_from_id(at_id)
                            ex_at_value = get_attribute_value_from_id(ex_at_id)
                            value_similarity = similarity.calculate_similarity(
                                at_value, ex_at_value)

                            print(at_value)
                            print(ex_at_value)
                            print(value_similarity)

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

            type_similarity = similarity.calculate_similarity(
                rel_type, ex_rel_type)
            if type_similarity >= 0.9:
                if type_similarity > max_ratio:
                    max_ratio = type_similarity
                    equal_rel = existing_rel

    return equal_rel


def ci_type_already_exists(title):
    """
    Finds out if a configuration item type already exists.
    Goes through the existing configuration item types and calculates the similarity between the titles, to find out if
    they are similar enough to be considered the same.

    Parameters
    ----------
    title : string
        The title of the configuration item type.

    Returns
    -------
    ConfiguratioItemType, None
        The existing configuration item type, or None if it wasn't found a onfiguration item type similar enough.
    """
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
    """
    Finds out if a relationship type already exists.
    Goes through the existing relationship types and calculates the similarity between the titles, to find out if
    they are similar enough to be considered the same.

    Parameters
    ----------
    title : string
        The title of the relationship type.

    Returns
    -------
    RelationshipType, None
        The existing relationship type, or None if it wasn't found a onfiguration item type similar enough.
    """
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
    """
    Adds a new configuration item, reconciling if the same object already exists.

    Parameters
    ----------
    ci : ConfiguratioItem
        The configuration item.
    """
    if ci != None:
        print()
        print("adding ci")
        exists = ci_already_exists(ci)
        print()
        print(ci.get_title())
        print(exists)
        if exists != None:
            print(exists.get_title())
            new = reconciliation.reconcile_configuration_items(ci, exists)
            delete_configuration_item(exists)
            objects["configuration_items"].append(new)
        else:
            objects["configuration_items"].append(ci)


def add_rel(rel):
    """
    Adds a new relationship, reconciling if the same object already exists.

    Parameters
    ----------
    rel : Relationship
        The relationship.
    """
    if rel != None:
        exists = relationship_already_exists(rel)
        if exists != None:
            new = reconciliation.reconcile_relationships(rel, exists)
            delete_relationship(exists)
            objects["relationships"].append(new)
        else:
            objects["relationships"].append(rel)


def add_ci_type(ci_type):
    """
    Adds a new configuration item type, if it does not already exists.

    Parameters
    ----------
    ci_type : ConfiguratioItemType
        The configuration item type.

    Returns 
    ----------
    ConfiguratioItemType
        The same object, or the already existing one.
    """
    ex_ci_type = ci_type_already_exists(ci_type.get_title())
    if ex_ci_type != None:
        return ex_ci_type
    else:
        ci_type.set_title(
            normalization.parse_text_to_store(ci_type.get_title()))
        objects["configuration_item_types"].append(ci_type)
        return ci_type


def add_rel_type(rel_type):
    """
    Adds a new relationship type, if it does not already exists.

    Parameters
    ----------
    rel_type : RelationshipType
        The relationship type.

    Returns 
    ----------
    RelationshipType
        The same object, or the already existing one.
    """
    ex_rel_type = rel_type_already_exists(rel_type.get_title())
    if ex_rel_type != None:
        return ex_rel_type
    else:
        rel_type.set_title(
            normalization.parse_text_to_store(rel_type.get_title()))
        objects["relationship_types"].append(rel_type)
        return rel_type


def add_attribute(attr, obj):
    """
    Adds a new attribute to an object, if it does not already exists.

    Parameters
    ----------
    attr : Attribute
        The attribute.

    obj : ConfigurationItem or Relationship
        The object.
    """
    title = attr.get_title()

    equal = None
    max_ratio = 0
    existing_attrs = obj.get_attributes()

    for i in existing_attrs:
        a = get_attribute_from_id(i)
        a_name = a.get_title()
        sim = similarity.calculate_similarity(a_name, title)
        if sim > max_ratio:
            max_ratio = sim
            equal = a

    if max_ratio > 0.9:
        equal.set_value(attr.get_value())
    else:
        obj.add_attribute(attr.get_id())
        objects["attributes"].append(attr)


def create_relation(source, target, relation_type):
    """
    Creates a new reltionship between two configuration items.

    Parameters
    ----------
    source : ConfigurationItem
        The source configuration item involved in the relationship.

    target : ConfigurationItem
        The target configuration item involved in the relationship.

    relation_type : RelationshipType
        The type of the relationship.

    Returns
    ----------
    Relationship, None
        Returns the relationship, or None if the source, target or type weren't valid.
    """
    if source != None and target != None and relation_type != None:
        rel = Relationship.Relationship()
        rel.type_id = relation_type.get_id()
        rel.source_id = source.get_id()
        rel.target_id = target.get_id()
        return rel
    else:
        return None


def create_attribute(name, value):
    """
    Creates a new attribute.

    Parameters
    ----------
    name : string
        The name of the attribute.

    value : string
        The value of the attribute.

    Returns
    ----------
    Attribute, None
        Returns the attribute, or None if the name or value weren't valid.
    """
    if value != None and value != "":
        attr = Attribute.Attribute(name, value)
        return attr
    else:
        return None


def define_attribute(title, value, ci):
    """
    Adds a new attribute to an configuration item.

    Parameters
    ----------
    title : string
        The name of the attribute.

    value : string
        The value of the attribute.

    ci : ConfigurationItem
        The configuration item.
    """
    if title != None and title != "" and value != None and value != "":
        if similarity.calculate_similarity(title, "uuid") > 0.85:
            ci.set_uuid(value)
        elif similarity.calculate_similarity(title, "serial_number") > 0.85:
            ci.set_serial_number(value)
        elif similarity.calculate_similarity(title, "description") > 0.85:
            ci.set_description(value)
        elif similarity.calculate_similarity(title, "status") > 0.85:
            ci.set_status(value)
        elif similarity.calculate_similarity(title, "mac address") > 0.85:
            ci.set_mac_address(value)
        elif similarity.calculate_similarity(title, "ipv4 address") > 0.85:
            ci.add_ipv4_address(value)
        elif similarity.calculate_similarity(title, "ipv6 address") > 0.85:
            ci.add_ipv6_address(value)
        else:
            atr = create_attribute(
                title, normalization.parse_text_to_store(value))
            add_attribute(atr, ci)
