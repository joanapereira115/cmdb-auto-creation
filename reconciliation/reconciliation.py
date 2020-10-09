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
    new_at = [methods.get_attribute_from_id(at) for at in new.get_attributes()]
    prev_at = [methods.get_attribute_from_id(
        at) for at in prev.get_attributes()]

    combined = combine_attributes(new_at, prev_at)

    for at_id in combined:
        new.add_attribute(at_id)

    change_ids(prev.get_id(), new.get_id())

    return new
