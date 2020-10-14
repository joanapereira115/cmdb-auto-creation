# -*- coding: utf-8 -*-

from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import getpass
import regex
import pyfiglet
import requests


from password_vault import vault
from execution_queue import execution_queue
from db_population import population


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


class AddressValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'(\d{1,3}\.){3}\d{1,3}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address.',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'\d+', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid port number.',
                cursor_position=len(document.text))  # Move cursor to end


def define_vault_password():
    print(blue + ">>> " + reset + "Defining vault password...\n")
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
                'message': 'Enter your machine password:',
                'name': 'password',
                'validate': NotEmpty
            }
        ]
        password_answer = prompt(password_question, style=style)
        passwd = password_answer["password"]
        vault.add_secret('Discovery', user, passwd)


def get_addresses():
    # TODO: poder introduzir rede inteira x.y.z.w/24
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
        return addresses

    else:
        # TODO: descobrir endereços IP ativos
        print(blue + "\n>>> " + reset + "Finding addresses...\n")


def more_addresses():
    print()
    more_addresses = [
        {
            'type': 'list',
            'message': 'Do you want to specify another IPv4 address range?',
            'name': 'more',
            'choices': [{'name': 'Yes'}, {'name': 'No'}]
        }
    ]

    more_addresses_answer = prompt(more_addresses, style=style)
    if more_addresses_answer.get('more') == "Yes":
        return True
    else:
        return False


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


def basic_discovery():
    addresses = get_addresses()
    basic = ["nmap", "snmp"]
    #basic = ["snmp"]
    execution_queue.execute(basic, addresses)
    more = more_addresses()
    if more == True:
        basic_discovery()


def db_specification():
    """
    Asks the user to enter the necessary information (server address, port number and repository name) to access the database.

    Returns
    -------
    dict
        The database information (server address, port number and repository name).

    """
    db_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the IP address of the GraphDB server (use format yyx.yyx.yyx.yyx where \'y\' is optional):',
            'name': 'server',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter the port number where GraphDB is running:',
            'name': 'port',
            'validate': NumberValidator
        },
        {
            'type': 'input',
            'message': 'Enter the name of the GraphDB repository:',
            'name': 'repository',
            'validate': NotEmpty
        }
    ]

    db_specification_answer = prompt(db_specification_question, style=style)
    return db_specification_answer


def test_db_connection(server, port, repository):
    """
    Tests the access to the database.

    Parameters
    ----------
    server : string
        The IP address of the database server.

    port : string
        The port where the database is running.

    repository : string
        The name of the database repository.

    Returns
    -------
    boolean
        Returns true if the connection was successful and false otherwise.

    """
    global db_url
    db_url = "http://" + server + ":" + port + "/repositories/" + repository

    try:
        s = requests.Session()
        connection = s.get(db_url)
        unknown = regex.search(r'unknown repository',
                               connection.text, regex.IGNORECASE)
        if unknown != None:
            print(red + "\n>>> " + reset +
                  "Unknown repository. Please verify the connection information.\n")
            return False
        else:
            print(green + "\n>>> " + reset + "Successfully connected.\n")
            return True
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to GraphDB. Please verify the connection information.\n")
        return False


def get_db_info():
    db_info = db_specification()

    server = db_info.get("server")
    port = db_info.get("port")
    repository = db_info.get("repository")

    connection = test_db_connection(server, port, repository)
    if connection == False:
        get_db_info()
    else:
        return db_info


def run_discovery():
    open_message = pyfiglet.figlet_format(
        "Discovery Phase", font="small")
    print("**********************************************************************")
    print(open_message)
    print("**********************************************************************\n")

    vault_configuration()
    machine_password()

    basic_discovery()

    # categories = what2discover()

    ##########
    # TODO: mecanismos de descoberta
    ##########

    ##########
    print(blue + "\n>>> " + reset + "Make sure that GraphDB is running.\n")
    db_info = get_db_info()
    population.run_population(db_info)
    return db_info
