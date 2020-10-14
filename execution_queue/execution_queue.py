#!/usr/bin/env python3

from discovery_mechanisms import nmap, snmp
#from discovery_mechanisms_configuration import conf


def execute(mechanisms, addresses):
    for m in mechanisms:
        if m == "nmap":
            nmap.run_nmap(addresses)
        elif m == "snmp":
            snmp.run_snmp(addresses)
