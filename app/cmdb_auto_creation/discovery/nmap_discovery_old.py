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

import models
from objects import objects
from passwd_vault import vault
from reconciliation import reconcile
from normalization import normalize

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# tirar isto
nmap_res = [
    {
        "ipv4": "192.168.1.1",
        "state": "up",
        "hostname": "",
        "ports": [
            {
                "number": 80,
                "protocol": "tcp",
                "state": "open",
                "name": "http"
            },
            {
                "number": 81,
                "protocol": "tcp",
                "state": "filtered",
                "name": "hosts2-ns"
            },
            {
                "number": 82,
                "protocol": "tcp",
                "state": "filtered",
                "name": "xfer"
            },
            {
                "number": 83,
                "protocol": "tcp",
                "state": "filtered",
                "name": "mit-ml-dev"
            },
            {
                "number": 443,
                "protocol": "tcp",
                "state": "filtered",
                "name": "https"
            },
            {
                "number": 1080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "socks"
            },
            {
                "number": 3128,
                "protocol": "tcp",
                "state": "filtered",
                "name": "squid-http"
            },
            {
                "number": 4567,
                "protocol": "tcp",
                "state": "open",
                "name": "tram"
            },
            {
                "number": 8000,
                "protocol": "tcp",
                "state": "filtered",
                "name": "http-alt"
            },
            {
                "number": 8080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "http-proxy"
            },
            {
                "number": 8088,
                "protocol": "tcp",
                "state": "filtered",
                "name": "radan-http"
            },
            {
                "number": 8089,
                "protocol": "tcp",
                "state": "open",
                "name": "unknown"
            },
            {
                "number": 8888,
                "protocol": "tcp",
                "state": "filtered",
                "name": "sun-answerbook"
            }
        ]
    },
    {
        "ipv4": "192.168.1.2",
        "state": "up",
        "hostname": "",
        "ports": [
            {
                "number": 22,
                "protocol": "tcp",
                "state": "open",
                "name": "ssh"
            },
            {
                "number": 80,
                "protocol": "tcp",
                "state": "open",
                "name": "http"
            },
            {
                "number": 81,
                "protocol": "tcp",
                "state": "filtered",
                "name": "hosts2-ns"
            },
            {
                "number": 82,
                "protocol": "tcp",
                "state": "filtered",
                "name": "xfer"
            },
            {
                "number": 83,
                "protocol": "tcp",
                "state": "filtered",
                "name": "mit-ml-dev"
            },
            {
                "number": 443,
                "protocol": "tcp",
                "state": "filtered",
                "name": "https"
            },
            {
                "number": 1080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "socks"
            },
            {
                "number": 3128,
                "protocol": "tcp",
                "state": "filtered",
                "name": "squid-http"
            },
            {
                "number": 8000,
                "protocol": "tcp",
                "state": "filtered",
                "name": "http-alt"
            },
            {
                "number": 8080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "http-proxy"
            },
            {
                "number": 8088,
                "protocol": "tcp",
                "state": "filtered",
                "name": "radan-http"
            },
            {
                "number": 8888,
                "protocol": "tcp",
                "state": "filtered",
                "name": "sun-answerbook"
            }
        ]
    },
    {
        "ipv4": "192.168.1.9",
        "state": "up",
        "hostname": "",
        "ports": [
            {
                "number": 80,
                "protocol": "tcp",
                "state": "open",
                "name": "http"
            },
            {
                "number": 81,
                "protocol": "tcp",
                "state": "filtered",
                "name": "hosts2-ns"
            },
            {
                "number": 82,
                "protocol": "tcp",
                "state": "filtered",
                "name": "xfer"
            },
            {
                "number": 83,
                "protocol": "tcp",
                "state": "filtered",
                "name": "mit-ml-dev"
            },
            {
                "number": 135,
                "protocol": "tcp",
                "state": "open",
                "name": "msrpc"
            },
            {
                "number": 139,
                "protocol": "tcp",
                "state": "open",
                "name": "netbios-ssn"
            },
            {
                "number": 443,
                "protocol": "tcp",
                "state": "open",
                "name": "https"
            },
            {
                "number": 445,
                "protocol": "tcp",
                "state": "open",
                "name": "microsoft-ds"
            },
            {
                "number": 554,
                "protocol": "tcp",
                "state": "open",
                "name": "rtsp"
            },
            {
                "number": 1080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "socks"
            },
            {
                "number": 2869,
                "protocol": "tcp",
                "state": "open",
                "name": "icslap"
            },
            {
                "number": 3128,
                "protocol": "tcp",
                "state": "filtered",
                "name": "squid-http"
            },
            {
                "number": 3389,
                "protocol": "tcp",
                "state": "open",
                "name": "ms-wbt-server"
            },
            {
                "number": 5357,
                "protocol": "tcp",
                "state": "open",
                "name": "wsdapi"
            },
            {
                "number": 8000,
                "protocol": "tcp",
                "state": "open",
                "name": "http-alt"
            },
            {
                "number": 8080,
                "protocol": "tcp",
                "state": "filtered",
                "name": "http-proxy"
            },
            {
                "number": 8088,
                "protocol": "tcp",
                "state": "filtered",
                "name": "radan-http"
            },
            {
                "number": 8888,
                "protocol": "tcp",
                "state": "filtered",
                "name": "sun-answerbook"
            },
            {
                "number": 10243,
                "protocol": "tcp",
                "state": "open",
                "name": "unknown"
            }
        ]
    }
]

