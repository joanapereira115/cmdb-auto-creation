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


def storage_discovery(client, ci):
    _, stdout, stderr = client.exec_command(
        "system_profiler SPMemoryDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        memory = stdout.readlines()
        memory_info = json.loads("".join(memory)).get(
            'SPMemoryDataType')[0].get('_items')

        mem_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("RAM"))

        for mem in memory_info:
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_title(mem.get("_name"))
            obj.set_type(mem_type.get_id())
            # TODO: relacionamento com manufacturer?
            methods.define_attribute(
                "manufacturer", mem.get("dimm_manufacturer"), obj)
            methods.define_attribute(
                "part number", mem.get("dimm_part_number"), obj)
            methods.define_attribute(
                "serial number", mem.get("dimm_serial_number"), obj)
            methods.define_attribute("size", mem.get("dimm_size"), obj)
            methods.define_attribute("speed", mem.get("dimm_speed"), obj)
            methods.define_attribute("status", mem.get("dimm_status"), obj)
            methods.define_attribute("architecture", mem.get("dimm_type"), obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("associated memory"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " associated memory " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("is component of"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
            rel_obj_ci.title = str(obj.get_title()) + \
                " is component of " + str(ci.get_title())

            methods.add_ci(obj)
            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPSerialATADataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        storage = stdout.readlines()
        storage_info = json.loads("".join(storage)).get('SPSerialATADataType')
        storage_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType(storage_info.get("spsata_product")))
        for s in storage_info.get("_items"):
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_title(s.get("_name"))
            obj.set_type(storage_type.get_id())
            methods.define_attribute(
                "bsd name", s.get("bsd_name"), obj)
            methods.define_attribute(
                "detachable drive", s.get("detachable_drive"), obj)
            methods.define_attribute(
                "device model", s.get("device_model"), obj)
            methods.define_attribute(
                "device revision", s.get("device_revision"), obj)
            methods.define_attribute(
                "serial number", s.get("device_serial"), obj)
            methods.define_attribute("partition map type",
                                     s.get("partition_map_type"), obj)
            methods.define_attribute(
                "removable media", s.get("removable_media"), obj)
            methods.define_attribute("size", s.get("size"), obj)
            methods.define_attribute("medium type",
                                     s.get("spsata_medium_type"), obj)
            methods.define_attribute("ncq", s.get("spsata_ncq"), obj)
            methods.define_attribute(
                "ncq depth", s.get("spsata_ncq_depth"), obj)
            methods.define_attribute(
                "link speed", storage_info.get("spsata_linkspeed"), obj)
            methods.define_attribute(
                "link width", storage_info.get("spsata_linkwidth"), obj)
            methods.define_attribute("physical interconnect", storage_info.get(
                "spsata_physical_interconnect"), obj)
            methods.define_attribute(
                "port description", storage_info.get("spsata_portdescription"), obj)
            methods.define_attribute(
                "product", storage_info.get("spsata_product"), obj)

            vendor = storage_info.get("spsata_vendor")
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
            methods.add_rel(rel_obj_vendor)
            methods.add_rel(rel_vendor_obj)

            volumes = s.get("volumes")
            volume_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Volume"))
            for v in volumes:
                vol = ConfigurationItem.ConfigurationItem()
                vol.set_title(v.get("_name"))
                vol.set_type(volume_type.get_id())
                methods.define_attribute("bsd name", v.get("bsd_name"), vol)
                methods.define_attribute(
                    "filesystem", v.get("file_system"), vol)
                methods.define_attribute("iocontent", v.get("iocontent"), vol)
                methods.define_attribute("size", v.get("size"), vol)
                methods.define_attribute("uuid", v.get("volume_uuid"), vol)

                rel_type_obj_vol = methods.add_rel_type(
                    RelationshipType.RelationshipType("has volume"))
                rel_obj_vol = methods.create_relation(
                    obj, vol, rel_type_obj_vol)
                rel_obj_vol.title = str(obj.get_title()) + \
                    " has volume " + str(vol.get_title())

                rel_type_vol_obj = methods.add_rel_type(
                    RelationshipType.RelationshipType("is volume of"))
                rel_vol_obj = methods.create_relation(
                    vol, obj, rel_type_vol_obj)
                rel_vol_obj.title = str(vol.get_title()) + \
                    " is volume of " + str(obj.get_title())

                methods.add_rel(rel_obj_vol)
                methods.add_rel(rel_vol_obj)

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
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPStorageDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        volumes = stdout.readlines()
        volume_info = storage_info = json.loads(
            "".join(volumes)).get('SPStorageDataType')
        volume_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Volume"))

        for vol in volume_info:
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(volume_type.get_id())
            obj.set_title(vol.get("_name"))
            methods.define_attribute("bsd name", vol.get("bsd_name"), obj)
            methods.define_attribute("filesystem", vol.get("file_system"), obj)
            methods.define_attribute(
                "free space", vol.get("free_space_in_bytes"), obj)
            methods.define_attribute(
                "ignore ownership", vol.get("ignore_ownership"), obj)
            methods.define_attribute(
                "mount point", vol.get("mount_point"), obj)
            methods.define_attribute(
                "size", vol.get("size_in_bytes"), obj)
            methods.define_attribute("uuid", vol.get("volume_uuid"), obj)
            methods.define_attribute("writable", vol.get("writable"), obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("has volume"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " has volume " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("is volume of"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
            rel_obj_ci.title = str(obj.get_title()) + \
                " is volume of " + str(ci.get_title())

            methods.add_ci(obj)
            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
