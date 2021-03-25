# -*- coding: utf-8 -*-

import regex
import json
import requests
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def location_discovery(client, ci):
    """
    Gathers information about the location of the OS X machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.
    """
    r = requests.get('https://freegeoip.app/json/')
    loc_info = r.json()
    ip = loc_info.get("ip")
    if ip == None:
        print(red + ">>> " + reset +
              "An error has ocurred finding the machine location.\n")
    else:
        ipv6 = regex.search(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', ip)
        ipv4 = regex.search(
            r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])', ip)
        mac = regex.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', ip)

        if ipv6 != None:
            ci.add_ipv6_address(ip)
        elif ipv4 != None:
            ci.add_ipv4_address(ip)
        elif mac != None:
            ci.set_mac_address(ip)

    loc_type = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType("Location"))

    obj = ConfigurationItem.ConfigurationItem()
    obj.set_title(loc_info.get("country_code"))
    obj.set_type(loc_type.get_id())

    methods.define_attribute("country", loc_info.get("country_name"), obj)
    methods.define_attribute("region", loc_info.get("region_name"), obj)
    methods.define_attribute("city", loc_info.get("city"), obj)
    methods.define_attribute("zip_code", loc_info.get("zip_code"), obj)
    methods.define_attribute("time_zone", loc_info.get("time_zone"), obj)
    methods.define_attribute("latitude", loc_info.get("latitude"), obj)
    methods.define_attribute("longitude", loc_info.get("longitude"), obj)

    rel_type_ci_obj = methods.add_rel_type(
        RelationshipType.RelationshipType("located"))
    rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
    rel_ci_obj.title = str(ci.get_title()) + \
        " located " + str(obj.get_title())

    rel_type_obj_ci = methods.add_rel_type(
        RelationshipType.RelationshipType("location of"))
    rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
    rel_obj_ci.title = str(obj.get_title()) + \
        " location of " + str(ci.get_title())

    methods.add_ci(obj)
    methods.add_rel(rel_ci_obj)
    methods.add_rel(rel_obj_ci)
