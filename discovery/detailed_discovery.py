# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from password_vault import vault
from discovery_mechanisms import os_x, windows, linux
from models import ConfigurationItem, methods
from similarity import similarity
from .discovery_info import discovery_info

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
    print()
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
            'name': 'password'
        }
    ]

    password_answer = prompt(password_question, style=style)
    pwd = password_answer["password"]
    return pwd


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
        Returns "mac" if the operating system family of the configuration item is Mac OS X, "windows" if it's Microsoft Windows and
        "linux" if it's Linux. 
    """
    # TODO: handle more operating systems
    ci_os = ci.get_os_family()

    mac = similarity.calculate_similarity(ci_os, "mac os x")
    windows = similarity.calculate_similarity(ci_os, "windows")
    linux = similarity.calculate_similarity(ci_os, "linux")

    if mac > windows and mac > linux:
        return "mac"
    elif windows > mac and windows > linux:
        return "windows"
    elif linux > mac and linux > windows:
        return "linux"


def detailed_discovery(categories):
    """
    Executes the detailed discovery of the machine.
    Explores OS X, Windows and Linux devices.

    Parameters
    --------
    categories : list
        The list of categories selected by the user to explore.
    """
    unlock_vault()

    for ip in discovery_info.get("ip_addresses"):
        names = vault.get_names()
        if ip not in names:
            user = ask_username(ip)
            pwd = ask_password(ip)
            vault.add_secret(ip, user, pwd)

    for ip in discovery_info.get("ip_addresses"):
        if ip not in discovery_info.get("visited_addresses"):
            discovery_info["visited_addresses"].append(ip)

            user = vault.show_username_by_name(ip)
            pwd = vault.show_secret_by_name(ip)

            new_ci = ConfigurationItem.ConfigurationItem()
            new_ci.add_ipv4_address(ip)
            ci = methods.ci_already_exists(new_ci)
            if ci == None:
                ci = new_ci

            ci_os = check_os(ci)

            if ci_os == "mac":
                print(blue + ">>> " + reset +
                      "Discovery in the OS X machine with the address " + str(ip) + "...\n")
                os_x.run_os_x_discovery(ci, user, pwd, ip, categories)

            elif ci_os == "windows":
                print(blue + ">>> " + reset +
                      "Discovery in the Windows machine with the address " + str(ip) + "...\n")
                windows.run_windows_discovery(ci, user, pwd, ip, categories)

            elif ci_os == "linux":
                print(blue + ">>> " + reset +
                      "Discovery in the Linux machine with the address " + str(ip) + "...\n")
                linux.run_linux_discovery(ci, user, pwd, ip, categories)

            methods.add_ci(ci)
