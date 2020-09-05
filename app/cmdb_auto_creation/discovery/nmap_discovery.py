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

import models
from objects import objects
from passwd_vault import vault
from reconciliation import reconcile
from normalization import normalize


blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def create_relation(source, target, relation):
    rel = models.Relation()
    rel.rel_type = relation
    rel.source_id = source.get_id()
    rel.source_type = source.ci_type
    rel.target_id = target.get_id()
    rel.target_type = target.ci_type
    return rel

# TODO: melhorar isto


def already_discovered(ci_type, name, res):
    for o in res:
        if type(o) is models.Element:
            if o.ci_type == ci_type and o.name == name:
                # print("Object found: " + str(o.element_print()))
                return o
    return None


def run_nmap(addresses):
    res = []
    print(blue + ">>> " + reset + "Exploring addresses from " +
          addresses.split('-')[0] + " to " + addresses.split('-')[0][:-3] + addresses.split('-')[1] + " using nmap...")
    # tirar
    vault.initialize()
    vault.unlock('olaolaola')
    user = getpass.getuser()
    password = vault.show_secret(user)
    p = subprocess.Popen(["sudo", "-S", "nmap", "-R", "-A", "--osscan-limit", "--traceroute", "-sV", "-oX", "nmap.xml", addresses],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write((password + '\n').encode())
    p.stdin.close()
    p_status = p.wait()


def parse_nmap_results():
    res = []
    tree = ET.parse(
        '/Users/Joana/Desktop/tese/git/cmdb-automatic-creation/app/cmdb_auto_creation/nmap.xml')
    root = tree.getroot()
    for child in root:
        if child.tag == "host":
            print(blue + ">>> " + reset + "Parsing host...")
            h = models.Element()
            # mudar isto
            h.ci_type = "Host"
            h.name = "Host" + str(h.get_id())
            #
            for element in child:
                if element.tag == "status":
                    if "state" in element.attrib:
                        h.status = normalize(element.attrib["state"])

                if element.tag == "address":
                    ad = models.Element()
                    if "addr" in element.attrib:
                        ad.value = normalize(element.attrib["addr"])
                    if "addrtype" in element.attrib:
                        ad.ci_type = normalize(element.attrib["addrtype"])
                    if "vendor" in element.attrib:
                        h.manufacturer = normalize(element.attrib["vendor"])

                    rel1 = create_relation(h, ad, "has_address")
                    rel2 = create_relation(ad, h, "address_of")

                    res.append(ad)
                    res.append(rel1)
                    res.append(rel2)

                # if tag.tag == "hostnames":

                if element.tag == "ports":
                    for p in element:
                        if p.tag == "port":
                            port = models.Element()
                            port.ci_type = "Port"

                            if "protocol" in p.attrib:
                                proto = already_discovered(
                                    "Protocol", normalize(p.attrib["protocol"]), res)
                            if proto == None:
                                proto = models.Element()
                                proto.ci_type = "Protocol"
                                proto.name = normalize(p.attrib["protocol"])
                                rel3 = create_relation(
                                    port, proto, "has_protocol")
                                rel4 = create_relation(
                                    proto, port, "protocol_of")
                                res.append(proto)
                                res.append(rel3)
                                res.append(rel4)

                            if "portid" in p.attrib:
                                port.number = normalize(p.attrib["portid"])

                                for port_attr in p:
                                    if port_attr.tag == "state":
                                        if "state" in port_attr.attrib:
                                            port.status = normalize(
                                                port_attr.attrib["state"])
                                    # service como ci?
                                    if port_attr.tag == "service":
                                        service = already_discovered(
                                            "Service", normalize(port_attr.attrib["name"]), res)
                                        if service == None:
                                            service = models.Element()
                                            service.ci_type = "Service"
                                            if "name" in port_attr.attrib:
                                                service.name = normalize(
                                                    port_attr.attrib["name"])
                                            if "product" in port_attr.attrib:
                                                service.manufacturer = normalize(
                                                    port_attr.attrib["product"])
                                            if "version" in port_attr.attrib:
                                                service.version = normalize(
                                                    port_attr.attrib["version"])
                                            if "extrainfo" in port_attr.attrib:
                                                service.description = normalize(
                                                    port_attr.attrib["extrainfo"])
                                            if "ostype" in port_attr.attrib:
                                                ostype = port_attr.attrib["ostype"]

                                        rel5 = create_relation(
                                            port, service, "has_service")
                                        rel6 = create_relation(
                                            service, port, "service_of")
                                        res.append(service)
                                        res.append(rel5)
                                        res.append(rel6)

                if element.tag == "os":
                    for osmatch in element:
                        if osmatch.tag == "osmatch":
                            if "accuracy" in osmatch.attrib:
                                if osmatch.attrib["accuracy"] == '100':
                                    operating_system = already_discovered(
                                        "Operating_System", normalize(osmatch.attrib["name"]), res)
                                if operating_system == None:
                                    operating_system = models.Element()
                                    operating_system.ci_type = "Operating_System"
                                    # TODO: melhorar isto
                                    if "name" in osmatch.attrib:
                                        value = osmatch.attrib["name"]
                                        name = value.split()[0]
                                        version = value.split()[1]
                                        operating_system.name = name
                                        operating_system.version = version
                                    rel7 = create_relation(
                                        port, proto, "has_protocol")
                                    rel8 = create_relation(
                                        proto, port, "protocol_of")
                                    res.append(operating_system)
                                    res.append(rel7)
                                    res.append(rel8)

                # if element.tag == "uptime":

                # if element.tag == "distance":

                # if element.tag == "trace":

                # if element.tag == "tcpsequence":

                # if element.tag == "ipidsequence":

                # if element.tag == "tcptssequence":

                # if element.tag == "times":

            res.append(h)
    print(green + ">>> " + reset + "Addresses explored.")
    reconcile(res)
    return res


# parse_nmap_results()


# run_nmap("192.168.1.1-10")