"""
def give_sudo():
    euid = os.geteuid()
    if euid != 0:
        print(red + ">>> " + reset + "Need root permission. Running sudo...")
        user = getpass.getuser()
        password = vault.show_secret(user)

        p = subprocess.Popen(["sudo", "-S", "python", "./discovery/nmap_discovery.py"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write((password + '\n').encode())
        p.stdin.close()

        print("euid: " + str(os.geteuid()))
    """


def test_nmap():
    create_objects(nmap_res)


def run_nmap(addresses):
    res = []
    print(blue + ">>> " + reset + "Exploring addresses from " +
          addresses.split('-')[0] + " to " + addresses.split('-')[0][:-3] + addresses.split('-')[1] + " using nmap...")
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)

    nm.scan(addresses)
    for host in nm.all_hosts():
        ci = {}
        for addr in nm[host]['addresses']:
            ci[addr] = nm[host]['addresses'][addr]
        ci['state'] = nm[host].state()
        ci['hostname'] = nm[host].hostname()
        if nm[host]['vendor'] != {}:
            i = list(nm[host]['vendor'].keys())[0]
            ci['vendor'] = nm[host]['vendor'][i]
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            ports = []
            for port in lport:
                p = {}
                p['number'] = port
                p['protocol'] = proto
                if nm[host][proto][port]['state'] != '':
                    p['state'] = nm[host][proto][port]['state']
                if nm[host][proto][port]['cpe'] != '':
                    p['cpe'] = nm[host][proto][port]['cpe']
                if nm[host][proto][port]['name'] != '':
                    p['name'] = nm[host][proto][port]['name']
                if nm[host][proto][port]['product'] != '':
                    p['product'] = nm[host][proto][port]['product']
                if nm[host][proto][port]['version'] != '':
                    p['version'] = nm[host][proto][port]['version']
                if nm[host][proto][port]['extrainfo'] != '':
                    p['extrainfo'] = nm[host][proto][port]['extrainfo']
                ports.append(p)
            ci['ports'] = ports
        res.append(ci)
    print(green + ">>> " + reset + "Addresses explored.")
    print(res)
    create_objects(res)


def create_objects(discovered):
    res = []
    i = 1
    for host in discovered:
        h = models.Element()
        h.ci_type = "Host"
        h.id = i
        i += 1
        if "ipv4" in host:
            ipv4 = models.Element()
            ipv4.ci_type = "IPv4"
            ipv4.id = i
            i += 1
            ipv4.value = normalize(host["ipv4"])
            rel1 = create_relation(h, ipv4, "has address")
            rel2 = create_relation(ipv4, h, "address of")

            res.append(ipv4)
            res.append(rel1)
            res.append(rel2)
        if "ipv6" in host:
            ipv6 = models.Element()
            ipv6.ci_type = "IPv6"
            ipv6.id = i
            i += 1
            ipv6.value = normalize(host["ipv6"])
            rel3 = create_relation(h, ipv6, "has address")
            rel4 = create_relation(ipv6, h, "address of")

            res.append(ipv6)
            res.append(rel3)
            res.append(rel4)
        if "mac" in host:
            mac = models.Element()
            mac.ci_type = "MAC address"
            mac.id = i
            i += 1
            mac.value = normalize(host["mac"])
            rel5 = create_relation(h, mac, "has address")
            rel6 = create_relation(mac, h, "address of")

            res.append(mac)
            res.append(rel5)
            res.append(rel6)
        if "vendor" in host:
            h.manufacturer = normalize(host["vendor"])
        h.status = normalize(host["state"])
        h.name = normalize(host["hostname"])
        for port in host["ports"]:
            proto = models.exist_element("Protocol", port["protocol"])
            if models.exist_element("Protocol", port["protocol"]) == None:
                proto = models.Element()
                proto.id = i
                i += 1
                proto.ci_type = "Protocol"
                proto.name = normalize(port["protocol"])
            p = models.Element()
            p.ci_type = "Port"
            p.id = i
            i += 1
            p.value = normalize(str(port['number']))
            if 'state' in port:
                p.status = normalize(port['state'])
            if 'name' in port:
                p.name = normalize(port['name'])
            if 'product' in port:
                p.manufacturer = normalize(port['product'])
            if 'version' in port:
                p.version = normalize(port['version'])
            if 'extrainfo' in port:
                p.description = normalize(port['extrainfo'])

            rel7 = create_relation(h, p, "has port")
            rel8 = create_relation(p, h, "port in")
            rel9 = create_relation(p, proto, "has protocol")
            rel10 = create_relation(proto, p, "protocol of")

            res.append(p)
            res.append(proto)
            res.append(rel7)
            res.append(rel8)
            res.append(rel9)
            res.append(rel10)
        res.append(h)
    reconcile(res)
    return res


def create_relation(source, target, relation):
    rel = models.Relation()
    rel.rel_type = relation
    rel.source_id = source.id
    rel.source_type = source.ci_type
    rel.target_id = target.id
    rel.target_type = target.ci_type
    return rel


# run_nmap("192.168.1.1-10")
