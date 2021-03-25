# -*- coding: utf-8 -*-

import json
from colored import fg, attr
import datetime

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def sw_discovery(client, ci):
    """
    Gathers information about the installed applications, frameworks and extensions of the OS X machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.
    """
    _, stdout, stderr = client.exec_command(
        "system_profiler SPApplicationsDataType -json")

    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        apps = stdout.readlines()
        apps_info = json.loads("".join(apps)).get('SPApplicationsDataType')

        if apps_info != None:
            for app in apps_info:
                if "lastModified" in app:
                    lastMod = app.get("lastModified")
                    date = lastMod.split("T")[0]
                    new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    now = datetime.datetime.now()
                    diff = (now.year - new_date.year) * \
                        12 + now.month - new_date.month
                    # consider only the apps that were modified in the last month
                    if diff < 2:

                        app_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType("Application"))

                        obj = ConfigurationItem.ConfigurationItem()
                        obj.set_type(app_type.get_id())
                        obj.set_title(app.get("_name"))

                        methods.define_attribute(
                            "arch kind", app.get("arch_kind"), obj)
                        methods.define_attribute("info", app.get("info"), obj)
                        methods.define_attribute(
                            "last modified", app.get("lastModified"), obj)
                        methods.define_attribute("path", app.get("path"), obj)
                        methods.define_attribute(
                            "version", app.get("version"), obj)
                        methods.define_attribute(
                            "obtained from", app.get("obtained_from"), obj)

                        rel_type_ci_obj = methods.add_rel_type(
                            RelationshipType.RelationshipType("has installed"))
                        rel_ci_obj = methods.create_relation(
                            ci, obj, rel_type_ci_obj)
                        rel_ci_obj.title = str(ci.get_title()) + \
                            " has installed " + str(obj.get_title())

                        rel_type_obj_ci = methods.add_rel_type(
                            RelationshipType.RelationshipType("installed on"))
                        rel_obj_ci = methods.create_relation(
                            obj, ci, rel_type_obj_ci)
                        rel_obj_ci.title = str(obj.get_title()) + \
                            " installed on " + str(ci.get_title())

                        methods.add_ci(obj)
                        methods.add_rel(rel_ci_obj)
                        methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPFrameworksDataType -json")

    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        frames = stdout.readlines()
        frames_info = json.loads("".join(frames)).get('SPFrameworksDataType')
        for frame in frames_info:
            if "lastModified" in frame:
                lastMod = frame.get("lastModified")
                date = lastMod.split("T")[0]
                new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                now = datetime.datetime.now()
                diff = (now.year - new_date.year) * \
                    12 + now.month - new_date.month
                # consider only the frameworks that were modified in the last month
                if diff < 2:
                    frame_type = methods.add_ci_type(
                        ConfigurationItemType.ConfigurationItemType("Framework"))

                    obj = ConfigurationItem.ConfigurationItem()
                    obj.set_type(frame_type.get_id())
                    obj.set_title(frame.get("_name"))

                    methods.define_attribute(
                        "arch kind", frame.get("arch_kind"), obj)
                    methods.define_attribute("info", frame.get("info"), obj)
                    methods.define_attribute(
                        "last modified", frame.get("lastModified"), obj)
                    methods.define_attribute("path", frame.get("path"), obj)
                    methods.define_attribute(
                        "version", frame.get("version"), obj)
                    methods.define_attribute(
                        "obtained from", frame.get("obtained_from"), obj)
                    methods.define_attribute(
                        "private framework", frame.get("private_framework"), obj)

                    rel_type_ci_obj = methods.add_rel_type(
                        RelationshipType.RelationshipType("has installed"))
                    rel_ci_obj = methods.create_relation(
                        ci, obj, rel_type_ci_obj)
                    rel_ci_obj.title = str(ci.get_title()) + \
                        " has installed " + str(obj.get_title())

                    rel_type_obj_ci = methods.add_rel_type(
                        RelationshipType.RelationshipType("installed on"))
                    rel_obj_ci = methods.create_relation(
                        obj, ci, rel_type_obj_ci)
                    rel_obj_ci.title = str(obj.get_title()) + \
                        " installed on " + str(ci.get_title())

                    methods.add_ci(obj)
                    methods.add_rel(rel_ci_obj)
                    methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPExtensionsDataType -json")

    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        exts = stdout.readlines()
        ext_info = json.loads("".join(exts)).get('SPExtensionsDataType')

        for ext in ext_info:
            if "lastModified" in ext:
                lastMod = ext.get("lastModified")
                date = lastMod.split("T")[0]
                new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                now = datetime.datetime.now()
                diff = (now.year - new_date.year) * \
                    12 + now.month - new_date.month
                # consider only the extensions that were modified in the last month
                if diff < 2:
                    ext_type = methods.add_ci_type(
                        ConfigurationItemType.ConfigurationItemType("Extension"))

                    obj = ConfigurationItem.ConfigurationItem()
                    obj.set_type(ext_type.get_id())
                    obj.set_title(ext.get("_name"))

                    methods.define_attribute(
                        "bundle id", ext.get("spext_bundleid"), obj)
                    methods.define_attribute("has 64 Bit Intel Code", ext.get(
                        "spext_has64BitIntelCode"), obj)
                    methods.define_attribute("has All Dependencies", ext.get(
                        "spext_hasAllDependencies"), obj)
                    methods.define_attribute("last modified",
                                             ext.get("spext_lastModified"), obj)
                    methods.define_attribute(
                        "loadable", ext.get("spext_loadable"), obj)
                    methods.define_attribute(
                        "loaded", ext.get("spext_loaded"), obj)
                    methods.define_attribute(
                        "notarized", ext.get("spext_notarized"), obj)
                    methods.define_attribute(
                        "obtained from", ext.get("spext_obtained_from"), obj)
                    methods.define_attribute(
                        "path", ext.get("spext_path"), obj)
                    methods.define_attribute(
                        "version", ext.get("version"), obj)
                    methods.define_attribute(
                        "signed by", ext.get("spext_signed_by"), obj)
                    try:
                        methods.define_attribute(
                            "architecture", ext.get("spext_architectures")[0], obj)
                    except:
                        pass

                    rel_type_ci_obj = methods.add_rel_type(
                        RelationshipType.RelationshipType("has installed"))
                    rel_ci_obj = methods.create_relation(
                        ci, obj, rel_type_ci_obj)
                    rel_ci_obj.title = str(ci.get_title()) + \
                        " has installed " + str(obj.get_title())

                    rel_type_obj_ci = methods.add_rel_type(
                        RelationshipType.RelationshipType("installed on"))
                    rel_obj_ci = methods.create_relation(
                        obj, ci, rel_type_obj_ci)
                    rel_obj_ci.title = str(obj.get_title()) + \
                        " installed on " + str(ci.get_title())

                    methods.add_ci(obj)
                    methods.add_rel(rel_ci_obj)
                    methods.add_rel(rel_obj_ci)
