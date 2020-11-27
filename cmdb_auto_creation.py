#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyfiglet
from colored import fg, attr
import warnings
import subprocess
import os
import shlex
import sys
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from discovery_mechanisms import snmp, nmap
from discovery_phase import run_discovery
from mapping_phase import run_mapping
from population_phase import run_population
from password_vault import vault

style = style_from_dict({
    Token.QuestionMark: '#B54653 bold',
    Token.Selected: '#86DEB7 bold',
    Token.Instruction: '',
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})

warnings.filterwarnings("ignore")

"""
    Color definition.
"""
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
                cursor_position=len(document.text))


def define_vault_password():
    """
    Asks the user for a password to associate to the vault.

    Returns
    -------
    string
        Returns the password.
    """
    password_vault = [
        {
            'type': 'password',
            'message': 'Enter your vault password:',
            'name': 'password',
            'validate': NotEmpty
        },
        {
            'type': 'password',
            'message': 'Repeat your vault password:',
            'name': 'check_password',
            'validate': NotEmpty
        }
    ]
    password_answer = prompt(password_vault, style=style)
    passwd = password_answer.get("password")
    check_passwd = password_answer["check_password"]
    if passwd != check_passwd:
        print(red + "\n>>> " + reset + "Passwords do not match.\n")
        return define_vault_password()
    else:
        if len(passwd) < 8:
            print(red + "\n>>> " + reset +
                  "The password should be at least 8 characters.\n")
            return define_vault_password()
        else:
            return passwd


def delete_vault():
    """
    Asks the user if he wants to delete the password vault.

    Returns
    -------
    boolean
        Returns true if the user wants to delete the vault, and false if not.
    """
    print()
    delete_vault = [
        {
            'type': 'list',
            'message': 'Do you want to delete the password vault?',
            'name': 'delete',
            'choices': [{'name': 'No'}, {'name': 'Yes'}]
        }
    ]

    delete_vault_answer = prompt(delete_vault, style=style)
    if delete_vault_answer.get('delete') == "Yes":
        return True
    else:
        return False


def main():
    """
    Executes the complete process of automatic CMDB creation.
    """
    if os.getuid() != 0:
        print(red + "\n>>> " + reset + "Need root permissions.\n")
        subprocess.call(shlex.split('sudo ' + str(sys.argv[0])))
    else:
        open_message = pyfiglet.figlet_format("CMDB Automatic Creation")
        print(
            "\033[1m======================================================================================= \033[0m")
        print("\033[1m" + str(open_message) + "\033[0m")
        print("\033[1m=======================================================================================\n \033[0m")

        vault.initialize()
        if vault.password_already_definined() == False:
            print(blue + "\n>>> " + reset + "Defining vault password...\n")
            pwd = define_vault_password()
            vault.define_master_key(pwd)

        run_discovery()
        db_info, cmdb_info = run_mapping()
        run_population(db_info, cmdb_info)

        if delete_vault() == True:
            vault.delete_vault()
        else:
            vault.lock()


main()
