#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from unit_converter.converter import convert, converts
from nltk.corpus import wordnet as wn
import regex
from pprint import pprint
from colored import fg, bg, attr
from django.apps import apps
#from .models import *

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

acronyms_db = {
    'OS': 'operating_system',
    'IP': 'internet_protocol',
    'MAC': 'media_access_control',
    'TCP': 'transmission_control_protocol',
    'ITIL': 'information technology infrastructure library',
    'CMDB': 'configuration management database',
    'CI': 'configuration item',
    'ISO': 'international organization for standardization',
    'ICMP': 'internet control message protocol',
    'SNMP': 'simple network management protocol',
    'LAN': 'local area network',
    'WAN': 'wide area netwok',
    'VPN': 'virtual private network',
    'FDB': 'forwarding database',
    'ARP': 'address resolution protocol',
    'LLDP': 'link layer discovery protocol',
    'MIB': 'management information base',
    'UDP': 'user datagram protocol',
    'STP': 'spanning tree protocol',
    'SPAN': 'switched port analyzer',
    'RDP': 'remote desktop protocol',
    'API': 'application programming interface',
    'REST': 'representational state transfer',
    'TI': 'tecnologias da informação',
    'ITSM': 'it service management',
    'OSI': 'open system interconnection',
    'SSH': 'secure_shell',
    'WMI': 'windows management instrumentation',
    'WinRM': 'windows remote management',
    'CDP': 'cisco discovery protocol',
    'JMX': 'java management extensions',
    'SQL': 'structured query language',
    'DNS': 'domain name system',
    'NFS': 'network file system',
    'LDAP': 'lightweight directory access protocol',
    'TADDM': 'tivoli application dependency discovery manager',
    'SSD': 'solid-state drive',
    'DAS': 'direct attached storage',
    'NAS': 'network attached storage',
    'SAN': 'storage area network',
    'CPU': 'central processing unit',
    'BIOS': 'basic input/output system',
    'JSON': 'javascript object notation',
    'HTTP': 'hypertext_transfer_protocol',
    'HTTPS': 'hypertext transfer protocol secure',
    'XML': 'extensible markup language',
    'CIM': 'common information model',
    'SVS': 'service value system',
    'DMTF': 'distributed management task force',
    'UML': 'unified modeling language',
    'RPC': 'remote procedure call',
    'CMS': 'configuration management system',
    'CIDR': 'classless inter-domain routing',
    'TTL': 'time to live',
    'CSV': 'comma-separated values',
    'PHP': 'hypertext preprocessor',
    'XDP': 'express data path',
    'FDP': 'foundry discovery protocol',
    'OSPF': 'open shortest path first',
    'BGP': 'border gateway protocol',
    'NDP': 'neighbor discovery protocol',
    'UPS': 'uninterruptible power source',
    'MAN': 'metropolitan area network',
    'BAN': 'body area network',
    'PAN': 'personal area network',
    'AP': 'access point',
    'HDD': 'hard disk drive',
    'SGBD': 'sistemas de gestão de base de dados',
    'BD': 'bases de dados',
    'HTML': 'hypertext markup language',
    'URL': 'uniform resource locator',
    'SSL': 'secure sockets layer',
    'VLAN': 'virtual local area network',
    'UCS': 'unified computing system',
    'ACI': 'application centric infrastructure',
    'SDN': 'software defined network',
    'IPMI': 'intelligent platform management interface',
    'BMC': 'baseboard management controller',
    'SCCM': 'system center configuration manager',
    'FTP': 'file transfer protocol',
    'UUID': 'universally unique identifier',
    'CDM': 'common data model',
    'TPL': 'template file',
    'IS-IS': 'intermediate system-intermediate system',
    'RIP': 'routing information protocol'
}

"""
synonyms_db = {
    'up': ['normal', 'running', 'on', 'power on', 'operating'],
    'port': ['communication endpoint']
}
"""


def notations(word):
    # check for snake_case
    word = re.sub(r"_", " ", word, re.DOTALL)
    # check for kebab-case
    word = re.sub(r"-", " ", word, re.DOTALL)
    # check for camelCase and PascalCase
    word = re.sub(r"([a-z])([A-Z])", r"\1 \2", word, re.DOTALL)
    # separate numbers from units
    word = re.sub(r"([0-9]+\.?|,?[0-9]+?)([a-zA-Z]+)[^:]",
                  r"\1 \2", word, re.DOTALL)
    # trim spaces at the begin and end
    word = re.sub(r"^\s+", "", word)
    # trim multiple spaces
    word = re.sub(r"\s+", " ", word)
    return word


