#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import pyfiglet
from colored import fg, bg, attr

#import what2discover
#import mapping
#import population
from primary_discovery import primary_discover

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

open_message = pyfiglet.figlet_format("CMDB Automatic Creation")


def creation():

    print(open_message)

    primary_discover.run_primary_discovery()
    #discovery_answers = what2discover.run_discovery()

    # if len(discovery_answers['categories']) > 0:
    #    print(blue + "\n>>> " + reset + "Discovering:")
    #    for c in discovery_answers['categories']:
    #        print("\t" + blue + c + reset)
    #    mapping_result = mapping.run_mapping()
    #    print("\nMapping results:\n" + str(mapping_result))

    #    if(len(mapping_result) > 0):
    #        population.run_population()

    # else:
    #    print(red + "\n>>> " + reset + "You must choose at least one category.\n")
    #    creation()


creation()
