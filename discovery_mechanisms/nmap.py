#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex
import nmap
import sys
import os
from pprint import pprint
from colored import fg, bg, attr
from elevate import elevate
import getpass
import subprocess
import xml.etree.ElementTree as ET
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import json


from password_vault import vault
from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from normalization import normalization
import nmap

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

style = style_from_dict({
    Token.QuestionMark: '#B54653 bold',
    Token.Selected: '#86DEB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


class NotEmpty(Validator):
    def validate(self, document):
        ok = document.text != "" and document.text != None
        if not ok:
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text))  # Move cursor to end


def unlock_vault():
    vault.initialize()
    password_vault = [
        {
            'type': 'password',
            'message': 'Enter your vault password:',
            'name': 'password',
            'validate': NotEmpty
        }
    ]
    password_answer = prompt(password_vault, style=style)
    passwd = password_answer["password"]
    v = vault.unlock(passwd)
    if v == False:
        unlock_vault()


def create_relation(source, target, relation_type):
    if source != None and target != None and relation_type != None:
        rel = Relationship.Relationship()
        rel.type_id = relation_type.get_id()
        if source.get_id() == target.get_id():
            print("same source and target!")
            print()
        rel.source_id = source.get_id()
        rel.target_id = target.get_id()
        return rel
    else:
        return None


def create_attribute(obj, name, value):
    if value != None and value != "":
        attr = Attribute.Attribute(name, value)
        obj.add_attribute(attr.get_id())
        return attr
    else:
        return None