def acronyms(word):
    acs = list(acronyms_db.keys())
    for a in acs:
        exists = re.search(r'(^|\s)' + a + r'($|\s)', word, re.I)
        if exists != None:
            word = re.sub(r'(^|\s)' + a + r'($|\s)',
                          r'\1' + acronyms_db[a] + r'\2', word, flags=re.I)
    return word


"""
def synonyms(word):
    return synonyms_db[word.lower()]
"""


def unit_formatter(txt):
    # TODO: adicionar as restantes unidades
    # TODO: verificar a existência de valores na notação E (elevado a 10)

    # time units replacement
    txt = re.sub("yoctosecond(s)?", "ys", txt)
    txt = re.sub("zeptosecond(s)?", "zs", txt)
    txt = re.sub("attosecond(s)?", "as", txt)
    txt = re.sub("femtosecond(s)?", "fs", txt)
    txt = re.sub("picosecond(s)?", "ps", txt)
    txt = re.sub("nanosecond(s)?", "ns", txt)
    txt = re.sub("microsecond(s)?", "µs", txt)
    txt = re.sub("millisecond(s)?", "ms", txt)
    txt = re.sub("second(s)?", "s", txt)
    txt = re.sub("minute(s)?", "min", txt)
    txt = re.sub("hour(s)?", "h", txt)
    # measurement units replacement
    txt = re.sub("yoctometer(s)?", "ym", txt)
    txt = re.sub("zeptometer(s)?", "zm", txt)
    txt = re.sub("attometer(s)?", "am", txt)
    txt = re.sub("femtometer(s)?", "fm", txt)
    txt = re.sub("picometer(s)?", "pm", txt)
    txt = re.sub("nanometer(s)?", "nm", txt)
    txt = re.sub("micrometer(s)?", "µm", txt)
    txt = re.sub("millimeter(s)?", "mm", txt)
    txt = re.sub("centimeter(s)?", "cm", txt)
    txt = re.sub("decimeter(s)?", "dm", txt)
    txt = re.sub("decameter(s)?", "dam", txt)
    txt = re.sub("hectometer(s)?", "hm", txt)
    txt = re.sub("kilometer(s)?", "km", txt)
    txt = re.sub("megameter(s)?", "Mm", txt)
    txt = re.sub("gigameter(s)?", "Gm", txt)
    txt = re.sub("terameter(s)?", "Tm", txt)
    txt = re.sub("petameter(s)?", "Pm", txt)
    txt = re.sub("exameter(s)?", "Em", txt)
    txt = re.sub("zettameter(s)?", "Zm", txt)
    txt = re.sub("yottameter(s)?", "Ym", txt)
    txt = re.sub(" th$", "thou", txt)
    txt = re.sub(" in$", "inch", txt)
    txt = re.sub(" ft$", "foot", txt)
    txt = re.sub(" yd$", "yard", txt)
    txt = re.sub(" ch$", "chain", txt)
    txt = re.sub(" fur$", "furlong", txt)
    txt = re.sub(" ml$", "mile", txt)
    txt = re.sub(" lea$", "league", txt)
    txt = re.sub("meter(s)?", "m", txt)
    # mass units replacement
    txt = re.sub("yoctogram(s)?", "yg", txt)
    txt = re.sub("zeptogram(s)?", "zg", txt)
    txt = re.sub("attogram(s)?", "ag", txt)
    txt = re.sub("femtogram(s)?", "fg", txt)
    txt = re.sub("picogram(s)?", "pg", txt)
    txt = re.sub("nanogram(s)?", "ng", txt)
    txt = re.sub("microgram(s)?", "µg", txt)
    txt = re.sub("milligram(s)?", "mg", txt)
    txt = re.sub("centigram(s)?", "cg", txt)
    txt = re.sub("decigram(s)?", "dg", txt)
    txt = re.sub("decagram(s)?", "dag", txt)
    txt = re.sub("hectogram(s)?", "hg", txt)
    txt = re.sub("kilogram(s)?", "kg", txt)
    txt = re.sub("megagram(s)?", "Mg", txt)
    txt = re.sub("gigagram(s)?", "Gg", txt)
    txt = re.sub("teragram(s)?", "Tg", txt)
    txt = re.sub("petagram(s)?", "Pg", txt)
    txt = re.sub("exagram(s)?", "Eg", txt)
    txt = re.sub("zettagram(s)?", "Zg", txt)
    txt = re.sub("yottagram(s)?", "Yg", txt)
    txt = re.sub("gram(s)?", "g", txt)
    # speed units replacement
    txt = re.sub("yoctohertz(s)?", "yHz", txt)
    txt = re.sub("zeptohertz(s)?", "zHz", txt)
    txt = re.sub("attohertz(s)?", "aHz", txt)
    txt = re.sub("femtohertz(s)?", "fHz", txt)
    txt = re.sub("picohertz(s)?", "pHz", txt)
    txt = re.sub("nanohertz(s)?", "nHz", txt)
    txt = re.sub("microhertz(s)?", "µHz", txt)
    txt = re.sub("millihertz(s)?", "mHz", txt)
    txt = re.sub("centihertz(s)?", "cHz", txt)
    txt = re.sub("decihertz(s)?", "dHz", txt)
    txt = re.sub("decahertz(s)?", "daHz", txt)
    txt = re.sub("hectohertz(s)?", "hHz", txt)
    txt = re.sub("kilohertz(s)?", "kHz", txt)
    txt = re.sub("megahertz(s)?", "MHz", txt)
    txt = re.sub("gigahertz(s)?", "GHz", txt)
    txt = re.sub("terahertz(s)?", "THz", txt)
    txt = re.sub("petahertz(s)?", "PHz", txt)
    txt = re.sub("exahertz(s)?", "EHz", txt)
    txt = re.sub("zettahertz(s)?", "ZHz", txt)
    txt = re.sub("yottahertz(s)?", "YHz", txt)
    txt = re.sub("hertz(s)?", "Hz", txt)
    # thermodynamic temperature units replacement
    txt = re.sub("kelvin(s)?", "K", txt)
    txt = re.sub("celsius(s)?", "°C", txt)
    txt = re.sub("fahrenheit(s)?", "°F", txt)
    # other units replacement
    txt = re.sub("milliampere(s)?", "mA", txt)
    txt = re.sub("centiampere(s)?", "cA", txt)
    txt = re.sub("deciampere(s)?", "dA", txt)
    txt = re.sub("decampere(s)?", "daA", txt)
    txt = re.sub("hectoampere(s)?", "hA", txt)
    txt = re.sub("kiloampere(s)?", "kA", txt)
    txt = re.sub("megampere(s)?", "MA", txt)
    txt = re.sub("gigampere(s)?", "GA", txt)
    txt = re.sub("ampere(s)?", "A", txt)

    txt = re.sub(" us$", " µs", txt)

    return txt


