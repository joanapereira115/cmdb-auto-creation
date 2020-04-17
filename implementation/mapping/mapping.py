#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

import model_parser
#import automatic_model_mapper


class HostValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address',
                cursor_position=len(document.text))  # Move cursor to end


class PortValidator(Validator):
    def validate(self, document):
        ok = int(document.text) > 0 and int(document.text) < 49152
        if not ok:
            raise ValidationError(
                message='Please enter a valid port number',
                cursor_position=len(document.text))  # Move cursor to end


class NotEmpty(Validator):
    def validate(self, document):
        ok = document.text != "" and document.text != None
        if not ok:
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text))  # Move cursor to end


def run_mapping():
    style = style_from_dict({
        Token.QuestionMark: '#B54653 bold',
        Token.Selected: '#86DEB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#46B1C9 bold',
        Token.Question: '',
    })

    print("\n*******************************************")
    print("Mapping Phase")
    print("*******************************************\n")

    mapper_questions = [
        {
            'type': 'list',
            'name': 'engine',
            'message': 'What\'s the database engine of your CMDB?',
            'choices': ['PostgresSQL', 'MySQL', 'MariaDB', 'Oracle'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'What\'s the name of your CMDB?',
            'validate': NotEmpty
        },
        {
            'type': 'input',
            'name': 'host',
            'message': 'What\'s the IP of the host running the CMDB? (127.0.0.1 for localhost)',
            'validate': HostValidator
        },
        {
            'type': 'input',
            'name': 'port',
            'message': 'What\'s the port number running the CMDB?',
            'validate': PortValidator,
            'filter': lambda val: int(val)
        },
        {
            'type': 'input',
            'name': 'user',
            'message': 'What\'s the user for your CMDB?',
            'validate': NotEmpty
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'What\'s the password for your CMDB?'
        }
    ]

    mapper_answers = prompt(mapper_questions, style=style)
    cmdb_process = model_parser.final(mapper_answers)
    # automatic_model_mapper.final(cmdb_process)
