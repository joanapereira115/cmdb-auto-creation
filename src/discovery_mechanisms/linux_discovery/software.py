# -*- coding: utf-8 -*-

import json
from colored import fg, attr
import re

from similarity import similarity
from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def similar_apps(all_apps, used):
    apps = {}
    for app1 in used:
        apps[app1] = {}
        for app2 in all_apps:
            if re.match(app1, app2, re.IGNORECASE) != None:
                sim = similarity.calculate_similarity(app1, app2)
            else:
                sim = 0

            if sim > 0:
                apps[app1][app2] = sim

    sort = {}
    for a in apps:
        sort[a] = {k: v for k, v in sorted(
            apps.get(a).items(), key=lambda item: item[1], reverse=True)}

    apps = []
    for s in sort:
        if sort.get(s) != {}:
            apps.append(list(sort.get(s).keys())[0])

    return apps


def sw_discovery(client, ci):
    """
    Gathers information about the installed applications of the Linux machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the Linux machine that is going to be explored.
    """

    _, stdout, stderr = client.exec_command("dpkg-query -l")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:

        apps_info = stdout.readlines()[5:]
        info = {}
        for line in apps_info:
            app = line.split()[1:]
            info[app[0]] = [app[1], app[2], app[3]]

        _, stdout, stderr = client.exec_command(
            "top -n 1 -o VIRT -b | head -25 | tail -n +8 | awk '{ for(i=1;i<=NF;i++) {if ( i >= 12 ) printf $i\" \"}; printf \",\" }'")
        error = stderr.read().decode('utf-8')
        if error != "":
            print(red + ">>> " + reset + str(error) + "\n")
        else:
            last_used_np = stdout.readlines()[0].split(',')
            last_used = []
            for line in last_used_np:
                app = line.strip().strip('+')
                if app != "":
                    last_used.append(app)

            app_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Application"))

            apps = similar_apps({x for x in info}, last_used)

            for app in apps:
                obj = ConfigurationItem.ConfigurationItem()
                obj.set_type(app_type.get_id())
                obj.set_title(app)
                obj.set_description(info.get(app)[2])
                methods.define_attribute("Version", info.get(app)[0], obj)
                methods.define_attribute("Architecture", info.get(app)[1], obj)

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
