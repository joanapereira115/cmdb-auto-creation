#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scapy.all import *
import argparse
import os
import re
from socket import gethostbyname, gethostbyaddr, herror, gaierror
from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
from easysnmp import snmp_get, snmp_set, snmp_walk

from password_vault import vault

"""
    Color definition.
"""
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


def define_snmp_community():
    print()
    community = [
        {
            'type': 'password',
            'message': 'Enter your SNMP devices\' community string:',
            'name': 'community',
            'validate': NotEmpty
        }
    ]
    community_answer = prompt(community, style=style)
    community = community_answer["community"]
    vault.add_secret('SNMP', "SNMP", community)

    print()
    more_community = [
        {
            'type': 'list',
            'message': 'Do you want to specify another SNMP community string?',
            'name': 'more',
            'choices': [{'name': 'Yes'}, {'name': 'No'}]
        }
    ]

    more_community_answer = prompt(more_community, style=style)
    if more_community_answer['more'] == "Yes":
        define_snmp_community()


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


def handle_networks(addr_range):
    s = regex.search(
        r'(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?', addr_range)
    groups = s.groups()

    part1 = []
    part2 = []
    part3 = []

    beg1 = int(groups[0])
    if groups[2] != None:
        end1 = int(groups[2])
        for i in range(beg1, end1+1):
            part1.append(i)
    else:
        part1.append(beg1)

    beg2 = int(groups[3])
    if groups[5] != None:
        end2 = int(groups[5])
        for j in range(beg2, end2+1):
            part2.append(j)
    else:
        part2.append(beg2)

    beg3 = int(groups[6])
    if groups[8] != None:
        end3 = int(groups[8])
        for k in range(beg3, end3+1):
            part3.append(k)
    else:
        part3.append(beg3)

    nets = []

    for p1 in part1:
        for p2 in part2:
            for p3 in part3:
                nets.append(str(p1) + "." + str(p2) + "." + str(p3))

    return nets


def handle_range(addr_range):
    s = regex.search(
        r'(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?', addr_range)
    groups = s.groups()
    begin = int(groups[9])
    if groups[11] == None:
        end = int(groups[9])
    else:
        end = int(groups[11])
    return (begin, end)


def scanner(net, begin, end, community):
    """
    Verificar que endereços, no intervalo especificado, estão disponíveis via snmp
    """
    available = []
    load_module("p0f")
    for i in range(begin, end+1):
        ip = net + "." + str(i)
        print(ip)
        # print(p0f(ip))

        p = IP(dst=ip)
        UDP(dport=161, sport=39445)
        SNMP(community=community, PDU=SNMPget(id=1416992799, varbindlist=[
             SNMPvarbind(oid=ASN1_OID("1.3.6.1.2.1.1.1.0"))]))
        pkt = sr1(p, timeout=1)
        if pkt != None:
            available.append(pkt.sprintf("%IP.src%"))
    return available


def snmp_info(available_ips, secrets):
    snmp_info = {}
    for secret in secrets:
        for ip in available_ips:
            # TODO: checkar a versão do SNMP
            snmp_info[ip] = {}
            try:
                info = snmp_walk('system', hostname=ip,
                                 community=secret, version=2)
                for x in info:
                    if x.oid == "sysDescr":
                        description = x.value
                    if x.oid == "sysName":
                        name = x.value
                    if x.oid == "sysUpTimeInstance":
                        uptime = x.value
                    if x.oid == "sysContact":
                        contact = x.value
                    if x.oid == "sysLocation":
                        location = x.value
                snmp_info[ip]["description"] = description
                snmp_info[ip]["name"] = name
                snmp_info[ip]["uptime"] = uptime
                snmp_info[ip]["contact"] = contact
                snmp_info[ip]["location"] = location
            except:
                print("\nAn error occured with snmp_walk.\n")
    return snmp_info


def run_snmp(address_range):
    print(blue + "\n>>> " + reset + "Configuring SNMP...\n")
    unlock_vault()
    # define_snmp_community()
    nets = handle_networks(address_range)
    secrets = vault.show_secret("SNMP")
    print()
    begin, end = handle_range(address_range)
    available_ips = []
    for secret in secrets:
        for net in nets:
            av = scanner(net, begin, end, secret)
            for a in av:
                available_ips.append(a)
    print(available_ips)
    info = snmp_info(available_ips, secrets)
    print(info)


"""
Nmap scan report for 192.168.1.67
Host is up (0.012s latency).
MAC Address: 74:8A:0D:FC:AE:FD (Arris Group)
Nmap scan report for 192.168.1.71
Host is up (0.0094s latency).
MAC Address: 9E:DE:D0:7D:DB:E1 (Unknown)
Nmap scan report for 192.168.1.72
Host is up (0.085s latency).
MAC Address: AC:F1:DF:08:BC:50 (D-Link International)
Nmap scan report for 192.168.1.74
Host is up (0.085s latency).
MAC Address: 80:35:C1:6D:EA:AE (Xiaomi Communications)
Nmap scan report for 192.168.1.76
Host is up (0.085s latency).
MAC Address: 6C:60:EB:1B:2D:35 (ZHI Yuan Electronics, Limited)
Nmap scan report for 192.168.1.254
Host is up (0.027s latency).
MAC Address: CC:19:A8:62:4B:1F (PT Inovao e Sistemas SA)
Nmap scan report for 192.168.1.73
Host is up.
"""


"""
# ['192.168.1.67', '192.168.1.71', '192.168.1.72', '192.168.1.73']
# available_ips = scanner("192.168.1", 70, 75, "public")



conf.checkIPaddr = False
fam, hw = get_if_raw_hwaddr(conf.iface)
dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(
    sport=68, dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type", "discover"), "end"])
ans, unans = srp(dhcp_discover, multi=True)
for p in ans:
    print(p[1][Ether].src, p[1][IP].src)


from fastsnmp import snmp_poller

hosts = ("192.168.1.72",)
# oids in group must be with same indexes
oid_group = {"1.3.6.1.2.1.2.2.1.2": "ifDescr",
             "1.3.6.1.2.1.2.2.1.10": "ifInOctets",
             }

community = "public"
snmp_data = snmp_poller.poller(hosts, [list(oid_group)], community)

for d in snmp_data:
    print("host=%s oid=%s.%s value=%s" % (d[0], oid_group[d[1]], d[2], d[3]))
"""
