#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from unit_converter.converter import convert, converts
from nltk.corpus import wordnet as wn
import regex
from pprint import pprint
from colored import fg, bg, attr
import lexical_db
from django.apps import apps
#from .models import *

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

acronyms_db = {
    'OS': 'operating_system',
    'IP': 'internet_protocol',
    'MAC': 'media_access_control'}

synonyms_db = {
    'up': ['normal', 'running', 'on', 'power on', 'operating']
}


def acronyms(word):
    return acronyms_db[word.upper()]


def synonyms(word):
    return synonyms_db[word.lower()]


def conversion(txt):
    # time units replacement
    re.sub("yoctosecond(s)?", "ys", txt)
    re.sub("zeptosecond(s)?", "zs", txt)
    re.sub("attosecond(s)?", "as", txt)
    re.sub("femtosecond(s)?", "fs", txt)
    re.sub("picosecond(s)?", "ps", txt)
    re.sub("nanosecond(s)?", "ns", txt)
    re.sub("microsecond(s)?", "µs", txt)
    re.sub("millisecond(s)?", "ms", txt)
    re.sub("second(s)?", "s", txt)
    re.sub("minute(s)?", "min", txt)
    re.sub("hour(s)?", "h", txt)
    # measurement units replacement
    re.sub("yoctometer(s)?", "ym", txt)
    re.sub("zeptometer(s)?", "zm", txt)
    re.sub("attometer(s)?", "am", txt)
    re.sub("femtometer(s)?", "fm", txt)
    re.sub("picometer(s)?", "pm", txt)
    re.sub("nanometer(s)?", "nm", txt)
    re.sub("micrometer(s)?", "µm", txt)
    re.sub("millimeter(s)?", "mm", txt)
    re.sub("centimeter(s)?", "cm", txt)
    re.sub("decimeter(s)?", "dm", txt)
    re.sub("meter(s)?", "m", txt)
    re.sub("decameter(s)?", "dam", txt)
    re.sub("hectometer(s)?", "hm", txt)
    re.sub("kilometer(s)?", "km", txt)
    re.sub("megameter(s)?", "Mm", txt)
    re.sub("gigameter(s)?", "Gm", txt)
    re.sub("terameter(s)?", "Tm", txt)
    re.sub("petameter(s)?", "Pm", txt)
    re.sub("exameter(s)?", "Em", txt)
    re.sub("zettameter(s)?", "Zm", txt)
    re.sub("yottameter(s)?", "Ym", txt)
    re.sub(" th$", "thou", txt)
    re.sub(" in$", "inch", txt)
    re.sub(" ft$", "foot", txt)
    re.sub(" yd$", "yard", txt)
    re.sub(" ch$", "chain", txt)
    re.sub(" fur$", "furlong", txt)
    re.sub(" ml$", "mile", txt)
    re.sub(" lea$", "league", txt)
    # mass units replacement
    re.sub("yoctogram(s)?", "yg", txt)
    re.sub("zeptogram(s)?", "zg", txt)
    re.sub("attogram(s)?", "ag", txt)
    re.sub("femtogram(s)?", "fg", txt)
    re.sub("picogram(s)?", "pg", txt)
    re.sub("nanogram(s)?", "ng", txt)
    re.sub("microgram(s)?", "µg", txt)
    re.sub("milligram(s)?", "mg", txt)
    re.sub("centigram(s)?", "cg", txt)
    re.sub("decigram(s)?", "dg", txt)
    re.sub("gram(s)?", "g", txt)
    re.sub("decagram(s)?", "dag", txt)
    re.sub("hectogram(s)?", "hg", txt)
    re.sub("kilogram(s)?", "kg", txt)
    re.sub("megagram(s)?", "Mg", txt)
    re.sub("gigagram(s)?", "Gg", txt)
    re.sub("teragram(s)?", "Tg", txt)
    re.sub("petagram(s)?", "Pg", txt)
    re.sub("exagram(s)?", "Eg", txt)
    re.sub("zettagram(s)?", "Zg", txt)
    re.sub("yottagram(s)?", "Yg", txt)
    # speed units replacement
    re.sub("yoctohertz(s)?", "yHz", txt)
    re.sub("zeptohertz(s)?", "zHz", txt)
    re.sub("attohertz(s)?", "aHz", txt)
    re.sub("femtohertz(s)?", "fHz", txt)
    re.sub("picohertz(s)?", "pHz", txt)
    re.sub("nanohertz(s)?", "nHz", txt)
    re.sub("microhertz(s)?", "µHz", txt)
    re.sub("millihertz(s)?", "mHz", txt)
    re.sub("centihertz(s)?", "cHz", txt)
    re.sub("decihertz(s)?", "dHz", txt)
    re.sub("hertz(s)?", "Hz", txt)
    re.sub("decahertz(s)?", "daHz", txt)
    re.sub("hectohertz(s)?", "hHz", txt)
    re.sub("kilohertz(s)?", "kHz", txt)
    re.sub("megahertz(s)?", "MHz", txt)
    re.sub("gigahertz(s)?", "GHz", txt)
    re.sub("terahertz(s)?", "THz", txt)
    re.sub("petahertz(s)?", "PHz", txt)
    re.sub("exahertz(s)?", "EHz", txt)
    re.sub("zettahertz(s)?", "ZHz", txt)
    re.sub("yottahertz(s)?", "YHz", txt)
    # thermodynamic temperature units replacement
    re.sub("kelvin(s)?", "K", txt)
    re.sub("celsius(s)?", "°C", txt)
    re.sub("fahrenheit(s)?", "°F", txt)
    # other units replacement
    re.sub("milliampere(s)?", "mA", txt)
    re.sub("centiampere(s)?", "cA", txt)
    re.sub("deciampere(s)?", "dA", txt)
    re.sub("ampere(s)?", "A", txt)
    re.sub("decampere(s)?", "daA", txt)
    re.sub("hectoampere(s)?", "hA", txt)
    re.sub("kiloampere(s)?", "kA", txt)
    re.sub("megampere(s)?", "MA", txt)
    re.sub("gigampere(s)?", "GA", txt)

    re.sub(" us$", " µs", txt)

    time = re.search("min", txt) or re.search(
        "s", txt) or re.search("h", txt) or re.search("ms", txt) or re.search("µs", txt) or re.search("ns", txt) or re.search("ps", txt)

    speed = re.search("yHz", txt) or re.search(
        "zHz", txt) or re.search("aHz", txt) or re.search("fHz", txt) or re.search("pHz", txt) or re.search("nHz", txt) or re.search("µHz", txt) or re.search("mHz", txt) or re.search("cHz", txt) or re.search("dHz", txt) or re.search("Hz", txt) or re.search("daHz", txt) or re.search("hHz", txt) or re.search("kHz", txt) or re.search("MHz", txt) or re.search("GHz", txt) or re.search("THz", txt) or re.search("PHz", txt) or re.search("EHz", txt) or re.search("ZHz", txt) or re.search("YHz", txt)

    measurement = re.search("ym", txt) or re.search("zm", txt) or re.search("am", txt) or re.search("fm", txt) or re.search("pm", txt) or re.search("nm", txt) or re.search("µm", txt) or re.search("mm", txt) or re.search("cm", txt) or re.search("dm", txt) or re.search("m", txt) or re.search("dam", txt) or re.search("hm", txt) or re.search("km", txt) or re.search(
        "Mm", txt) or re.search("Gm", txt) or re.search("Tm", txt) or re.search("Pm", txt) or re.search("Em", txt) or re.search("Zm", txt) or re.search("Ym", txt) or re.search("thou", txt) or re.search("inch", txt) or re.search("foot", txt) or re.search("yard", txt) or re.search("chain", txt) or re.search("furlong", txt) or re.search("mile", txt) or re.search("league", txt)

    temperature = re.search("K", txt) or re.search(
        "°C", txt) or re.search("°F", txt)

    if time:
        return str(converts(txt, 's')) + ' s'

    elif measurement:
        return str(converts(txt, 'm')) + ' m'

    elif temperature:
        return str(converts(txt, 'K')) + ' K'

    elif speed:
        return str(converts(txt, 'Hz')) + ' Hz'




def normalize(collected_data, source):
    print(blue + ">>> " + reset +
          "Normalizing collected data from " + source + "...")
    # TODO: como normalizar?
    return(collected_data)

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
