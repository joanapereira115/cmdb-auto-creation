# -*- coding: utf-8 -*-

import json
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def network_discovery(client, ci):
    """
    Gathers the network information about the OS X machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.
    """
    _, stdout, stderr = client.exec_command(
        "system_profiler SPFirewallDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        firewall = stdout.readlines()
        firewall_info = json.loads("".join(firewall)).get('SPFirewallDataType')
        firewall_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Firewall"))
        for frwl in firewall_info:
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(firewall_type.get_id())
            obj.set_title(frwl.get("_name"))

            methods.define_attribute(
                "mode", frwl.get("spfirewall_globalstate"), obj)
            methods.define_attribute("logging", frwl.get(
                "spfirewall_loggingenabled"), obj)
            methods.define_attribute("stealth mode", frwl.get(
                "spfirewall_stealthenabled"), obj)
            for app in frwl.get("spfirewall_applications"):
                methods.define_attribute(app, frwl.get(
                    "spfirewall_applications").get(app), obj)
            for serv in frwl.get("spfirewall_services"):
                methods.define_attribute(serv, frwl.get(
                    "spfirewall_services").get(serv), obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("associated firewall"))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " associated firewall " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType("firewall of"))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
            rel_obj_ci.title = str(obj.get_title()) + \
                " firewall of " + str(ci.get_title())

            methods.add_ci(obj)
            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPNetworkDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        services = stdout.readlines()
        services_info = json.loads(
            "".join(services)).get('SPNetworkDataType')
        for serv in services_info:
            net_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Network Service"))
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(net_type.get_id())

            name = serv.get("_name")
            hw = serv.get("hardware")
            itfc = serv.get("interface")

            obj.set_title(frwl.get("_name"))

            hw_port_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Hardware Port"))
            port_obj = ConfigurationItem.ConfigurationItem()
            port_obj.set_type(hw_port_type.get_id())
            port_obj.set_title(name)
            methods.define_attribute("interface", itfc, port_obj)
            methods.define_attribute("hardware", hw, port_obj)

            rel_type_obj_port = methods.add_rel_type(
                RelationshipType.RelationshipType("associated port"))
            rel_obj_port = methods.create_relation(
                obj, port_obj, rel_type_ci_obj)
            rel_obj_port.title = str(obj.get_title()) + \
                " associated port " + str(port_obj.get_title())

            rel_type_port_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("associated network service"))
            rel_port_obj = methods.create_relation(
                port_obj, obj, rel_type_obj_ci)
            rel_port_obj.title = str(port_obj.get_title()) + \
                " associated network service " + str(obj.get_title())

            methods.add_ci(obj)
            methods.add_ci(port_obj)
            methods.add_rel(rel_obj_port)
            methods.add_rel(rel_obj_ci)

            #dhcp_info = serv.get("dhcp")
            #dns_info = serv.get("DNS")
            ethernet_info = serv.get("Ethernet")
            if ethernet_info != None:
                mac = ethernet_info.get("MAC Address")
                obj.set_mac_address(mac)

                ipv4_info = serv.get("IPv4")
                for ipv4 in ipv4_info.get("Addresses"):
                    ci.add_ipv4_address(ipv4)
                    obj.add_ipv4_address(ipv4)

                ipv6_info = serv.get("IPv6")
                for ipv6 in ipv6_info.get("Addresses"):
                    ci.add_ipv6_address(ipv6)
                    obj.add_ipv6_address(ipv6)
                #proxies_info = serv.get("Proxies")

                rel_type_ci_obj = methods.add_rel_type(
                    RelationshipType.RelationshipType("has network service"))
                rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
                rel_ci_obj.title = str(ci.get_title()) + \
                    " has network service " + str(obj.get_title())

                rel_type_obj_ci = methods.add_rel_type(
                    RelationshipType.RelationshipType("running on"))
                rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
                rel_obj_ci.title = str(obj.get_title()) + \
                    " running on " + str(ci.get_title())

                methods.add_ci(obj)
                methods.add_rel(rel_ci_obj)
                methods.add_rel(rel_obj_ci)
###########################################

    # TODO: $ system_profiler SPNetworkLocationDataType
    # TODO: $ networksetup -listVLANs
