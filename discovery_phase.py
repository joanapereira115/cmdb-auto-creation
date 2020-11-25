# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import regex
import pyfiglet
from netaddr import IPNetwork

from password_vault import vault
from db_population import population
from discovery import basic_discovery, detailed_discovery, discovery_info

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
orange = fg('#e76f51')
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
                cursor_position=len(document.text))


class AddressesValidator(Validator):
    def validate(self, document):
        add = regex.match(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', document.text)
        rng = regex.match(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}', document.text)
        cidr = regex.match(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}', document.text)
        if cidr != None:
            s = regex.search(
                r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\/(\d{1,2})', document.text)
            groups = s.groups()
            if int(groups[0]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[1]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[2]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[3]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[4]) > 32:
                raise ValidationError(
                    message='Please enter a valid IPv4 CIDR notation.',
                    cursor_position=len(document.text))
        elif rng != None:
            s = regex.search(
                r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})-(\d{1,3})', document.text)
            groups = s.groups()
            if int(groups[0]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[1]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[2]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[3]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[3]) > int(groups[4]):
                raise ValidationError(
                    message='Please enter a valid IPv4 address range.',
                    cursor_position=len(document.text))
            if int(groups[4]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
        elif add != None:
            s = regex.search(
                r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})', document.text)
            groups = s.groups()
            if int(groups[0]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[1]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[2]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
            if int(groups[3]) > 255:
                raise ValidationError(
                    message='Please enter a valid IPv4 address.',
                    cursor_position=len(document.text))
        else:
            raise ValidationError(
                message='Please enter a valid IPv4 address range.',
                cursor_position=len(document.text))


def handle_range(addresses):
    """
    Processes the possible IPv4 addresses from ranges, CIDR notation, or addresses defined by the user.

    Parameters
    ----------
    addresses : string
        The text that represents an IPv4 range, a CIDR, or an address.

    Returns
    -------
    list
        Returns the possible IPv4 addresses.
    """
    ips = []

    add = regex.match(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', addresses)
    rng = regex.match(
        r'(\d{1,3}\.\d{1,3}\.\d{1,3})\.(\d{1,3})-(\d{1,3})', addresses)
    cidr = regex.match(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}', addresses)

    if cidr != None:
        for ip in IPNetwork(addresses):
            ips.append(str(ip))
    elif rng != None:
        groups = rng.groups()
        beg = int(groups[1])
        end = int(groups[2]) + 1
        for i in range(beg, end):
            ips.append(str(groups[0])+"."+str(i))
    elif add != None:
        ips.append(str(addresses))

    return ips


def more_addresses():
    """
    Asks the user if he wants to define more addresses to discover.

    Returns
    -------
    boolean
        Returns true if the user wants to define more addresses, and false if not.
    """
    print()
    more_addresses = [
        {
            'type': 'list',
            'message': 'Do you want to specify another IPv4 address or range?',
            'name': 'more',
            'choices': [{'name': 'Yes'}, {'name': 'No'}]
        }
    ]

    more_addresses_answer = prompt(more_addresses, style=style)
    if more_addresses_answer.get('more') == "Yes":
        return True
    else:
        return False


def get_addresses():
    """
    Asks the user for the addresses to discover.
    """
    range_question = [
        {
            'type': 'input',
            'name': 'addresses',
            'message': 'Enter the IPv4 address (yyx.yyx.yyx.yyx, where \'yy\' is optional), IPv4 range (yyx.yyx.yyx.yyx-zzz, where \'yy\' and \'-zzz\' are optional) or CIDR (yyx.yyx.yyx.yyx/yx, where \'y\' is optional) you want to discover.',
            'validate': AddressesValidator
        }
    ]
    range_answer = prompt(range_question, style=style)
    addresses = range_answer["addresses"]
    ips = handle_range(addresses)
    for ip in ips:
        discovery_info.add_ip(ip)
    more = more_addresses()
    if more == True:
        get_addresses()


def what2discover():
    """
    Asks the user which IT categories he wants to have a more detailed discovery.

    Returns
    -------
    list
        Returns the list of categories selected by the user.
    """
    print()
    categories_questions = [
        {
            'type': 'checkbox',
            'message': 'In which IT infrastructure categories would you want to make a more detailed discovery?',
            'name': 'categories',
            'choices': [
                {'name': 'Network - collects information about the network connections of the machine',
                    'value': 'network', 'short': 'Network'},

                {'name': 'Devices - gathers data about the devices directly connected or attached to the machine', 'value': 'devices',
                    'short': 'Devices'},

                {'name': 'Operating Systems - collects information about the operating system executing on the machine', 'value': 'operating systems',
                    'short': 'Operating Systems'},

                {'name': 'Processing - gathers data about different types of processors present on the machine',
                    'value': 'processing', 'short': 'Processing'},

                {'name': 'Storage - collects information about the storage systems of the machine',
                    'value': 'storage', 'short': 'Storage'},

                {'name': 'Software - gathers data about the software products installed on the machine',
                    'value': 'software', 'short': 'Software'},

                {'name': 'Hardware - collects information about the hardware specifications of the machine',
                    'value': 'hardware', 'short': 'Hardware'},

                {'name': 'Virtual Machines - gathers information about virtual machine instances executing in the machine', 'value': 'virtual machines',
                    'short': 'Virtual Machines'},

                {'name': 'Databases - gathers information about the database management systems executing in the machine and the database instances associated with them',
                    'value': 'databases', 'short': 'Databases'},

                {'name': 'Services - collects data about the services executing in the machine',
                    'value': 'services', 'short': 'Services'},

                {'name': 'Containers - gathers information about container instances executing in the machine',
                    'value': 'containers', 'short': 'Containers'},

                {'name': 'Cloud Systems - collects information about cloud systems executing in the machine', 'value': 'cloud systems',
                    'short': 'Cloud Systems'},

                {'name': 'Location - gathers data about the geographical location of the machine', 'value': 'location',
                    'short': 'Location'},

                {'name': 'People - collects information about users',
                    'value': 'people', 'short': 'People'},

                {'name': 'Documents - collects data about the existing documents in the machine',
                    'value': 'documents', 'short': 'Documents'}

            ],
            'validate': lambda answer: len(answer) > 0 or 'You must choose at least one category.'
        }
    ]

    categories_answer = prompt(categories_questions, style=style)

    categories = categories_answer.get("categories")
    return categories


def import_data():
    """
    Asks the user if he imported the file into his GraphDB repository.
    """
    print(orange + "\n>>> " + reset +
          "Make sure that GraphDB is running and that you import the discovered information.")
    import_question = [
        {
            'type': 'confirm',
            'name': 'import',
            'message': "Have you imported the file 'cmdb.ttl' stored in the folder 'graphdb-import' to your GraphDB repository?\n"
        }]
    import_answer = prompt(import_question, style=style).get("import")
    if import_answer == False:
        import_data()


def run_discovery():
    """
    Executes the discovery of the machines and the population of the database with that info. 
    """
    open_message = pyfiglet.figlet_format(
        "Discovery Phase", font="small")
    print()
    print(
        "\033[1m**********************************************************************\033[0m")
    print(open_message)
    print(
        "\033[1m**********************************************************************\033[0m\n")

    get_addresses()
    basic_discovery.basic_discovery()
    categories = what2discover()
    detailed_discovery.detailed_discovery(categories)
    population.run_population()

    import_data()
