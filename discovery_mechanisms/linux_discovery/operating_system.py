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
    _, stdout, stderr = client.exec_command("cat /etc/os-release")
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
            if at == "NAME":
                obj.set_title(info.get(at))
            else:
                methods.define_attribute(at, info.get(at), obj)
###########################################
    _, stdout, stderr = client.exec_command("hostnamectl")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        hostnamectl = stdout.readlines()
        info = {}
        if len(hostnamectl) > 0:
            for line in hostnamectl:
                info[regex.sub("\n|\"", "", line.split(":")[0]).strip()] = regex.sub(
                    "\n|\"", "", line.split(":")[1]).strip()
        for at in info:
            methods.define_attribute(at, info.get(at), obj)
###########################################

    rel_type_ci_obj = methods.add_rel_type(
        RelationshipType.RelationshipType("running operating system"))
    rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
    rel_ci_obj.title = str(ci.get_title()) + \
        " running operating system " + str(obj.get_title())

    rel_type_obj_ci = methods.add_rel_type(
        RelationshipType.RelationshipType("installed operating system"))
    rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
    rel_obj_ci.title = str(obj.get_title()) + \
        " installed operating system " + str(ci.get_title())

    methods.add_ci(obj)
    methods.add_rel(rel_ci_obj)
    methods.add_rel(rel_obj_ci)