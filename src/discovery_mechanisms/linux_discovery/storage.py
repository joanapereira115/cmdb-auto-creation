# -*- coding: utf-8 -*-

import json
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def storage_discovery(client, ci):
    """
    Gathers information about the storage of the Linux machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the Linux machine that is going to be explored.
    """
    _, stdout, stderr = client.exec_command("/sbin/blkid")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        memory = stdout.readlines()
        if len(memory) > 0:
            memory = memory[0]
        name = memory.split(":")[0]
        info = memory.split(":")[1].split()
        attrs = {}
        for pair in info:
            attrs[pair.split("=")[0]] = pair.split("=")[1].strip("\"")
##################################################################
        _, stdout, stderr = client.exec_command("df " + str(name))
        error = stderr.read().decode('utf-8')
        if error != "":
            print(red + ">>> " + reset + str(error) + "\n")
        else:
            memory = stdout.readlines()
            if len(memory) > 1:
                names = ['Filesystem', '1K-blocks', 'Used',
                         'Available', 'Use%', 'Mounted on']
                memory = memory[1].split()
            for i in range(len(names)):
                attrs[names[i]] = memory[i]
##################################################################
        _, stdout, stderr = client.exec_command("lsblk " + str(name))
        error = stderr.read().decode('utf-8')
        if error != "":
            print(red + ">>> " + reset + str(error) + "\n")
        else:
            memory = stdout.readlines()
            if len(memory) > 1:
                names = ['NAME', 'MAJ:MIN', 'RM',
                         'SIZE', 'RO', 'TYPE', 'MOUNTPOINT']
                memory = memory[1].split()
            for i in range(len(names)):
                if i < len(memory):
                    attrs[names[i]] = memory[i]

            obj = ConfigurationItem.ConfigurationItem()

            mem_type = None
            for at in attrs:
                if at == "RO":
                    if attrs.get(at) == 0:
                        mem_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType("SSD"))
                    elif attrs.get(at) == 1:
                        mem_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType("HDD"))

                methods.define_attribute(at, attrs.get(at), obj)

            if mem_type != None:
                obj.set_type(mem_type.get_id())
                rel_type_ci_obj = methods.add_rel_type(
                    RelationshipType.RelationshipType("has storage"))
                rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
                rel_ci_obj.title = str(ci.get_title()) + \
                    " has storage " + str(obj.get_title())

                rel_type_obj_ci = methods.add_rel_type(
                    RelationshipType.RelationshipType("is storage of"))
                rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
                rel_obj_ci.title = str(obj.get_title()) + \
                    " is storage of " + str(ci.get_title())

                methods.add_rel(rel_ci_obj)
                methods.add_rel(rel_obj_ci)
                methods.add_ci(obj)
