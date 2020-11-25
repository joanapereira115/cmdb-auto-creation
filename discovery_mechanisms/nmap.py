# -*- coding: utf-8 -*-

import regex
import nmap
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods
import nmap
from discovery import discovery_info

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_nmap(ip):
    """
    Obtains information about the machine using the Nmap tool.
    Gathers data about addresses, status, ports, device types and operating systems families.

    Parameters
    --------
    ip : string
        The IP address of the machine.
    """
    print(blue + "\n>>> " + reset +
          "NMAP discovery in the address " + str(ip) + "...")

    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-PR -sV -A -R')

    for h in nm.all_hosts():
        host_type = None
        host = ConfigurationItem.ConfigurationItem()
        host.add_ipv4_address(ip)
        mac = discovery_info.get_mac_from_ip(ip)
        if mac != None:
            host.set_mac_address(mac)

        addresses = nm[h].get("addresses")
        for addr in addresses:
            if addr == "ipv4":
                host.add_ipv4_address(addresses.get(addr))
            if addr == "ipv6":
                host.add_ipv6_address(addresses.get(addr))
            elif addr == "mac":
                discovery_info.add_mac(addresses.get(addr))
                discovery_info.add_ip_to_mac(ip, addresses.get(addr))
                host.set_mac_address(addresses.get(addr))

        hostnames = nm[h].get("hostnames")
        for hostname in hostnames:
            name = hostname.get("name")
            if name != None and name != "":
                methods.define_attribute("hostname", name, host)

        v = list(nm[h].get("vendor").values())
        if len(v) > 0:
            vendor = list(nm[h].get("vendor").values())[0]
            vendor_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Vendor"))
            vendor_obj = ConfigurationItem.ConfigurationItem()
            vendor_obj.set_title(vendor)
            vendor_obj.set_type(vendor_type.get_id())

            rel_type_obj_vendor = methods.add_rel_type(
                RelationshipType.RelationshipType("has vendor"))
            rel_obj_vendor = methods.create_relation(
                host, vendor_obj, rel_type_obj_vendor)
            rel_obj_vendor.title = str(host.get_title()) + \
                " has vendor " + str(vendor_obj.get_title())

            rel_type_vendor_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("is vendor of"))
            rel_vendor_obj = methods.create_relation(
                vendor_obj, host, rel_type_vendor_obj)
            rel_vendor_obj.title = str(vendor_obj.get_title()) + \
                " is vendor of " + str(host.get_title())

            methods.add_ci(vendor_obj)
            methods.add_rel(rel_obj_vendor)
            methods.add_rel(rel_vendor_obj)

        status = nm[h].get("status").get("state")
        host.set_status(status)

        for proto in nm[h].all_protocols():
            ports = nm[h][proto].keys()
            for port in ports:
                port_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Port"))
                p = ConfigurationItem.ConfigurationItem()
                p.set_type(port_type.get_id())
                p.set_title(port)

                methods.define_attribute("protocol", proto, p)

                proto_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Protocol"))
                protocol = ConfigurationItem.ConfigurationItem()
                protocol.set_type(proto_type.get_id())
                protocol.set_title(proto)

                rel_type_port_proto = methods.add_rel_type(
                    RelationshipType.RelationshipType("has protocol"))
                rel_port_proto = methods.create_relation(
                    p, protocol, rel_type_port_proto)
                rel_port_proto.title = str(p.get_title()) + \
                    " has protocol " + str(protocol.get_title())

                rel_type_proto_port = methods.add_rel_type(
                    RelationshipType.RelationshipType("is protocol of"))
                rel_proto_port = methods.create_relation(
                    protocol, p, rel_type_proto_port)
                rel_proto_port.title = str(protocol.get_title()) + \
                    " is protocol of " + str(p.get_title())

                methods.add_ci(protocol)
                methods.add_rel(rel_port_proto)
                methods.add_rel(rel_proto_port)

                if nm[h][proto][port]['state'] != '':
                    p.set_status(nm[h].get(proto).get(port).get('state'))
                if nm[h][proto][port]['cpe'] != '':
                    methods.define_attribute(
                        "cpe", nm[h].get(proto).get(port).get('cpe'), p)

                prod = nm[h].get(proto).get(port).get('name')
                methods.define_attribute("product", prod, p)

                product_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Product"))
                product = ConfigurationItem.ConfigurationItem()
                product.set_type(product_type.get_id())
                product.set_title(prod)
                product.set_description(
                    nm[h].get(proto).get(port).get('product'))
                methods.define_attribute(
                    "version", nm[h].get(proto).get(port).get('version'), product)

                rel_type_port_product = methods.add_rel_type(
                    RelationshipType.RelationshipType("running product"))
                rel_port_product = methods.create_relation(
                    p, product, rel_type_port_product)
                rel_port_product.title = str(p.get_title()) + \
                    " running product " + str(product.get_title())

                rel_type_product_port = methods.add_rel_type(
                    RelationshipType.RelationshipType("is running on port"))
                rel_product_port = methods.create_relation(
                    product, p, rel_type_product_port)
                rel_product_port.title = str(product.get_title()) + \
                    " is running on port " + str(p.get_title())

                methods.add_ci(product)
                methods.add_rel(rel_port_product)
                methods.add_rel(rel_product_port)

                rel_type_port_host = methods.add_rel_type(
                    RelationshipType.RelationshipType("port from"))
                rel_port_host = methods.create_relation(
                    p, host, rel_type_port_host)
                rel_port_host.title = str(p.get_title()) + \
                    " port from " + str(host.get_title())

                rel_type_host_port = methods.add_rel_type(
                    RelationshipType.RelationshipType("has port"))
                rel_host_port = methods.create_relation(
                    host, p, rel_type_host_port)
                rel_host_port.title = str(host.get_title()) + \
                    " has port " + str(p.get_title())

                methods.add_ci(p)
                methods.add_rel(rel_port_host)
                methods.add_rel(rel_host_port)

        if 'osmatch' in nm[h]:
            if len(list(nm[h]['osmatch'])) > 0:
                osmatch = list(nm[h]['osmatch'])[0]
                if 'osclass' in osmatch:
                    if len(list(osmatch.get('osclass'))) > 0:
                        osclass = list(osmatch.get('osclass'))[0]
                        host.set_os_family(osclass.get('osfamily'))

                    if osclass.get('type') == "general purpose":
                        host_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType("Host"))
                    else:
                        host_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType(osclass.get('type')))

        if host_type == None:
            host_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Host"))

        host.set_type(host_type.get_id())
        methods.add_ci(host)
