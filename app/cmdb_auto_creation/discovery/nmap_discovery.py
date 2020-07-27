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

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# tirar isto
nmap_res = [{'ipv4': '192.168.1.1', 'state': 'up', 'hostname': '', 'ports': [{'number': 80, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 81, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'hosts2-ns', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 82, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'xfer', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 83, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'mit-ml-dev', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 443, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'https', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 1080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'socks', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 3128, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'squid-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 4567, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tram', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8000, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'http-alt', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'http-proxy', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8088, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'radan-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8089, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'unknown', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8888, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'sun-answerbook', 'product': '', 'version': '', 'extrainfo': ''}]}, {'ipv4': '192.168.1.10', 'state': 'down', 'hostname': ''}, {'ipv4': '192.168.1.2', 'state': 'up', 'hostname': '', 'ports': [{'number': 22, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:linux:linux_kernel', 'name': 'ssh', 'product': 'Dropbear sshd', 'version': '2012.55', 'extrainfo': 'protocol 2.0'}, {'number': 80, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 81, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'hosts2-ns', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 82, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'xfer', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 83, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'mit-ml-dev', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 443, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'https', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 1080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'socks', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 3128, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'squid-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8000, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'http-alt', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'http-proxy', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8088, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'radan-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8888, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'sun-answerbook', 'product': '', 'version': '', 'extrainfo': ''}]}, {'ipv4': '192.168.1.3', 'state': 'down', 'hostname': ''}, {'ipv4': '192.168.1.4', 'state': 'down', 'hostname': ''}, {'ipv4': '192.168.1.5', 'state': 'down', 'hostname': ''}, {'ipv4': '192.168.1.6', 'state': 'up', 'hostname': '', 'ports': [{'number': 80, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 135, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': ''}, {'number': 139, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'netbios-ssn',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'product': 'Microsoft Windows netbios-ssn', 'version': '', 'extrainfo': ''}, {'number': 445, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'microsoft-ds', 'product': 'Windows 10 Pro 18362 microsoft-ds', 'version': '', 'extrainfo': 'workgroup: WORKGROUP'}, {'number': 1801, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'msmq', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 2103, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': ''}, {'number': 2105, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': ''}, {'number': 2107, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': ''}, {'number': 2869, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'http', 'product': 'Microsoft HTTPAPI httpd', 'version': '2.0', 'extrainfo': 'SSDP/UPnP'}, {'number': 8000, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}]}, {'ipv4': '192.168.1.7', 'state': 'down', 'hostname': ''}, {'ipv4': '192.168.1.8', 'state': 'up', 'hostname': '', 'ports': [{'number': 80, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 81, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'hosts2-ns', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 82, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'xfer', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 83, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'mit-ml-dev', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 135, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': ''}, {'number': 139, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'netbios-ssn', 'product': 'Microsoft Windows netbios-ssn', 'version': '', 'extrainfo': ''}, {'number': 443, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 445, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'microsoft-ds', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 554, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'rtsp', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 1080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'socks', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 2869, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'http', 'product': 'Microsoft HTTPAPI httpd', 'version': '2.0', 'extrainfo': 'SSDP/UPnP'}, {'number': 3128, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'squid-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 3389, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'ms-wbt-server', 'product': 'Microsoft Terminal Services', 'version': '', 'extrainfo': ''}, {'number': 5357, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'http', 'product': 'Microsoft HTTPAPI httpd', 'version': '2.0', 'extrainfo': 'SSDP/UPnP'}, {'number': 8000, 'protocol': 'tcp', 'state': 'open', 'cpe': '', 'name': 'tcpwrapped', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8080, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'http-proxy', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8088, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'radan-http', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 8888, 'protocol': 'tcp', 'state': 'filtered', 'cpe': '', 'name': 'sun-answerbook', 'product': '', 'version': '', 'extrainfo': ''}, {'number': 10243, 'protocol': 'tcp', 'state': 'open', 'cpe': 'cpe:/o:microsoft:windows', 'name': 'http', 'product': 'Microsoft HTTPAPI httpd', 'version': '2.0', 'extrainfo': 'SSDP/UPnP'}]}, {'ipv4': '192.168.1.9', 'state': 'down', 'hostname': ''}]


def run_nmap(addresses):
    res = []
    euid = os.geteuid()
    if euid != 0:
        user = getpass.getuser()
        password = vault.show_secret(user)
        print(red + ">>> " + reset + "Need root permission. Running sudo...")
        p = subprocess.Popen(["sudo", "-S", "./discovery/nmap_discovery.py"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write((password + '\n').encode())
        p.stdin.close()
    print(blue + ">>> " + reset + "Exploring addresses from " +
          addresses.split('-')[0] + " to " + addresses.split('-')[0][:-3] + addresses.split('-')[1] + " using nmap...")
    # descomentar isto
    nm = nmap.PortScanner()
    nm.scan(addresses, arguments="-R -A -r -sV -v")
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
                p['state'] = nm[host][proto][port]['state']
                p['cpe'] = nm[host][proto][port]['cpe']
                p['name'] = nm[host][proto][port]['name']
                p['product'] = nm[host][proto][port]['product']
                p['version'] = nm[host][proto][port]['version']
                p['extrainfo'] = nm[host][proto][port]['extrainfo']
                ports.append(p)
            ci['ports'] = ports
        if (os.getuid() == 0):
            if 'osmatch' in nm[host]:
                osmatches = []
                for osmatch in nm[host]['osmatch']:
                    osm = {}
                    osm['name'] = osmatch['name']
                    osm['line'] = osmatch['line']
                    if 'osclass' in osmatch:
                        osclasses = []
                        for osclass in osmatch['osclass']:
                            osc = {}
                            osc['type'] = osclass['type']
                            osc['vendor'] = osclass['vendor']
                            osc['family'] = osclass['osfamily']
                            osc['generation'] = osclass['osgen']
                            osclasses.append(osc)
                        osm['classes'] = osclasses
                    osmatches.append(osm)
                ci['os'] = osmatches
            if 'fingerprint' in nm[host]:
                ci['fingerprint'] = nm[host]['fingerprint']
        res.append(ci)
    print(res)
    print(green + ">>> " + reset + "Addresses explored.")
    # mudar isto
    # create_objects(nmap_res)
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
            ipv4.value = host["ipv4"]
            rel1 = create_relation(h, ipv4, "has_address")
            rel2 = create_relation(ipv4, h, "address_of")

            res.append(ipv4)
            res.append(rel1)
            res.append(rel2)
        if "mac" in host:
            mac = models.Element()
            mac.ci_type = "MAC_address"
            mac.id = i
            i += 1
            mac.value = host["mac"]
            rel3 = create_relation(h, mac, "has_address")
            rel4 = create_relation(mac, h, "address_of")

            res.append(mac)
            res.append(rel3)
            res.append(rel4)
        if "vendor" in host:
            h.manufacturer = host["vendor"]
        h.status = host["state"]
        h.name = host["hostname"]
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


# run_nmap("192.168.001.001-010")
