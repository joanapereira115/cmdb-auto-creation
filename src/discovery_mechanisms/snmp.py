# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from easysnmp import snmp_get, snmp_set, snmp_walk
from pysnmp.entity.rfc3413.oneliner import cmdgen

from password_vault import vault
from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods
from discovery import discovery_info

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def get_info(ip, oid, community):
    """    
    Accesses the value of the oid via SNMP.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    oid : string
        The oid of the variable we want to know.

    community : string
        The SNMP community string.

    Returns
    -------
    string, None
        Returns the value of the variable, or None if the value cannot be retrieved.
    """
    cmdGen = cmdgen.CommandGenerator()
    errIndication, _, _, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((ip, 161), retries=2),
        oid, lookupNames=False, lookupValues=False
    )

    if errIndication:
        print(red + "\n>>> " + reset + "Unable to retrieve SNMP information.")
    else:
        r = varBinds[0][1].prettyPrint()
        if ((r == "No Such Object currently exists at this OID") | (r == "No Such Instance currently exists at this OID")):
            return None
        return r

    return None


def get_bulk(ip, oid, community):
    """    
    Accesses the multiple values of the oid via SNMP.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    oid : string
        The oid of the variable we want to know.

    community : string
        The SNMP community string.

    Returns
    -------
    list, None
        Returns the values of the variable, or None if the value cannot be retrieved.
    """
    cmdGen = cmdgen.CommandGenerator()
    errIndication, _, _, varBindTable = cmdGen.bulkCmd(cmdgen.CommunityData(community),
                                                       cmdgen.UdpTransportTarget(
        (ip, 161), timeout=30, retries=2),
        0, 50,
        oid,
        lookupNames=False, lookupValues=False
    )

    if errIndication:
        print(red + "\n>>> " + reset + "Unable to retrieve SNMP information.")
    else:
        ret = []
        for r in varBindTable:
            for n, _ in r:
                n = str(n)
                if (n.startswith(oid) == 0):
                    return ret
                ret.append(r)
        return ret

    return None


def addresses(ip, community, ci):
    """
    Accesses the table of addressing information relevant to this entity's IPv4 addresses of the machine via SNMP 
    and obtains all the addresses of it's interfaces.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    ci : ConfigurationItem
        The ConfigurationItem object that represents the machine.
    """
    # The table of addressing information relevant to this entity's IPv4 addresses.
    ipAdEntAddr = "1.3.6.1.2.1.4.20.1.1"
    ipAdEntNetMask = "1.3.6.1.2.1.4.20.1.3"

    ret = get_bulk(ip, ipAdEntAddr, community)
    if ret != None:
        for r in ret:
            for _, val in r:
                ip = val.prettyPrint()
                ci.add_ipv4_address(ip)
                # discovery_info.add_ip(ip)

    ret = get_bulk(ip, ipAdEntNetMask, community)
    if ret != None:
        for r in ret:
            for name, val in r:
                ip = name.prettyPrint()[len("SNMPv2-SMI::mib-2.4.20.1.3."):]
                mask = val.prettyPrint()
                discovery_info.add_to_network(ip, mask)


def has_printer_mib(ip, community):
    """
    Checks if the machine has a PrinterMIB via SNMP.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    Returns
    -------
    boolean
        Returns true if the machine has a PrinterMIB, and false otherwise.
    """
    res = get_info(ip, "1.3.6.1.2.1.43", community)
    if res == None:
        return False
    else:
        return True


def has_bridge_mib(ip, community):
    """
    Checks if the machine has a BridgeMIB via SNMP.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    Returns
    -------
    boolean
        Returns true if the machine has a BridgeMIB, and false otherwise.
    """
    res = get_info(ip, "1.3.6.1.2.1.17", community)
    if res == None:
        return False
    else:
        return True


