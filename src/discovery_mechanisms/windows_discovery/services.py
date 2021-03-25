# -*- coding: utf-8 -*-

import regex
import requests
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def services_discovery(client, ci):
    """
    Gathers information about the services running in the machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the Windows machine that is going to be explored.

    """
    r = client.run_cmd(
        'wmic service where (state=\"running\") GET caption, description, displayname, name, processid, status', [])
    lines = r.std_out.decode("Windows-1251")
    lines = lines.split("\n")
    fields = lines[0]
    # gets only the first 10 services
    values = lines[1:11]
    fields = [f for f in fields.split(
        " ") if f != "" and regex.search(r'\w', f) != None]

    for vals in values:
        serv_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Service"))
        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(serv_type.get_id())

        v = [t for t in vals.split(
            "    ") if t != "" and regex.search(r'\w', t) != None]
        for i in range(0, min(len(fields), len(v))):
            field = fields[i].strip(" ")
            value = v[i].strip(" ")
            methods.define_attribute(field, value, obj)

        rel_type_ci_obj = methods.add_rel_type(
            RelationshipType.RelationshipType("running service"))
        rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
        rel_ci_obj.title = str(ci.get_title()) + \
            " running service " + str(obj.get_title())

        rel_type_obj_ci = methods.add_rel_type(
            RelationshipType.RelationshipType("running on"))
        rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
        rel_obj_ci.title = str(obj.get_title()) + \
            " running on " + str(ci.get_title())

        methods.add_ci(obj)
        methods.add_rel(rel_ci_obj)
        methods.add_rel(rel_obj_ci)
