# -*- coding: utf-8 -*-

from colored import fg, attr
import regex

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def os_discovery(client, ci):
    """
    Gathers information about the Linux operating system of the machine that is being explored.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the Linux machine that is going to be explored.

    """
    os_type = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType("Operating System"))
    obj = ConfigurationItem.ConfigurationItem()
    obj.set_type(os_type.get_id())
###########################################
    _, stdout, stderr = client.exec_command("cat /etc/*-release")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        os_name = stdout.readlines()
        info = {}
        if len(os_name) > 0:
            for line in os_name:
                info[regex.sub("\n|\"", "", line.split("=")[0])] = regex.sub(
                    "\n|\"", "", line.split("=")[1])
        for at in info:
            if at == "PRETTY_NAME":
                obj.set_title(info.get(at))
                methods.define_attribute("os name", info.get(at), ci)
            elif at == "NAME":
                methods.define_attribute("os family", info.get(at), ci)
            elif at == "VERSION_ID":
                methods.define_attribute("version number", info.get(at), obj)
                methods.define_attribute("os version", info.get(at), ci)
            elif at == "DISTRIB_ID":
                methods.define_attribute("vendor", info.get(at), obj)
            else:
                methods.define_attribute(at, info.get(at), obj)
###########################################
    rel_type_ci_obj = methods.add_rel_type(
        RelationshipType.RelationshipType("installed os"))
    rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
    rel_ci_obj.title = str(ci.get_title()) + \
        " installed os " + str(obj.get_title())

    rel_type_obj_ci = methods.add_rel_type(
        RelationshipType.RelationshipType("running os"))
    rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
    rel_obj_ci.title = str(obj.get_title()) + \
        " running os " + str(ci.get_title())

    methods.add_ci(obj)
    methods.add_rel(rel_ci_obj)
    methods.add_rel(rel_obj_ci)