def convert_time_func(matchobj):
    m = matchobj.group(0)
    return str(converts(m, 's')) + ' s'


def convert_speed_func(matchobj):
    m = matchobj.group(0)
    return str(converts(m, 'Hz')) + ' Hz'


def conversion(txt):
    # TODO: mudar as outras unidades

    measurement = re.search(r"[0-9]+(.|,[0-9]+)?( )?ym", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?zm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?am", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?fm", txt) or re.search("pm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?nm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?µm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?mm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?cm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?dm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?m", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?dam", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?hm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?km", txt) or re.search(
        r"[0-9]+(.|,[0-9]+)?( )?Mm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Gm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Tm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Pm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Em", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Zm", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?Ym", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?thou", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?inch", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?foot", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?yard", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?chain", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?furlong", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?mile", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?league", txt)

    temperature = re.search(r"[0-9]+(.|,[0-9]+)?( )?K", txt) or re.search(
        r"[0-9]+(.|,[0-9]+)?( )?°C", txt) or re.search(r"[0-9]+(.|,[0-9]+)?( )?°F", txt)

    txt = re.sub(r"[0-9]+(\.|,[0-9]+)?( )?(min|s|h|ms|µs|ns|ps)",
                 convert_time_func, txt)

    txt = re.sub(r"[0-9]+(\.|,[0-9]+)?( )?(yHz|zHz|aHz|fHz|pHz|nHz|µHz|mHz|cHz|dHz|Hz|daHz|hHz|kHz|MHz|GHz|THz|PHz|EHz|ZHz|YHz)",
                 convert_speed_func, txt)
    """
    elif measurement != None:
        return str(converts(txt, 'm')) + ' m'

    elif temperature != None:
        return str(converts(txt, 'K')) + ' K'
    """
    return txt


