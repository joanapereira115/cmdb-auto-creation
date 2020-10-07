# -*- coding: utf-8 -*-

from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from model_mapper import mapper, mapping


def reconcile_relationships(new, prev):
    new_at = [methods.get_attribute_title_from_id(
        at) for at in new.get_attributes()]
    prev_at = [methods.get_attribute_title_from_id(
        at) for at in prev.get_attributes()]
    similarity = mapper.calculate_class_similarity(new_at, prev_at)
    similars = mapping.select_most_similar(similarity)
    print(similars)
    return new

    #value = methods.get_attribute_value_from_id(at)


def reconcile_configuration_items(new, prev):
    # verificar os atributos
    pass
