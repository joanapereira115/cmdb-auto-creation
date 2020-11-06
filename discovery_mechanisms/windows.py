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
import requests
import winrm

from password_vault import vault
from models import Attribute, ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods, objects
from normalization import normalization
from similarity import similarity
from .windows_discovery import operating_system
# , processing, location, storage, software, hardware, network

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


def run_windows_discovery(ci, user, pwd, ip, categories):
    print("windows discovery\n")

    ok = True
    try:
        s = winrm.Session(ip, auth=(user, pwd))
    except:
        print(red + ">>> " + reset +
              "Unable to connect with the machine " + ip + " via WinRM.\n")
        ok = False
    if ok == True:
        r = s.run_cmd("hostname", [])
        hostname = r.std_out.decode("ISO-8859-1").strip("\n")
        methods.define_attribute("hostname", hostname, ci)

        r = s.run_cmd("wmic bios get serialnumber", [])
        serial = r.std_out.decode(
            "ISO-8859-1").split("\n")[1].strip("\n").strip(" "). strip("\r")
        methods.define_attribute("serial number", serial, ci)

        if 'operating systems' in categories:
            operating_system.os_discovery(s, ci)

        """ 
        if 'processing' in categories:
            processing.processing_discovery(client, ci)
        if 'location' in categories:
            location.location_discovery(client, ci)
        if 'storage' in categories:
            storage.storage_discovery(client, ci)
        if 'software' in categories:
            software.sw_discovery(client, ci)
        if 'hardware' in categories:
            hardware.hw_discovery(client, ci)
        if 'network' in categories:
            network.network_discovery(client, ci)
        if 'end user devices' in categories:
            devices_discovery(client, ci)
        if 'virtual machines' in categories:
            vm_discovery(client, ci)
        if 'databases' in categories:
            db_discovery(client, ci)
        if 'services' in categories:
            services_discovery(client, ci)
        if 'containers' in categories:
            containers_discovery(client, ci)
        if 'cloud systems' in categories:
            cloud_discovery(client, ci)
        if 'documents' in categories:
            doc_discovery(client, ci)
        if 'people' in categories:
            people_discovery(client, ci)
        
        """
