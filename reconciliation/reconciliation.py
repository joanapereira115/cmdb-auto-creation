# -*- coding: utf-8 -*-

from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from model_mapper import mapper, mapping


def combine_attributes(new_at, prev_at):
    res = []
    for prev in prev_at:
        at_id, sim = methods.find_most_similar_attribute(
            prev.get_title(), [at.get_id() for at in new_at])
        if sim < 0.9:
            res.append(prev.get_id())
    return res


def reconcile_relationships(new, prev):
    new_title = new.get_title()
    if new_title == None or new_title == "":
        prev_title = prev.get_title()
        if prev_title != None and prev_title != "":
            new.set_title(prev_title)

    new_type = new.get_type()
    if new_type == None or new_type == 0:
        prev_type = prev.get_type()
        if prev_type != None and prev_type != 0:
            new.set_type(prev_type)

    new_at = [methods.get_attribute_from_id(at) for at in new.get_attributes()]
    prev_at = [methods.get_attribute_from_id(
        at) for at in prev.get_attributes()]

    combined = combine_attributes(new_at, prev_at)

    for at_id in combined:
        new.add_attribute(at_id)

    return new


def change_ids(old, new):
    rels = objects.objects.get("relationships")
    for rel in rels:
        source = rel.get_source_id()
        if source == old:
            rel.set_source_id(new)
        target = rel.get_target_id()
        if target == old:
            rel.set_target_id(new)


def reconcile_configuration_items(new, prev):

    new_uuid = new.get_uuid()
    if new_uuid == None or new_uuid == "":
        prev_uuid = prev.get_uuid()
        if prev_uuid != None and prev_uuid != "":
            new.set_uuid(prev_uuid)

    new_serial_number = new.get_serial_number()
    if new_serial_number == None or new_serial_number == "":
        prev_serial_number = prev.get_serial_number()
        if prev_serial_number != None and prev_serial_number != "":
            new.set_serial_number(prev_serial_number)

    new_title = new.get_title()
    if new_title == None or new_title == "":
        prev_title = prev.get_title()
        if prev_title != None and prev_title != "":
            new.set_title(prev_title)

    new_description = new.get_description()
    prev_description = prev.get_description()
    if prev_description != None and prev_description != "":
        desc = new_description + prev_description
        new.set_description(desc)

    new_status = new.get_status()
    if new_status == None or new_status == "":
        prev_status = prev.get_status()
        if prev_status != None and prev_status != "":
            new.set_status(prev_status)

    new_mac_address = new.get_mac_address()
    if new_mac_address == None or new_mac_address == "":
        prev_mac_address = prev.get_mac_address()
        if prev_mac_address != None and prev_mac_address != "":
            new.set_mac_address(prev_mac_address)

    new_type = new.get_type()
    if new_type == None or new_type == 0:
        prev_type = prev.get_type()
        if prev_type != None and prev_type != 0:
            new.set_type(prev_type)

    for ip4 in prev.get_ipv4_addresses():
        if ip4 not in new.get_ipv4_addresses():
            new.add_ipv4_address(ip4)

    for ip6 in prev.get_ipv6_addresses():
        if ip6 not in new.get_ipv6_addresses():
            new.add_ipv6_address(ip6)

    new_at = [methods.get_attribute_from_id(at) for at in new.get_attributes()]
    prev_at = [methods.get_attribute_from_id(
        at) for at in prev.get_attributes()]

    combined = combine_attributes(new_at, prev_at)

    for at_id in combined:
        new.add_attribute(at_id)

    change_ids(prev.get_id(), new.get_id())

    return new
