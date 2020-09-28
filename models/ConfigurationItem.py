# -*- coding: utf-8 -*-

import json
import itertools


class ConfigurationItem:
    """Represents an organization's infrastructure component.

    Attributes:
        id_iter         int               The iterator used to generate the item identifier.
        uuid            string            The universally unique identifier (128-bit number) assigned to the item.
        serial_number   string            The manufacturer-allocated number used to identify the item.
        name            string            The label by which the item is known.
        description     string            The textual description of the item.
        status          string            The current status value for the operational condition of the item.
        mac_address     string            The media access control address assigned to the item.
        ipv4_addresses  list<string>      The list of Internet Protocol version 4 addresses assigned to the item.
        ipv6_addresses  list<string>      The list of Internet Protocol version 6 addresses assigned to the item.
        type_id         int               The identifier of the item type.
        attributes      list<int>         The list of identifiers of the item attributes.
    """

    id_iter = itertools.count()
    uuid = ""
    serial_number = ""
    name = ""
    description = ""
    status = ""
    mac_address = ""
    ipv4_addresses = []
    ipv6_addresses = []
    type_id = 0
    attributes = []

    def __init__(self):
        """Initialize the configuration item with a generated identifier."""
        self.id = next(self.id_iter) + 1

    def get_id(self):
        """Get the configuration item identifier."""
        return self.id

    def get_uuid(self):
        """Get the configuration item type universally unique identifier."""
        return self.uuid

    def set_uuid(self, uuid):
        """Set the configuration item universally unique identifier to the value passed."""
        self.uuid = uuid

    def get_serial_number(self):
        """Get the configuration item serial number."""
        return self.serial_number

    def set_serial_number(self, serial_number):
        """Set the configuration item serial number to the value passed."""
        self.serial_number = serial_number

    def get_name(self):
        """Get the configuration item name."""
        return self.name

    def set_name(self, name):
        """Set the configuration item name to the value passed."""
        self.name = name

    def get_description(self):
        """Get the configuration item description."""
        return self.description

    def set_description(self, description):
        """Set the configuration item description to the value passed."""
        self.description = description

    def get_status(self):
        """Get the configuration item status."""
        return self.status

    def set_status(self, status):
        """Set the configuration item status to the value passed."""
        self.status = status

    def get_mac_address(self):
        """Get the configuration item mac address."""
        return self.mac_address

    def set_mac_address(self, mac_address):
        """Set the configuration item mac address to the value passed."""
        self.mac_address = mac_address

    def get_ipv4_addresses(self):
        """Get the list of IPv4 addresses associated with the configuration item."""
        return self.ipv4_addresses

    def add_ipv4_address(self, ipv4):
        """Adds a new IPv4 address to the list of IPv4 addresses of the configuration item."""
        if ipv4 not in self.ipv4_addresses:
            self.ipv4_addresses.append(ipv4)

    def get_ipv6_addresses(self):
        """Get the list of IPv6 addresses associated with the configuration item."""
        return self.ipv6_addresses

    def add_ipv6_address(self, ipv6):
        """Adds a new IPv6 address to the list of IPv6 addresses of the configuration item."""
        if ipv6 not in self.ipv6_addresses:
            self.ipv6_addresses.append(ipv6)

    def get_type(self):
        """Get the configuration item type identifier."""
        return self.type_id

    def set_type(self, type_id):
        """Set the configuration item type identifier to the value passed."""
        self.type_id = type_id

    def get_attributes(self):
        """Get the list of attributes identifiers of the configuration item."""
        return self.attributes

    def add_attribute(self, attribute_id):
        """Adds a new attribute identifier to the list of configuration item attributes."""
        if attribute_id not in self.attributes:
            self.attributes.append(attribute_id)

    # TODO: não é necessário
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
