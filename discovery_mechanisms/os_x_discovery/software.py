import regex
import json
import requests
from colored import fg, bg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods
from normalization import normalization

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# descoberta de aplicações instaladas, frameworks e extensões


def sw_discovery(client, ci):
    _, stdout, stderr = client.exec_command(
        "system_profiler SPApplicationsDataType -json")

    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        apps = stdout.readlines()
        apps_info = json.loads("".join(apps)).get('SPSoftwareDataType')

        for app in apps_info:
            app_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Application"))

            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(app_type.get_id())
            obj.set_title(app.get("_name"))

            methods.define_attribute("arch kind", app.get("arch_kind"), obj)
            methods.define_attribute("info", app.get("info"), obj)
            methods.define_attribute(
                "last modified", app.get("lastModified"), obj)
            methods.define_attribute("path", app.get("path"), obj)
            methods.define_attribute("version", app.get("version"), obj)
            methods.define_attribute(
                "obtained from", app.get("obtained_from"), obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("has installed"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " has installed " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("installed on"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
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
            frame_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Framework"))

            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(frame_type.get_id())
            obj.set_title(frame.get("_name"))

            methods.define_attribute("arch kind", frame.get("arch_kind"), obj)
            methods.define_attribute("info", frame.get("info"), obj)
            methods.define_attribute(
                "last modified", frame.get("lastModified"), obj)
            methods.define_attribute("path", frame.get("path"), obj)
            methods.define_attribute("version", frame.get("version"), obj)
            methods.define_attribute(
                "obtained from", frame.get("obtained_from"), obj)
            methods.define_attribute(
                "private framework", frame.get("private_framework"), obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("has installed"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " has installed " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("installed on"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
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
            ext_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Extension"))

            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(ext_type.get_id())
            obj.set_title(ext.get("_name"))

            {

                "spext_architectures": [
                    "x86_64"
                ],
                "spext_bundleid": "com.apple.driver.ACPI_SMC_PlatformPlugin",
                "spext_has64BitIntelCode": "spext_yes",
                "spext_hasAllDependencies": "spext_satisfied",
                "spext_lastModified": "2019-11-15T05:21:29Z",
                "spext_loadable": "spext_yes",
                "spext_loaded": "spext_no",
                "spext_notarized": "spext_yes",
                "spext_obtained_from": "spext_apple",
                "spext_path": "/System/Library/Extensions/IOPlatformPluginFamily.kext/Contents/PlugIns/ACPI_SMC_PlatformPlugin.kext",
                "spext_runtime_environment": "spext_arch_x86",
                "spext_signed_by": "Software Signing, Apple Code Signing Certification Authority, Apple Root CA",
                "spext_version": "1.0.0",
                "version": "1.0.0"
            },

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
            methods.define_attribute("loaded", ext.get("spext_loaded"), obj)
            methods.define_attribute(
                "notarized", ext.get("spext_notarized"), obj)
            methods.define_attribute(
                "obtained from", ext.get("spext_obtained_from"), obj)
            methods.define_attribute("path", ext.get("spext_path"), obj)
            methods.define_attribute("version", ext.get("version"), obj)
            methods.define_attribute(
                "signed by", ext.get("spext_signed_by"), obj)
            try:
                methods.define_attribute(
                    "architecture", ext.get("spext_architectures")[0], obj)
            except:
                pass

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("has installed"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " has installed " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("installed on"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
            rel_obj_ci.title = str(obj.get_title()) + \
                " installed on " + str(ci.get_title())

            methods.add_ci(obj)
            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
