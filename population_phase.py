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


def run_population(info):
    open_message = pyfiglet.figlet_format(
        "Population Phase", font="small")
    print("\n**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    population.run_cmdb_population(info)
