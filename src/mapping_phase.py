# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import pyfiglet

from cmdb_processor import i_doit_processor, itop_processor
from db_processor import db_processor
from model_mapper import mapper
from db_processor import db_info

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
    Token.Instruction: '',
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


def choose_software():
    """
    Asks the user which CMDB software is he using.

    Returns
    -------
    string
        The CMDB software selected by the user.
    """
    # TODO: handle other CMDBs
    cmdb_software = [
        {
            'type': 'list',
            'message': 'What is the software of the CMDB?',
            'name': 'software',
            'choices': [{'name': 'i-doit'}, {'name': 'iTop'}]
        }
    ]

    cmdb_software_answer = prompt(cmdb_software, style=style)
    cmdb = cmdb_software_answer.get("software")
    return cmdb


def run_mapping(db):
    """
    Executes the mapping between the CMDB and the database data models. 

    Returns
    -------
    dict, dict
        Returns the information about the database and the CMDB information.
    """
    cmdb_info = {}

    open_message = pyfiglet.figlet_format(
        "Mapping Phase", font="small")
    print()
    print(
        "\033[1m**********************************************************************\033[0m")
    print(open_message)
    print(
        "\033[1m**********************************************************************\033[0m\n")

    db_processor.process_db_data_model(db)

    cmdb = choose_software()

    cmdb_info["software"] = cmdb

    if cmdb == "i-doit":
        cmdb_info["cmdb"] = i_doit_processor.process_i_doit()
    if cmdb == "iTop":
        cmdb_info["cmdb"] = itop_processor.process_itop()

    mapper.run_mapper()

    return cmdb_info
