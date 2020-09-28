# -*- coding: utf-8 -*-

from model_mapper import transformation_rules
from colored import fg, bg, attr
import pyfiglet

from cmdb_population import population

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def get_transformation_rules():
    # rules = transformation_rules.rules
    rules = {
        'ci_types': {
            'Router': 'C__OBJTYPE__ROUTER'
        },
        'rel_types': {
            'Network connection': 'C__RELATION_TYPE__NET_CONNECTIONS'
        },
        'ci_attributes': {
            'Router': {
                'serial_number': 'serial',
                'name': 'title',
                'description': 'description',
                'status': 'status'
            }
        },
        'rel_attributes': {
            'Network connection': {}
        }
    }
    return rules


def run_population(info):
    open_message = pyfiglet.figlet_format(
        "Population Phase", font="small")
    print("**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")
    rules = get_transformation_rules()
    population.run_cmdb_population(info, rules)
