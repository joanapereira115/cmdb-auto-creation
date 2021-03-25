# -*- coding: utf-8 -*-

from colored import fg, attr
import regex

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def processing_discovery(client, ci):
    """
    Gathers information about the CPU of the Linux machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the Linux machine that is going to be explored.

    """
###########################################
    _, stdout, stderr = client.exec_command("lscpu")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        cpu_info = stdout.readlines()

        cpu_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("CPU"))

        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(cpu_type.get_id())

        info = {}
        if len(cpu_info) > 0:
            for pair in cpu_info:
                info[pair.split(": ")[0]] = pair.split(": ")[1].strip()

        for at in info:
            if at == "Model name":
                obj.set_title(info.get(at))
                methods.define_attribute("CPU", info.get(at), ci)
            if at == "CPU(s)":
                methods.define_attribute(at, info.get(at), obj)
                methods.define_attribute("CPU cores", info.get(at), ci)
            else:
                methods.define_attribute(at, info.get(at), obj)

        rel_type_ci_obj = methods.add_rel_type(
            RelationshipType.RelationshipType("associated processor"))
        rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
        rel_ci_obj.title = str(ci.get_title()) + \
            " associated processor " + str(obj.get_title())

        rel_type_obj_ci = methods.add_rel_type(
            RelationshipType.RelationshipType("processor of"))
        rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
        rel_obj_ci.title = str(obj.get_title()) + \
            " processor of " + str(ci.get_title())

        methods.add_ci(obj)
        methods.add_rel(rel_ci_obj)
        methods.add_rel(rel_obj_ci)
###########################################
