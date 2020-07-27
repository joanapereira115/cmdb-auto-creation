#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError


def run_discovery():
    style = style_from_dict({
        Token.QuestionMark: '#B54653 bold',
        Token.Selected: '#86DEB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#46B1C9 bold',
        Token.Question: '',
    })

    print("*******************************************")
    print("Discovery Phase")
    print("*******************************************\n")

    discovery_questions = [
        {
            'type': 'checkbox',
            'message': 'What IT infrastructure categories would you want to discover?',
            'name': 'categories',
            'choices': [
                {'name': 'Data Centers', 'disabled': 'impossible'},
                {'name': 'Network'},
                {'name': 'Compute'},
                {'name': 'Storage'},
                {'name': 'Operating Systems'},
                {'name': 'End User Devices'},
                {'name': 'Software'},
                {'name': 'Data Bases'},
                {'name': 'Services'},
                {'name': 'People'},
                {'name': 'Documents'}
            ],
            'validate': lambda answer: len(answer) > 0 or 'You must choose at least one category.'
        }
    ]

    discovery_answers = prompt(discovery_questions, style=style)
    return discovery_answers