def run_nmap(addresses):
    print(blue + "\n>>> " + reset +
          "NMAP discovery in the range address " + str(addresses) + "...\n")

    nm = nmap.PortScanner()
    nm.scan(hosts=addresses, arguments='-PR -sV -A -R')

    for h in nm.all_hosts():
        print(green + "\t>>> " + reset +
              "Found active machine in the address " + str(h) + "...")
        host = ConfigurationItem.ConfigurationItem()
        addresses = nm[h].get("addresses")
        for addr in addresses:
            if addr == "ipv4":
                host.add_ipv4_address(addresses.get(addr))
            if addr == "ipv6":
                host.add_ipv6_address(addresses.get(addr))
            elif addr == "mac":
                host.set_mac_address(addresses.get(addr))

        hostnames = nm[h].get("hostnames")
        for hostname in hostnames:
            name = hostname.get("name")
            if name != None and name != "":
                hostname_attr = create_attribute(host, "hostname", name)
                methods.add_attribute(hostname_attr)

        v = list(nm[h].get("vendor").values())
        if len(v) > 0:
            vendor = list(nm[h].get("vendor").values())[0]
            vendor_ci = ConfigurationItem.ConfigurationItem()
            vendor_type = methods.ci_type_already_exists("Vendor")
            if vendor_type == None:
                vendor_type = ConfigurationItemType.ConfigurationItemType(
                    "Vendor")
                methods.add_ci_type(vendor_type)
            vendor_ci.set_type(vendor_type.get_id())
            vendor_ci.set_title = vendor
            vendor_rel_type = methods.rel_type_already_exists("has vendor")
            if vendor_rel_type == None:
                vendor_rel_type = RelationshipType.RelationshipType(
                    "has vendor")
                methods.add_rel_type(vendor_rel_type)
            vendor_rel = create_relation(host, vendor_ci, vendor_rel_type)
            vendor_rel.title = "has vendor"
            methods.add_ci(vendor_ci)
            methods.add_rel(vendor_rel)

        status = nm[h].get("status").get("state")
        host.set_status(status)

        for proto in nm[h].all_protocols():
            ports = nm[h][proto].keys()
            for port in ports:
                port_type = methods.ci_type_already_exists("Port")
                if port_type == None:
                    port_type = ConfigurationItemType.ConfigurationItemType(
                        "Port")
                    methods.add_ci_type(port_type)
                p = ConfigurationItem.ConfigurationItem()
                p.set_type(port_type.get_id())
                p.set_title(port)

                protocol_attr = create_attribute(p, "protocol", proto)
                methods.add_attribute(protocol_attr)

                """
                proto_type = methods.ci_type_already_exists("Protocol")
                if proto_type == None:
                    proto_type = ConfigurationItemType.ConfigurationItemType(
                        "Protocol")
                    methods.add_ci_type(proto_type)
                protocol = ConfigurationItem.ConfigurationItem()
                protocol.set_type(proto_type.get_id())
                protocol.set_title(proto)

                proto_rel_type = methods.rel_type_already_exists(
                    "has protocol")
                if proto_rel_type == None:
                    proto_rel_type = RelationshipType.RelationshipType(
                        "has protocol")
                    methods.add_rel_type(proto_rel_type)
                proto_rel = create_relation(p, protocol, proto_rel_type)
                proto_rel.title = "has protocol"
                methods.add_ci(protocol)
                methods.add_rel(proto_rel)
                """

                if nm[h][proto][port]['state'] != '':
                    p.set_status(nm[h][proto][port]['state'])
                if nm[h][proto][port]['cpe'] != '':
                    cpe_attr = create_attribute(
                        p, "cpe", nm[h][proto][port]['cpe'])
                    methods.add_attribute(cpe_attr)

                product_type = methods.ci_type_already_exists("Product")
                if product_type == None:
                    product_type = ConfigurationItemType.ConfigurationItemType(
                        "Product")
                    methods.add_ci_type(product_type)
                product = ConfigurationItem.ConfigurationItem()
                product.set_type(product_type.get_id())
                if nm[h][proto][port]['name'] != '':
                    product.set_title(nm[h][proto][port]['name'])
                if nm[h][proto][port]['product'] != '':
                    product.set_description(nm[h][proto][port]['product'])
                if nm[h][proto][port]['version'] != '':
                    version_attr = create_attribute(
                        product, "version", nm[h][proto][port]['version'])
                    methods.add_attribute(version_attr)

                product_rel_type = methods.rel_type_already_exists(
                    "has product")
                if product_rel_type == None:
                    product_rel_type = RelationshipType.RelationshipType(
                        "has product")
                    methods.add_rel_type(product_rel_type)
                product_rel = create_relation(p, product, product_rel_type)
                product_rel.title = "has product"
                methods.add_ci(product)
                methods.add_rel(product_rel)
                methods.add_ci(p)

        if 'osmatch' in nm[h]:
            if len(list(nm[h]['osmatch'])) > 0:
                osmatch = list(nm[h]['osmatch'])[0]
                if osmatch.get('accuracy') == 100:
                    os_type = methods.ci_type_already_exists(
                        "Operating System")
                    if os_type == None:
                        os_type = ConfigurationItemType.ConfigurationItemType(
                            "Operating System")
                        methods.add_ci_type(os_type)
                    os = ConfigurationItem.ConfigurationItem()
                    os.set_type(os_type.get_id())
                    os.set_title(osmatch.get('name'))

                    if 'osclass' in osmatch:
                        osclass = list(osmatch.get('osclass'))[0]

                        host_type = None
                        if osclass.get('type') == "general purpose":
                            host_type = methods.ci_type_already_exists("Host")
                            if host_type == None:
                                host_type = ConfigurationItemType.ConfigurationItemType(
                                    "Host")
                                methods.add_ci_type(host_type)
                        else:
                            host_type = methods.ci_type_already_exists(
                                osclass.get('type'))
                            if os_type == None:
                                host_type = ConfigurationItemType.ConfigurationItemType(
                                    osclass.get('type'))
                                methods.add_ci_type(host_type)
                        host.set_type(host_type.get_id())

                        vendor = osclass.get('vendor')
                        vendor_ci = ConfigurationItem.ConfigurationItem()
                        vendor_type = methods.ci_type_already_exists("Vendor")
                        if vendor_type == None:
                            vendor_type = ConfigurationItemType.ConfigurationItemType(
                                "Vendor")
                            methods.add_ci_type(vendor_type)
                        vendor_ci.set_type(vendor_type.get_id())
                        vendor_ci.set_title = vendor
                        vendor_rel_type = methods.rel_type_already_exists(
                            "has vendor")
                        if vendor_rel_type == None:
                            vendor_rel_type = RelationshipType.RelationshipType(
                                "has vendor")
                            methods.add_rel_type(vendor_rel_type)
                        vendor_rel = create_relation(
                            os, vendor_ci, vendor_rel_type)
                        vendor_rel.title = "has vendor"
                        methods.add_ci(vendor_ci)
                        methods.add_rel(vendor_rel)

                        family_attr = create_attribute(
                            os, "family", osclass.get('osfamily'))
                        methods.add_attribute(family_attr)

                        generation_attr = create_attribute(
                            os, "generation", osclass.get('osgen'))
                        methods.add_attribute(generation_attr)

                else:
                    if 'osclass' in osmatch:
                        if len(list(osmatch.get('osclass'))) > 0:
                            osclass = list(osmatch.get('osclass'))[0]
                            os_attr = create_attribute(
                                host, "operating system", osclass.get('osfamily'))
                            methods.add_attribute(os_attr)
                    host_type = methods.ci_type_already_exists("Host")
                    if host_type == None:
                        host_type = ConfigurationItemType.ConfigurationItemType(
                            "Host")
                        methods.add_ci_type(host_type)
                    host.set_type(host_type.get_id())

        methods.add_ci(host)

    print(green + "\n>>> " + reset + "Nmap discovery ended.")
