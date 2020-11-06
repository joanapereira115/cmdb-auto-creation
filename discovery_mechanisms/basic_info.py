# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex
import nmap
import sys
import os
from pprint import pprint
from colored import fg, bg, attr
from elevate import elevate
import getpass
import subprocess
import xml.etree.ElementTree as ET
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import json
import paramiko

from password_vault import vault
from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from normalization import normalization
from similarity import similarity
from .os_x import run_os_x_discovery
from .windows import run_windows_discovery

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


def unlock_vault():
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

##############################


def windows_discovery(user, pwd, ip, categories):
    print("windows discovery\n")


def linux_discovery(user, pwd, ip, categories):
    print("linux discovery\n")
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ok = True
    try:
        client.connect(ip, 22, user, pwd)
    except:
        print(red + ">>> " + reset +
              "Unable to connect with the machine " + ip + " via SSH.\n")
        ok = False
    """


def run_basic_info(available_ips, categories):
    print("available_ips: " + str(available_ips))
    print("categories: " + str(categories))
    print()
    unlock_vault()
    for ip in available_ips:
        print(blue + ">>> " + reset +
              "Discovery in the address " + str(ip) + "...\n")

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
        m = 0
        val = ""
        for at in new_ci.get_attributes():
            title = methods.get_attribute_title_from_id(at)
            sim = similarity.calculate_similarity(title, "operating system")
            if sim > m:
                m = sim
                val = methods.get_attribute_value_from_id(at)
        mac = similarity.calculate_similarity(val, "mac os x")
        linux = similarity.calculate_similarity(val, "linux")
        windows = similarity.calculate_similarity(val, "windows")
        if mac > linux and mac > windows:
            run_os_x_discovery(new_ci, user, pwd, ip, categories)
        if linux > mac and linux > windows:
            linux_discovery(user, pwd, ip, categories)
        if windows > mac and windows > linux:
            run_windows_discovery(new_ci, user, pwd, ip, categories)
