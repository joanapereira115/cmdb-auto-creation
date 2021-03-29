# -*- coding: utf-8 -*-

import json
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def os_discovery(client, ci):
    """
    Gathers information about the OS X operating system of the machine that is being explored.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.

    """
    os_type = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType("Operating System"))
    obj = ConfigurationItem.ConfigurationItem()
    obj.set_type(os_type.get_id())
###########################################
    _, stdout, stderr = client.exec_command("sw_vers -productName")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        os_name = stdout.readlines()
        if len(os_name) > 0:
            value = os_name[0].strip('\n')
            methods.define_attribute("os name", value, ci)
            methods.define_attribute("os family", value, obj)
###########################################
    _, stdout, stderr = client.exec_command("sw_vers -productVersion")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        os_version = stdout.readlines()
        if len(os_version) > 0:
            value = os_version[0].strip('\n')
            methods.define_attribute("os version", value, ci)
            methods.define_attribute("version number", value, obj)
###########################################
    _, stdout, stderr = client.exec_command("sw_vers -buildVersion")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        os_build = stdout.readlines()
        if len(os_build) > 0:
            value = os_build[0].strip('\n')
            methods.define_attribute("build version", value, obj)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPSoftwareDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        os = stdout.readlines()
        os_info = json.loads("".join(os)).get('SPSoftwareDataType')[0]

        methods.define_attribute(
            "kernel version", os_info.get("kernel_version"), ci)
        methods.define_attribute(
            "kernel version", os_info.get("kernel_version"), ci)
        obj.set_title(os_info.get("os_version"))
        methods.define_attribute("os", os_info.get("os_version"), ci)
        methods.define_attribute(
            "boot mode", os_info.get("boot_mode"), ci)
        methods.define_attribute(
            "time since boot", os_info.get("uptime"), ci)

        ci.set_title(os_info.get("local_host_name"))

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
