# -*- coding: utf-8 -*-

from colored import fg, attr
import pyfiglet

from cmdb_population import population

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_population(db_info, cmdb_info):
    """
    Executes the population of the CMDB. 

    Parameters
    -------
    db_info : dict
        The information about the database.

    cmdb_info : dict
        The information about the CMDB.
    """
    open_message = pyfiglet.figlet_format(
        "Population Phase", font="small")
    print("\n**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    population.run_cmdb_population(db_info, cmdb_info)
