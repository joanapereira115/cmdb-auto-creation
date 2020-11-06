import regex
import json
import requests
from colored import fg, bg, attr
import winrm
import chardet

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods
from normalization import normalization

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# descoberta de informação acerca do sistema operativo


def os_discovery(client, ci):
    os_type = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType("Operating System"))
    obj = ConfigurationItem.ConfigurationItem()
    obj.set_type(os_type.get_id())
###########################################
    r = client.run_cmd('systeminfo /fo CSV', [])
    lines = r.std_out
    the_encoding = chardet.detect(lines)['encoding']
    lines = lines.decode(the_encoding)

    fields = lines.split("\n")[0].split(",")
    values = [l.strip('\"') for l in lines.split("\n")[1].split("\",")]
    info = {}

    for i in range(0, len(fields)-1):
        info[fields[i].strip("\"")] = values[i]

    obj.set_title(info.get("OS Name"))
    methods.define_attribute("version", info.get("OS Version"), obj)
    methods.define_attribute(
        "configuration", info.get("OS Configuration"), obj)
    methods.define_attribute("build type", info.get("OS Build Type"), obj)
    methods.define_attribute("product id", info.get("Product ID"), obj)
    methods.define_attribute(
        "install date", info.get("Original Install Date"), obj)
    methods.define_attribute("boot device", info.get("Boot Device"), obj)
    methods.define_attribute("BIOS version", info.get("BIOS Version"), obj)

    manufacturer = info.get("OS Manufacturer")

    manufacturer_type = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType("Manufacturer"))
    man_obj = ConfigurationItem.ConfigurationItem()
    man_obj.set_title(manufacturer)
    man_obj.set_type(manufacturer_type.get_id())

    rel_type_obj_man = methods.add_rel_type(
        RelationshipType.RelationshipType("has manufacturer"))
    rel_obj_man = methods.create_relation(
        obj, man_obj, rel_type_obj_man)
    rel_obj_man.title = str(obj.get_title()) + \
        " has manufacturer " + str(man_obj.get_title())

    rel_type_man_obj = methods.add_rel_type(
        RelationshipType.RelationshipType("manufacturer of"))
    rel_man_obj = methods.create_relation(
        man_obj, obj, rel_type_man_obj)
    rel_man_obj.title = str(man_obj.get_title()) + \
        " manufacturer of " + str(obj.get_title())

    methods.add_ci(obj)
    methods.add_ci(man_obj)
    methods.add_rel(rel_obj_man)
    methods.add_rel(rel_man_obj)

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

    methods.add_rel(rel_ci_obj)
    methods.add_rel(rel_obj_ci)
