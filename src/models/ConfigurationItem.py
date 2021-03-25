# -*- coding: utf-8 -*-

import itertools
from normalization import normalization


class ConfigurationItem:
    """Represents an organization's infrastructure component.

    Attributes:
        id_iter         int               The iterator used to generate the item identifier.
        uuid            string            The universally unique identifier (128-bit number) assigned to the item.
        serial_number   string            The manufacturer-allocated number used to identify the item.
        title            string            The label by which the item is known.
        description     string            The textual description of the item.
        status          string            The current status value for the operational condition of the item.
        mac_address     string            The media access control address assigned to the item.
        os_family       string            The operating system family of the item.
        ipv4_addresses  list<string>      The list of Internet Protocol version 4 addresses assigned to the item.
        ipv6_addresses  list<string>      The list of Internet Protocol version 6 addresses assigned to the item.
        type_id         int               The identifier of the item type.
        attributes      list<int>         The list of identifiers of the item attributes.
    """

    id_iter = itertools.count()
    uuid = ""
    serial_number = ""
    title = ""
    description = ""
    status = ""
    mac_address = ""
    os_family = ""
    ipv4_addresses = []
    ipv6_addresses = []
    type_id = 0
    attributes = []

    def __init__(self):
        """Initialize the configuration item with a generated identifier."""
        self.id = next(self.id_iter) + 1
        self.uuid = ""
        self.serial_number = ""
        self.title = ""
        self.description = ""
        self.status = ""
        self.mac_address = ""
        self.ipv4_addresses = []
        self.ipv6_addresses = []
        self.type_id = 0
        self.attributes = []

    def get_id(self):
        """Get the configuration item identifier."""
        return self.id

    def get_uuid(self):
        """Get the configuration item type universally unique identifier."""
        return self.uuid

    def set_uuid(self, uuid):
        """Set the configuration item universally unique identifier to the value passed."""
        if uuid != None:
            self.uuid = uuid

    def get_serial_number(self):
        """Get the configuration item serial number."""
        return self.serial_number

    def set_serial_number(self, serial_number):
        """Set the configuration item serial number to the value passed."""
        if serial_number != None:
            self.serial_number = serial_number

    def get_title(self):
        """Get the configuration item title."""
        return self.title

    def set_title(self, title):
        """Set the configuration item title to the value passed."""
        if title != None:
            self.title = title

    def get_description(self):
        """Get the configuration item description."""
        return self.description

    def set_description(self, description):
        """Set the configuration item description to the value passed."""
        if description != None:
            old = self.description
            if old != "":
                self.description = old + " " + description
            else:
                self.description = description

    def get_status(self):
        """Get the configuration item status."""
        return self.status

    def set_status(self, status):
        """Set the configuration item status to the value passed."""
        if status != None:
            self.status = status

    def get_mac_address(self):
        """Get the configuration item mac address."""
        return self.mac_address

    def set_mac_address(self, mac_address):
        """Set the configuration item mac address to the value passed."""
        if mac_address != None:
            self.mac_address = mac_address

    def get_os_family(self):
        """Get the configuration item operating system family."""
        return self.os_family

    def set_os_family(self, os_family):
        """Set the configuration item operating system family to the value passed."""
        if os_family != None:
            self.os_family = os_family

    def get_ipv4_addresses(self):
        """Get the list of IPv4 addresses associated with the configuration item."""
        return self.ipv4_addresses

    def add_ipv4_address(self, ipv4):
        """Adds a new IPv4 address to the list of IPv4 addresses of the configuration item."""
        if ipv4 not in self.ipv4_addresses and ipv4 != None and ipv4 != "127.0.0.1" and ipv4 != "":
            self.ipv4_addresses.append(ipv4)

    def get_ipv6_addresses(self):
        """Get the list of IPv6 addresses associated with the configuration item."""
        return self.ipv6_addresses

    def add_ipv6_address(self, ipv6):
        """Adds a new IPv6 address to the list of IPv6 addresses of the configuration item."""
        if ipv6 not in self.ipv6_addresses and ipv6 != None:
            self.ipv6_addresses.append(ipv6)

    def get_type(self):
        """Get the configuration item type identifier."""
        return self.type_id

    def set_type(self, type_id):
        """Set the configuration item type identifier to the value passed."""
        if type_id != None:
            self.type_id = int(type_id)

    def get_attributes(self):
        """Get the list of attributes identifiers of the configuration item."""
        return self.attributes

    def add_attribute(self, attribute_id):
        """Adds a new attribute identifier to the list of configuration item attributes."""
        if attribute_id not in self.attributes and attribute_id != None:
            self.attributes.append(attribute_id)
