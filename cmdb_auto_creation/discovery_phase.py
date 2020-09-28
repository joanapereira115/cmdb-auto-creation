# -*- coding: utf-8 -*-

from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import getpass
import regex
import pyfiglet

from password_vault import vault

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


class NotEmpty(Validator):
    def validate(self, document):
        ok = document.text != "" and document.text != None
        if not ok:
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text))  # Move cursor to end


class AddressRangeValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?', document.text)
        if ok:
            s = regex.search(
                r'(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?\.(\d{1,3})(-(\d{1,3}))?', document.text)
            groups = s.groups()
            x = 0
            while x < 10:
                beg = int(groups[x])
                if groups[x+2] != None:
                    end = int(groups[x+2])
                    if beg > end:
                        raise ValidationError(
                            message='Please enter a valid IPv4 address range.',
                            cursor_position=len(document.text))  # Move cursor to end
                x += 3
        else:
            raise ValidationError(
                message='Please enter a valid IPv4 address range.',
                cursor_position=len(document.text))  # Move cursor to end


def define_vault_password():
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
    passwd = password_answer["password"]
    check_passwd = password_answer["check_password"]
    if passwd != check_passwd:
        print(red + "\n>>> " + reset + "Passwords do not match.\n")
        return define_vault_password()
    else:
        if not vault.is_key_valid(passwd):
            print(red + "\n>>> " + reset +
                  "The password should be at least 8 characters.\n")
            return define_vault_password()
        else:
            return passwd


def unlock_vault():
    password_vault = [
        {
            'type': 'password',
            'message': 'Enter your vault password:',
            'name': 'password',
            'validate': NotEmpty
        }
    ]
    password_answer = prompt(password_vault, style=style)
    passwd = password_answer["password"]
    v = vault.unlock(passwd)
    if v == False:
        unlock_vault()


def vault_configuration():
    vault.initialize()
    if not os.path.isfile(vault.vault_path):
        passwd = define_vault_password()
        vault.define_master_key(passwd)
        vault.unlock(passwd)
    else:
        unlock_vault()


def machine_password():
    users = vault.get_usernames()
    user = getpass.getuser()
    if user not in users:
        password_question = [
            {
                'type': 'password',
                'message': 'Enter your password:',
                'name': 'password',
                'validate': NotEmpty
            }
        ]
        password_answer = prompt(password_question, style=style)
        passwd = password_answer["password"]
        vault.add_secret('Discovery', user, passwd)


def get_addresses():
    range_specification = [
        {
            'type': 'list',
            'message': 'Do you want to specify the IPv4 address range?',
            'name': 'range_specification',
            'choices': [{'name': 'Yes'}, {'name': 'No', 'disabled': 'unavailable'}]
        }
    ]

    range_specification_answer = prompt(range_specification, style=style)

    if range_specification_answer['range_specification'] == "Yes":
        range_question = [
            {
                'type': 'input',
                'name': 'addresses',
                'message': 'Enter the address range you want to discover (use format xxx-yyy.xxx-yyy.xxx-yyy.xxx-yyy, where \'-yyy\' is optional).',
                'validate': AddressRangeValidator
            }
        ]
        range_answer = prompt(range_question, style=style)
        addresses = range_answer["addresses"]

    else:
        # TODO: descobrir endereços IP ativos
        print(blue + "\n>>> " + reset + "Finding addresses...\n")


def what2discover():
    # TODO: atualizar as descrições das categorias
    # TODO: desenvolver mecanismos para as categorias indisponíveis
    categories_questions = [
        {
            'type': 'checkbox',
            'message': 'What IT infrastructure categories would you want to discover?',
            'name': 'categories',
            'choices': [
                {'name': 'Network - a group or system of interconnected machines', 'value': 'network',
                    'short': 'Network', 'disabled': 'unavailable'},
                {'name': 'Compute - machines, physical or virtual, located in data centers',
                    'value': 'compute', 'short': 'Compute'},
                {'name': 'End User Devices', 'value': 'end user devices',
                    'short': 'End User Devices'},
                {'name': 'Operating Systems', 'value': 'operating systems',
                    'short': 'Operating Systems'},
                {'name': 'Processing', 'value': 'processing', 'short': 'Processing'},
                {'name': 'Storage', 'value': 'storage', 'short': 'Storage'},
                {'name': 'Software', 'value': 'software', 'short': 'Software'},
                {'name': 'Virtual Machines', 'value': 'virtual machines',
                    'short': 'Virtual Machines'},
                {'name': 'Databases', 'value': 'databases', 'short': 'Databases'},
                {'name': 'Services', 'value': 'services', 'short': 'Services'},
                {'name': 'Containers', 'value': 'containers',
                    'short': 'Containers', 'disabled': 'unavailable'},
                {'name': 'Cloud Systems', 'value': 'cloud systems',
                    'short': 'Cloud Systems', 'disabled': 'unavailable'},
                {'name': 'Documents', 'value': 'documents',
                    'short': 'Documents', 'disabled': 'unavailable'},
                {'name': 'People', 'value': 'people',
                    'short': 'People', 'disabled': 'unavailable'},
                {'name': 'Data Centers', 'value': 'data centers',
                    'short': 'Data Centers', 'disabled': 'unavailable'}
            ],
            'validate': lambda answer: len(answer) > 0 or 'You must choose at least one category.'
        }
    ]

    categories_answer = prompt(categories_questions, style=style)

    categories = categories_answer["categories"]
    return categories


def run_discovery():
    open_message = pyfiglet.figlet_format(
        "Discovery Phase", font="small")
    print("**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    vault_configuration()
    machine_password()
    get_addresses()

    ##########
    # TODO: descoberta básica
    ##########

    categories = what2discover()

    ##########
    # TODO: mais intervalos?
    ##########

    ##########
    # TODO: mecanismos de descoberta
    ##########

    ##########
    # TODO: povoamento da BD
    ##########
