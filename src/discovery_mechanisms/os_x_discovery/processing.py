# -*- coding: utf-8 -*-

import json
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def processing_discovery(client, ci):
    """
    Gathers information about the GPU and CPU of the OS X machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.

    """
    _, stdout, stderr = client.exec_command(
        "system_profiler SPHardwareDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        hw = stdout.readlines()
        hw_info = json.loads("".join(hw)).get('SPHardwareDataType')[0]

        cpu_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("CPU"))

        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(cpu_type.get_id())

        obj.set_title(hw_info.get("cpu_type"))
        methods.define_attribute("CPU", hw_info.get("cpu_type"), ci)
        methods.define_attribute("Speed", hw_info.get(
            "current_processor_speed"), obj)
        methods.define_attribute("Number of Cores",
                                 hw_info.get("number_processors"), obj)
        methods.define_attribute("L2 Cache",
                                 hw_info.get("l2_cache_core"), obj)
        methods.define_attribute("L3 Cache", hw_info.get("l3_cache"), obj)
        methods.define_attribute("SMC Version",
                                 hw_info.get("SMC_version_system"), obj)

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
    _, stdout, stderr = client.exec_command(
        "system_profiler SPDisplaysDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        display = stdout.readlines()
        display_info = json.loads("".join(display)).get('SPDisplaysDataType')

        for graph in display_info:
            graph_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("GPU"))

            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(graph_type.get_id())

            obj.set_title(graph.get("_name"))
            methods.define_attribute("GPU", graph.get("_name"), ci)

            methods.define_attribute("Chipset Model", graph.get(
                "sppci_model"), obj)
            methods.define_attribute("Bus", graph.get("sppci_bus"), obj)
            methods.define_attribute(
                "VRAM", graph.get("_spdisplays_vram"), obj)
            methods.define_attribute(
                "Device ID", graph.get("spdisplays_device"), obj)
            methods.define_attribute("Revision ID",
                                     graph.get("spdisplays_revision-id"), obj)
            methods.define_attribute("VRAM shared",
                                     graph.get("spdisplays_vram_shared"), obj)

            vendor = graph.get("spdisplays_vendor")
            vendor_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Vendor"))
            vendor_obj = ConfigurationItem.ConfigurationItem()
            vendor_obj.set_title(vendor)
            vendor_obj.set_type(vendor_type.get_id())

            rel_type_obj_vendor = methods.add_rel_type(
                RelationshipType.RelationshipType("has vendor"))
            rel_obj_vendor = methods.create_relation(
                obj, vendor_obj, rel_type_obj_vendor)
            rel_obj_vendor.title = str(obj.get_title()) + \
                " has vendor " + str(vendor_obj.get_title())

            rel_type_vendor_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("is vendor of"))
            rel_vendor_obj = methods.create_relation(
                vendor_obj, obj, rel_type_vendor_obj)
            rel_vendor_obj.title = str(vendor_obj.get_title()) + \
                " is vendor of " + str(obj.get_title())

            methods.add_ci(obj)
            methods.add_ci(vendor_obj)
            methods.add_rel(rel_obj_vendor)
            methods.add_rel(rel_vendor_obj)

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

            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
