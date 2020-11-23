# -*- coding: utf-8 -*-

"""
    Saves information about the .
"""
discovery_info = {
    # ["IP address", ...]
    "ip_addresses": [],

    # ["MAC address", ...]
    "mac_addresses": [],

    # {"IP address": "MAC address", ...}
    "ip_to_mac_address": {},

    # ["IP/MAC address", ...]
    "visited_addresses": []
}


def add_ip(ip):
    if ip != None and ip != "":
        if ip not in discovery_info.get("ip_addresses"):
            discovery_info["ip_addresses"].append(ip)


def add_mac(mac):
    if mac != None and mac != "":
        if mac not in discovery_info.get("mac_addresses"):
            discovery_info["mac_addresses"].append(mac)


def add_ip_to_mac(ip, mac):
    if ip != None and ip != "" and mac != None and mac != "":
        if ip not in discovery_info.get("ip_to_mac_address"):
            discovery_info["ip_to_mac_address"][ip] = mac
