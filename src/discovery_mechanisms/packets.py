# -*- coding: utf-8 -*-

import socket
import pyshark
import psutil
from colored import fg, attr
from getmac import get_mac_address as gma
import regex

from discovery import discovery_info

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
orange = fg('#e76f51')
reset = attr('reset')


def get_interfaces():
    """
    Obtains the active interfaces in the machine.

    Returns
    -------
    list
        Returns the list of active interfaces.
    """
    ifs = []
    addrs = psutil.net_if_addrs()
    for ifc in addrs.keys():
        interface_addrs = psutil.net_if_addrs().get(ifc) or []
        active = socket.AF_INET in [
            snicaddr.family for snicaddr in interface_addrs]
        if active == True:
            ifs.append(ifc)
    return ifs


def get_packets(ifc):
    """
    Sniffs packets in the given interface.

    Parameters
    -------
    ifc : string
        The interface of the machine.

    Returns
    -------
    list
        Returns the list of packets.
    """
    print(blue + "\n>>> " + reset +
          "Exploring packets in the interface " + str(ifc) + ".")
    capture = pyshark.LiveCapture(interface=ifc)
    try:
        capture.sniff(packet_count=5, timeout=20)
    except:
        print(red + ">>> " + reset + "Error sniffing.")
    return capture


def get_lldp_packets(packets):
    """
    Checks for LLDP packets.

    Parameters
    -------
    packets : list
        The list of packets.

    Returns
    -------
    list
        Returns the list of LLDP packets.
    """
    lldp_packs = []
    if packets != None and len(packets) > 0:
        for pack in packets:
            if 'LLDP' in pack:
                lldp_packs.append(pack)
    return lldp_packs


def explore_lldp_packets(lldp_packs):
    """
    Explores LLDP packets to find more devices.

    Parameters
    -------
    lldp_packs : list
        The list of LLDP packets.
    """
    my_mac = gma()
    for pack in lldp_packs:
        src = pack.eth.src
        if src != my_mac:
            #print()
            #print("Founded via LLDP: " + str(src))
            ipv6 = regex.search(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', src)
            ipv4 = regex.search(
                r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])', src)
            mac = regex.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', src)

            if ipv6 != None:
                discovery_info.add_ip(src)
            elif ipv4 != None:
                discovery_info.add_ip(src)
            elif mac != None:
                discovery_info.add_mac(src)


def explore_packets():
    """
    Sniffs packets on the active interfaces of the machine.
    """
    ifs = get_interfaces()
    for ifc in ifs:
        packets = get_packets(ifc)
        lldp_packs = get_lldp_packets(packets)
        explore_lldp_packets(lldp_packs)