def normalize(data):
    # print(blue + ">>> " + reset + "Normalizing data...")
    #print(blue + "\t>>> " + reset + "Before: " + str(data))
    data = notations(data)
    data = acronyms(data)
    data = unit_formatter(data)
    data = conversion(data)
    #data = synonyms(data)
    #data = conversion(data)
    #print(blue + "\t>>> " + reset + "After: " + str(data))
    return data


# normalize(' ola   20minutes  3,3 megahertz  tcp_ciencia ci      ')

"""
def get_tables_names():
    print(blue + ">>> " + reset +
          "Finding models...")
    # TODO: automatizar isto
    res = ['managed_system_element', 'port',
           'operating_system', 'computer_system', 'installed_os', 'running_os', 'has_port']
    return res


def get_table_attributes(table):
    print(blue + ">>> " + reset +
          "Finding attributes...")
    # TODO: automatizar isto
    tables = {
        'managed_system_element': ['install_date', 'name', 'status', 'health_state', 'communication_status', 'detailed_status', 'operating_status', 'primary_status', 'instance_id', 'caption', 'description', 'element_name', 'generation'],
        'port': ['number', 'protocol', 'state', 'cpe', 'name', 'product', 'version', 'description'],
        'operating_system': ['cs_creation_class_name', 'cs_name', 'creation_class_name', 'name', 'os_type', 'other_type_description', 'version', 'last_boot_up_time', 'local_date_time', 'current_time_zone', 'number_of_licensed_users', 'number_of_users', 'number_of_processes', 'max_number_of_processes', 'total_swap_space_size', 'total_virtual_memory_size', 'free_virtual_memory', 'free_physical_memory', 'total_visible_memory_size', 'size_stored_in_paging_files', 'free_space_in_paging_files', 'max_process_memory_size', 'distributed', 'max_processes_per_user', 'enabled_state', 'other_enabled_state', 'requested_state', 'enabled_default', 'time_of_last_state_change', 'transitioning_to_state', 'install_date', 'status', 'health_state', 'communication_status', 'detailed_status', 'operating_status', 'primary_status', 'instance_id', 'caption', 'description', 'element_name', 'generation'],
        'computer_system': ['name_format', 'reset_capability', 'creation_class_name', 'name', 'primary_owner_name', 'primary_owner_contact', 'allocation_state', 'enabled_state', 'other_enabled_state', 'requested_state', 'enabled_default', 'time_of_last_state_change', 'transitioning_to_state', 'install_date', 'status', 'health_state', 'communication_status', 'detailed_status', 'operating_status', 'primary_status', 'instance_id', 'caption', 'description', 'element_name', 'generation'],
        'installed_os': ['computer_system_id', 'operating_system_id', 'primary_os'],
        'running_os': ['operating_system_id', 'computer_system_id'],
        'has_port': ['computer_system_id', 'port_id']
    }
    return tables[table]
"""


"""
Other Units

'mol': Unit('mol', 'mole', N=1),
'cd': Unit('cd', 'candela', J=1),
'N': Unit('N', 'newton', M=1, L=1, T=-2),
'Pa': Unit('Pa', 'pascal', M=1, L=-1, T=-2),
'J': Unit('J', 'joule', M=1, L=2, T=-2),
'W': Unit('W', 'watt', M=1, L=2, T=-3),
'C': Unit('C', 'coulomb', T=1, I=1),
'V': Unit('V', 'volt', M=1, L=2, T=-3, I=-1),
'Ω': Unit('Ω', 'ohm', M=1, L=2, T=-3, I=-2),
'S': Unit('S', 'siemens', M=-1, L=-2, T=3, I=2),
'F': Unit('F', 'farad', M=-1, L=-2, T=4, I=2),
'T': Unit('T', 'tesla', M=1, T=-2, I=-1),
'Wb': Unit('Wb', 'weber', M=1, L=2, T=-2, I=-1),
'H': Unit('H', 'henry', M=1, L=2, T=-2, I=-2),
'rad': Unit('rad', 'radian'),
'sr': Unit('sr', 'steradian'),
'bar': Unit('bar', 'bar', M=1, L=-1, T=-2, coef=D('1E5')),
"""
