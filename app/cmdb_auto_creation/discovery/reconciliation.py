#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from colored import fg, bg, attr

from objects import objects
from models import Element, Relation

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# como saber que dois objectos representam a mesma entidade física?
# número de série, Universally Unique Identifiers (UUIDs) e nomes


def check_same(obj1, obj2):
    if type(obj1) is Element:
        if obj1.serial_number == obj2.serial_number and obj1.serial_number != "":
            return True
        elif obj1.ci_type == obj2.ci_type and obj1.ci_type != "":
            if obj1.value == obj2.value and obj1.value != "":
                return True
            elif obj1.hostname == obj2.hostname and obj1.hostname != "":
                return True
            elif obj1.name == obj2.name and obj1.name != "":
                return True
    elif type(obj1) is Relation:
        if obj1.rel_type == obj2.rel_type and obj1.rel_type != "":
            if obj1.source_id == obj2.source_id and obj1.source_id != "":
                if obj1.target_id == obj2.target_id and obj1.target_id != "":
                    return True
    return False

# TODO: quando "elimino" um objeto tenho de ver os relacionamentos já criados também!


def reconcile(objs):
    print(blue + ">>> " + reset + "Reconciling objects...")
    for obj1 in objs:
        x = False
        t1 = type(obj1)
        for obj2 in objects:
            t2 = type(obj2)
            if t1 == t2:
                if check_same(obj1, obj2) == True:
                    print(blue + ">>> " + reset +
                          "Find an existing object...")
                    x = True
                    if type(obj1) is Element:
                        if obj1.ci_type != "":
                            obj2.ci_type = obj1.ci_type
                        if obj1.name != "":
                            obj2.name = obj1.name
                        if obj1.value != "":
                            obj2.value = obj1.value
                        if obj1.status != "":
                            obj2.status = obj1.status
                        if obj1.description != "":
                            obj2.description = obj1.description
                    elif type(obj1) is Relation:
                        if obj1.rel_type != "":
                            obj2.rel_type = obj1.rel_type
                        if obj1.source_id != "":
                            obj2.source_id = obj1.source_id
                        if obj1.source_type != "":
                            obj2.source_type = obj1.source_type
                        if obj1.target_id != "":
                            obj2.target_id = obj1.target_id
                        if obj1.target_type != "":
                            obj2.target_type = obj1.target_type
        if x == False:
            print(blue + ">>> " + reset + "New object added...")
            objects.append(obj1)


"""
            generation = ""
            install_date = ""
            availability = ""
            serial_number = ""
            version = ""
            model = ""
            manufacturer = ""
            number = ""
            hostname = ""
            management_address = ""
            connectivity_status = ""
            net_mask = ""
            net_number = ""
            type_ = ""
            size = ""
            layout = ""
            bandwidth = ""
            height = ""
            width = ""
            speed = ""
            resolution = ""
            business_category = ""
            email = ""
            fax = ""
            mobile_phone = ""
            department = ""
            title = ""
            webpage = ""
            core_number = ""
            architecture = ""
            family = ""
            power = ""
            ip_range = ""
            capacity = ""
            removable = ""
            block_size = ""
            number_of_blocks = ""
            compression_method = ""
            transfer_rate = ""
            address = ""
            city = ""
            price = ""
            available_space = ""
            max_number_of_processes = ""
            author = ""
            filename = ""
            date = ""
            path = ""
            provider = ""
"""
