#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from colored import fg, bg, attr

from .nmap_discovery import run_nmap

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


class NotEmpty(Validator):
    def validate(self, document):
        ok = document.text != "" and document.text != None
        if not ok:
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text))  # Move cursor to end


style = style_from_dict({
    Token.QuestionMark: '#B54653 bold',
    Token.Selected: '#86DEB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


def run_primary_discovery():
    print("*******************************************")
    print("Primary Discovery Phase")
    print("*******************************************\n")

    addresses = ""

    # TODO: deixar selecionar apenas sim ou não
    range_question = [
        {
            'type': 'checkbox',
            'message': 'Do you want to specify the address range?',
            'name': 'address_range',
            'choices': [
                {'name': 'Yes'},
                {'name': 'No'}
            ],
            'validate': lambda answer: len(answer) > 0 or 'You must choose at least one category.'
        }
    ]

    range_answer = prompt(range_question, style=style)

    # TODO: mais do que um intervalo
    if range_answer['address_range'][0] == "Yes":
        addresses_question = [
            {
                'type': 'input',
                'name': 'name',
                'message': 'Enter the address range you want to discover. (Use format xxx.xxx.xxx.yyy-zzz)',
                'validate': NotEmpty
            }
        ]
        addresses_answer = prompt(addresses_question, style=style)
        addresses = addresses_answer
        print(addresses_answer)

    else:
        print(blue + ">>> " + reset + "Finding active IP addresses...")
        # TODO: descobrir endereços IP ativos
        addresses = "192.168.001.001-006"

    run_nmap(addresses)
