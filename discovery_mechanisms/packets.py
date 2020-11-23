# -*- coding: utf-8 -*-

import socket
import pyshark
import psutil
from colored import fg, attr
from getmac import get_mac_address as gma

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
        capture.sniff(packet_count=500)
    except:
        print(red + "\n>>> " + reset + "Error sniffing.")
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
    Explores LLDP packets.

    Parameters
    -------
    lldp_packs : list
        The list of LLDP packets.
    """
    my_mac = gma()
    for pack in lldp_packs:
        src = pack.eth.src
        if src != my_mac:
            print(green + "\n>>> " + reset +
                  "Found a machine via LLDP: " + str(src))
            # TODO: explore this machine


def explore_packets():
    """
    Sniffs packets on the active interfaces of the machine.
    """
    ifs = get_interfaces()
    for ifc in ifs:
        packets = get_packets(ifc)
        lldp_packs = get_lldp_packets(packets)
        explore_lldp_packets(lldp_packs)
