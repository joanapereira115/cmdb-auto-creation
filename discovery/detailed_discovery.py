# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from password_vault import vault
from discovery_mechanisms import os_x
from discovery_mechanisms import windows
from models import ConfigurationItem, methods
from similarity import similarity
from normalization import normalization

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
                cursor_position=len(document.text))


def unlock_vault():
    """
    Asks the user for the password of the vault to unlock it.
    """
    vault.initialize()
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


def ask_username(ip):
    """
    Asks the user for the username to login into the machine with the given IP.

    Parameters
    ----------
    ip : string
        The IPv4 address.

    Returns
    -------
    string
        Returns the username specified for the user.
    """
    username_question = [
        {
            'type': 'input',
            'message': 'Enter the username of the machine with yhe IP address ' + ip + ':',
            'name': 'username',
            'validate': NotEmpty
        }
    ]

    username_answer = prompt(username_question, style=style)
    user = username_answer["username"]
    return user


def ask_password(ip):
    """
    Asks the user for the password to login into the machine with the given IP.

    Parameters
    ----------
    ip : string
        The IPv4 address.

    Returns
    -------
    string
        Returns the password specified for the user.
    """
    password_question = [
        {
            'type': 'password',
            'message': 'Enter the password of the machine with yhe IP address ' + ip + ':',
            'name': 'password',
            'validate': NotEmpty
        }
    ]

    password_answer = prompt(password_question, style=style)
    pwd = password_answer["password"]
    return pwd


def external_data():
    """
    Asks the user if he wants to import information from an external application/source.

    Returns
    -------
    boolean
        Returns true if the user wants to use an external source, and false if not.
    """
    external_data = [
        {
            'type': 'list',
            'message': 'Do you want to import information from an external application/source?',
            'name': 'external',
            'choices': [{'name': 'Yes'}, {'name': 'No'}]
        }
    ]

    external_data_answer = prompt(external_data, style=style)
    if external_data_answer.get('external') == "Yes":
        return True
    else:
        return False


def check_os(ci):
    """
    Checks the operating system family of a configuration item.

    Parameters
    ----------
    ci : ConfigurationItem
        The configuration item.

    Returns
    -------
    string
        Returns "mac" if the operating system family of the configuration item is Mac OS X and "windows" if it's Microsoft Windows.
    """
    # TODO: handle more operating systems
    ci_os = ci.get_os_family()

    mac = similarity.calculate_similarity(ci_os, "mac os x")
    windows = similarity.calculate_similarity(ci_os, "windows")

    if mac > windows:
        return "mac"
    elif windows > mac:
        return "windows"


def detailed_discovery(available_ips, categories):
    external = external_data()
    if external == True:
        # TODO: handle external app
        pass
    else:
        # TODO: tirar
        print()
        print("available_ips: " + str(available_ips))
        print("categories: " + str(categories))
        print()
        unlock_vault()
        for ip in available_ips:
            names = vault.get_names()
            if ip not in names:
                user = ask_username(ip)
                pwd = ask_password(ip)
                vault.add_secret(ip, user, pwd)
            else:
                user = vault.show_login_by_name(ip)[0]
                pwd = vault.show_secret_by_name(ip)[0]

            ci = ConfigurationItem.ConfigurationItem()
            ci.add_ipv4_address(ip)
            new_ci = methods.ci_already_exists(ci)
            if new_ci == None:
                new_ci = ci

            ci_os = check_os(new_ci)
            if ci_os == "mac":
                print(blue + ">>> " + reset +
                      "Discovery in the OS X machine with the address " + str(ip) + "...\n")
                os_disc = os_x.run_os_x_discovery(
                    new_ci, user, pwd, ip, categories)
                if os_disc == False:
                    pass
                    # TODO: credenciais erradas ou o OS estava errado?
            elif ci_os == "windows":
                print(blue + ">>> " + reset +
                      "Discovery in the Windows machine with the address " + str(ip) + "...\n")
                win_disc = windows.run_windows_discovery(
                    new_ci, user, pwd, ip, categories)
                if win_disc == False:
                    pass
                    # TODO: credenciais erradas ou o OS estava errado?

            methods.add_ci(new_ci)
