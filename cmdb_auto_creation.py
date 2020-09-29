#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyfiglet
from colored import fg, bg, attr

from discovery_phase import run_discovery
from mapping_phase import run_mapping
from population_phase import run_population
import warnings

warnings.filterwarnings("ignore")

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def main():
    open_message = pyfiglet.figlet_format("CMDB Automatic Creation")
    print(open_message)
    # run_discovery()
    info = run_mapping()
    """
    info = {
        "cmdb": {"server": "192.168.1.72", "username": "admin", "password": "admin", "api_key": "joana"},
        "db": {"server": "192.168.1.72", "port": "7200", "repository": "cmdb"}
    }
    """
    run_population(info)


main()
