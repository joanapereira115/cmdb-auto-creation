#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from objects import objects
import itertools

########################################################## CLASSES ##########################################################


class Element:
    id_iter = itertools.count()
    ci_type = ""
    name = ""
    value = ""
    status = ""
    description = ""
    generation = ""
    install_date = ""
    availability = ""
    serial_number = ""
    version = ""
    model = ""
    manufacturer = ""
    number = ""
    hostname = ""
    management_address = ""
    connectivity_status = ""
    net_mask = ""
    net_number = ""
    type_ = ""
    size = ""
    layout = ""
    bandwidth = ""
    height = ""
    width = ""
    speed = ""
    resolution = ""
    business_category = ""
    email = ""
    fax = ""
    mobile_phone = ""
    department = ""
    title = ""
    webpage = ""
    core_number = ""
    architecture = ""
    family = ""
    power = ""
    ip_range = ""
    capacity = ""
    removable = ""
    block_size = ""
    number_of_blocks = ""
    compression_method = ""
    transfer_rate = ""
    address = ""
    city = ""
    price = ""
    available_space = ""
    max_number_of_processes = ""
    author = ""
    filename = ""
    date = ""
    path = ""
    provider = ""

    def __init__(self):
        self.id = next(self.id_iter)

    def get_id(self):
        return self.id

    def element_print(self):
        print("--------------")
        print(self.ci_type)
        print("\tId: " + str(self.id))
        print("\tName: " + self.name)
        print("--------------")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


ci_types = [
    "Access_Point", "Protocol_Endpoint", "Communication_Endpoint", "IP_Endpoint", "LAN_Endpoint", "Organization", "Person", "LAN", "WAN", "DBMS",
    "DB_Schema", "DB_Instance", "Hardware_Component", "Keyboard", "Mouse", "Monitor", "Network_Port", "Motherboard", "CPU", "GPU", "UPS", "Chassis",
    "Card", "Rack", "Server", "Rack_Server", "Blade_Server", "Tower_Server", "Cluster", "Memory", "DRAM", "SRAM", "ROM", "HDD", "SSD", "RAID",
    "Disk_Partition", "CD_ROM", "Floppy_Drive", "Tape_Drive", "DVD_ROM", "BD_ROM", "Disk_Drive", "Building", "Service", "Business_Service", "Account",
    "Filesystem", "Software", "Patch", "Product", "Package", "BIOS_Element", "Operating_System", "Application", "Virtual_Server", "Virtual_Host",
    "Document", "Contract", "Licence", "File", "Cloud_Instance", "Workstation", "IPv4", "IPv6", "MAC_address", "Network", "Subnet", "Host",
    "NIC", "Hub", "Bridge", "Switch", "Router", "Firewall", "Load_Balancer", "SAN", "Mainframe", "Desktop", "Laptop", "Battery", "Printer",
    "Scanner", "Tablet", "Phone", "Container"
]

########################################################## RELATIONSHIPS ##########################################################

# TODO: atributos nos relacionamentos


class Relation:
    rel_type = ""
    source_id = 0
    source_type = ""
    target_id = 0
    target_type = ""

    def relation_print(self):
        print(self.rel_type + "\n")
        print("\tSource: " + self.source_type)
        print("\tTarget: " + self.target_type)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


relation_types = [
    "has_component", "is_component", "located_on", "has_location", "hosts", "installed_on", "has_address", "address_of", "assigned_to",
    "assigned_of", "connected_to", "mounted_in", "has_mount", "of_type", "has_instance"
]


def exist_element(ci_type, name):
    for o in objects:
        if type(o) is Element:
            if o.ci_type == ci_type and o.name == name:
                return o
    return None


def exist_relation(rel_type, source_id, target_id):
    for o in objects:
        if type(o) is Relation:
            if o.rel_type == rel_type and o.source_id == source_id and o.target_id == target_id:
                return True
    return False


def get_name_from_id(id):
    for o in objects:
        if type(o) is Element:
            if o.id == id:
                return o.name
    return ""