def device_type(ip, community, ci):
    """
    Accesses the sysServices via SNMP and obtains the type of the machine.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    ci : ConfigurationItem
        The ConfigurationItem object that represents the machine.
    """
    sysServices = int(get_info(ip, "1.3.6.1.2.1.1.7.0", community))
    binary = '{0:07b}'.format(sysServices)
    l7 = binary[0]
    l4 = binary[3]
    l3 = binary[4]
    l2 = binary[5]

    if l2 == "1":
        if l3 == "1":
            if has_bridge_mib(ip, community) == True:
                ci_type = "L3 Switch"
            else:
                if l7 == "1":
                    ci_type = "L7 Application Switch"
                else:
                    ci_type = "Router"
        else:
            if has_bridge_mib(ip, community) == True:
                ci_type = "L2 Switch"
            else:
                ci_type = "Host"
    else:
        if l3 == "1":
            if l4 == "1":
                ci_type = "L4 Switch"
            else:
                if l7 == "1":
                    ci_type = "L7 Application Switch"
                else:
                    ci_type = "Router"
        else:
            if has_printer_mib(ip, community) == True:
                ci_type = "Printer"
            else:
                ci_type = "Host"

    tp = methods.add_ci_type(
        ConfigurationItemType.ConfigurationItemType(ci_type))
    ci.set_type(tp.get_id())


def arp_table(ip, community, ci):
    """
    Accesses the IPv4 address translation table of the device.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    ci : ConfigurationItem
        The ConfigurationItem object that represents the machine.
    """
    ipNetToMediaPhysAddress = "1.3.6.1.2.1.3.1.1.2"

    ret = get_bulk(ip, ipNetToMediaPhysAddress, community)
    if ret != None:
        for r in ret:
            for name in r:
                val = name.prettyPrint()[len(
                    "SNMPv2-SMI::mib-2.3.1.1.2.2.1."):]
                ip = val.split("=")[0].strip()
                mac = val.split("=")[1].strip()[len("0x"):]
                new_mac = ""
                for i in range(0, len(mac)):
                    if i % 2 == 0 and i != 0:
                        new_mac += ":" + mac[i]
                    else:
                        new_mac += mac[i]
                mac = new_mac.upper()

                discovery_info.add_ip(ip)
                discovery_info.add_mac(mac)
                discovery_info.add_ip_to_mac(ip, mac)


def routing_table(ip, community, ci):
    """
    Accesses the routing table of the machine via SNMP and obtains all it's routes.
    Checks the direct and indirect routes.
    If a route is direct, it means that the route is directly connected into the (sub-)network.
    If a route is indirect, it's a route to a non-local host/network/sub-network.

    Parameters
    -------
    ip : string
        The IP address of the machine.

    community : string
        The SNMP community string.

    ci : ConfigurationItem
        The ConfigurationItem object that represents the machine.
    """
    ipRouteType = "1.3.6.1.2.1.4.21.1.8"
    ret = get_bulk(ip, ipRouteType, community)
    if ret != None:
        for r in ret:
            for name, val in r:
                ip = name.prettyPrint()[len("SNMPv2-SMI::mib-2.4.21.1.8."):]
                route_type = int(val.prettyPrint())

                # indirect(4)
                if route_type == 4:
                    discovery_info.add_ip(ip)

                    new_ci = ConfigurationItem.ConfigurationItem()
                    new_ci.add_ipv4_address(ip)
                    mac = discovery_info.get_mac_from_ip(ip)
                    if mac != None:
                        ci.set_mac_address(mac)

                    rel_type = methods.add_rel_type(
                        RelationshipType.RelationshipType("route to"))
                    rel_obj_1 = methods.create_relation(ci, new_ci, rel_type)
                    rel_obj_1.set_title(str(ci.get_title()) +
                                        " route to " + str(new_ci.get_title()))

                    rel_obj_2 = methods.create_relation(new_ci, ci, rel_type)
                    rel_obj_2.set_title(str(new_ci.get_title()) + " route to " +
                                        str(ci.get_title()))

                    methods.add_ci(new_ci)
                    methods.add_rel(rel_obj_1)
                    methods.add_rel(rel_obj_2)

                # direct(3)
                elif route_type == 3:
                    ci.add_ipv4_address(ip)
                    # discovery_info.add_ip(ip)


def run_snmp(ip, secrets):
    """
    Obtains information about the machines using the SNMP protocol.
    Gathers data about addresses, device types and other connected devices.
    """
    for secret in secrets:
        c = get_info(ip, "1.3.6.1.2.1.1.1.0", secret)
        if c != None:
            ci = ConfigurationItem.ConfigurationItem()
            mac = discovery_info.get_mac_from_ip(ip)
            if mac != None:
                ci.set_mac_address(mac)

            print(blue + "\n>>> " + reset +
                  "SNMP discovery in the address " + str(ip) + "...")
            addresses(ip, secret, ci)
            device_type(ip, secret, ci)
            arp_table(ip, secret, ci)
            #routing_table(ip, secret, ci)

            methods.add_ci(ci)
