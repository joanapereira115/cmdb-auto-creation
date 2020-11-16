# -*- coding: utf-8 -*-

from discovery_mechanisms import nmap
from discovery_mechanisms import snmp


def basic_discovery(available_ips):
    nmap.run_nmap(available_ips)
    snmp.run_snmp(available_ips)
