#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex
import nmap

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from colored import fg, bg, attr

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_nmap(addresses):
    print(blue + ">>> " + reset + "Exploring addresses from " +
          addresses.split('-')[0] + " to " + addresses.split('-')[0][:-3] + addresses.split('-')[1] + "...")
    nm = nmap.PortScanner()
    nm.scan(addresses)
    nmap_finds = nm.csv()
    print(nmap_finds)
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
