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
            'choices': [{'name': 'i-doit'}, {'name': 'iTop'}, {'name': 'Other', 'disabled': 'unavailable'}]
        }
    ]

    cmdb_software_answer = prompt(cmdb_software, style=style)
    cmdb = cmdb_software_answer.get("software")
    return cmdb


def choose_connection_method(cmdb):
    """
    Asks the user which type of connection is going to be used to access to it's CMDB.

    Parameters
    ----------
    cmdb : string
        The CMDB software selected by the user.

    Returns
    -------
    string
        The type of connection selected by the user.
    """
    # TODO: handle other connections and software
    if cmdb == 'i-doit':
        connection_question = [
            {
                'type': 'list',
                'message': 'How to connect to the CMDB?',
                'name': 'connection',
                'choices': [{'name': 'API'}]
            }
        ]
    if cmdb == 'iTop':
        connection_question = [
            {
                'type': 'list',
                'message': 'How to connect to the CMDB?',
                'name': 'connection',
                'choices': [{'name': 'Database'}]
            }
        ]
    connection_answer = prompt(connection_question, style=style)
    connection = connection_answer["connection"]
    return connection


def run_mapping():
    """
    Executes the mapping between the CMDB and the database data models. 

    Returns
    -------
    dict, dict
        Returns the information about the database and the CMDB information.
    """
    cmdb_info = {}
    db = {}

    open_message = pyfiglet.figlet_format(
        "Mapping Phase", font="small")
    print("**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    db = db_info.get_db_info()
    db_processor.process_db_data_model(db)

    cmdb = choose_software()
    connection = choose_connection_method(cmdb)

    cmdb_info["software"] = cmdb
    cmdb_info["connection"] = connection

    if cmdb == "i-doit" and connection == "API":
        cmdb_info["cmdb"] = i_doit_processor.process_i_doit()
    if cmdb == "iTop" and connection == "Database":
        cmdb_info["cmdb"] = itop_processor.process_itop()

    mapper.run_mapper()

    return db, cmdb_info
