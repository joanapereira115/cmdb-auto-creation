# -*- coding: utf-8 -*-

from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from model_mapper import mapper, mapping


def reconcile_relationships(new, prev):
    new_at = new.get_attributes()
    print("new_at: " + str(new_at))
    prev_at = [at for at in prev.get_attributes() if at != None]
    print("prev_at: " + str(prev_at))
    for at in new_at:
        if at != None:
            at_title = methods.get_attribute_value_from_id(at)
            ex_at_id = methods.find_most_similar_attribute(at_title, prev_at)
            atr = methods.get_attribute_from_id(at)
            if atr != None:
                methods.get_attribute_from_id(ex_at_id).value = atr.get_value()
            # TODO: remover o anterior da lista

    return new

    #value = methods.get_attribute_value_from_id(at)


def reconcile_configuration_items(new, prev):
    # verificar os atributos
    pass
