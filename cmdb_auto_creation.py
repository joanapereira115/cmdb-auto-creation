#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyfiglet
from colored import fg, bg, attr
import warnings
import subprocess
import os
import shlex
import sys

from discovery_mechanisms import snmp, nmap
from discovery_phase import run_discovery
from mapping_phase import run_mapping
from population_phase import run_population

warnings.filterwarnings("ignore")

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def main():
    if os.getuid() != 0:
        print(red + "\n>>> " + reset + "Need root permissions.\n")
        subprocess.call(shlex.split('sudo ' + str(sys.argv[0])))
    else:
        open_message = pyfiglet.figlet_format("CMDB Automatic Creation")
        print(open_message)
        # run_discovery()
        # info = run_mapping()
        # run_population(info)
        # snmp.run_snmp("192.168.1.60-75")
        nmap.run_nmap("192.168.1.60-75")


main()
