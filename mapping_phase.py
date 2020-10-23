# -*- coding: utf-8 -*-

from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import getpass
import regex
import pyfiglet

from cmdb_processor import i_doit_processor, itop_processor
from db_processor import db_processor
from model_mapper import mapper

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
    Token.Instruction: '',  # default
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


def choose_software():
    # TODO: desenvolver para outro tipo de software
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
    # TODO: desenvolver para as bases de dados
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


def run_mapping(db_info):
    cmdb_info = {}

    open_message = pyfiglet.figlet_format(
        "Mapping Phase", font="small")
    print("**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    cmdb = choose_software()
    connection = choose_connection_method(cmdb)

    cmdb_info["software"] = cmdb
    cmdb_info["connection"] = connection

    if cmdb == "i-doit" and connection == "API":
        # {"server": "", "username": "", "password": "", "api_key": ""}
        cmdb_info["cmdb"] = i_doit_processor.process_i_doit()
    if cmdb == "iTop" and connection == "Database":
        # {"server": "", "username": "", "password": "", "api_key": ""}
        cmdb_info["cmdb"] = itop_processor.process_itop()
    # {"server": "", "port": "", "repository": ""}
    # cmdb_info["db"] = db_processor.process_db_data_model()
    db_processor.process_db_data_model(db_info)

    mapper.run_mapper()

    return cmdb_info
