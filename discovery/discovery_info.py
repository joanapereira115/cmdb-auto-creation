# -*- coding: utf-8 -*-

import regex
import ipaddress

"""
    Saves information about the network addresses of the infrastructure.
"""
discovery_info = {
    # ["IP address", ...]
    "ip_addresses": [],

    # ["MAC address", ...]
    "mac_addresses": [],

    # {"IP address": "MAC address", ...}
    "ip_to_mac_address": {},

    # ["IP/MAC address", ...]
    "visited_addresses": [],

    # {"Network": ["IP address", ...], ...}
    "networks": {}
}


def add_ip(ip):
    """
    Saves an IP address.

    Parameters
    ------
    ip : string
        The IP address to save.
    """
    net = regex.search(
        r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}0', ip)
    broad = regex.search(
        r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}255', ip)
    if ip != None and ip != "" and ip != "127.0.0.1" and net == None and broad == None:
        if ip not in discovery_info.get("ip_addresses"):
            discovery_info["ip_addresses"].append(ip)


def add_mac(mac):
    """
    Saves an MAC address.

    Parameters
    ------
    mac : string
        The MAC address to save.
    """
    if mac != None and mac != "":
        if mac not in discovery_info.get("mac_addresses"):
            discovery_info["mac_addresses"].append(mac)


def add_ip_to_mac(ip, mac):
    """
    Saves an correspondent IP and MAC addresses.

    Parameters
    ------
    ip : string
        The IP address.

    mac : string
        The MAC address.
    """
    if ip != None and ip != "" and mac != None and mac != "":
        if ip not in discovery_info.get("ip_to_mac_address"):
            discovery_info["ip_to_mac_address"][ip] = mac


def get_mac_from_ip(ip):
    """
    Returns the MAC address of the IP address translation.

    Parameters
    ------
    ip : string
        The IP address.

    Returns 
    ------
    string, None
        Returns the MAC address, or None if there is no match with the IP address.
    """
    if ip in discovery_info.get("ip_to_mac_address"):
        return discovery_info.get("ip_to_mac_address").get(ip)
    else:
        return None


def add_to_network(ip, mask):
    """
    Adds an IP address to it's network.

    Parameters
    ------
    ip : string
        The IP address.

    mask : string
        The network mask of the IP address.

    """
    net = regex.search(
        r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}0', ip)
    broad = regex.search(
        r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}255', ip)

    if ip != None and ip != "" and ip != "127.0.0.1" and net == None and broad == None:
        t = str(ip) + "/" + str(mask)
        net = str(ipaddress.ip_network(t, strict=False))

        if net not in discovery_info.get("networks"):
            discovery_info["networks"][net] = []
        if ip not in discovery_info.get("networks").get(net):
            discovery_info["networks"][net].append(ip)
