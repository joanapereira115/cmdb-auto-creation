# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
import os
import csv

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods
from discovery import discovery_info

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


class FilenameValidator(Validator):
    def validate(self, document):
        csv = regex.match(r'.*\.csv$', document.text)
        if not csv:
            raise ValidationError(
                message='Please enter a valid .csv file name.', cursor_position=len(document.text))


def import_file():
    """
    Asks the user if he imported the file into the 'external_data' folder.
    """
    print(orange + "\n>>> " + reset +
          "Make sure that you have imported the Angry IP Scanner .csv file into the folder 'external_data'.")
    import_question = [
        {
            'type': 'confirm',
            'name': 'import',
            'message': "Have you imported the file into the 'external_data' folder?\n"
        }]
    import_answer = prompt(import_question, style=style).get("import")
    if import_answer == False:
        import_file()


def check_if_file_exists(filename):
    """
    Checks if the Angry IP Scanner exists.

    Parameters
    -------
    filename : string
        The file name.

    Returns
    -------
    boolean
        Returns true if the file exists in the 'external_data' folder, and false otherwise.
    """
    file_path = os.path.abspath(os.getcwd()) + "/../external_data/" + filename
    return os.path.isfile(file_path)


def filename():
    """
    Asks the user for the .csv filename.
    """
    print()
    filename_question = [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'Enter the Angry IP Scanner .csv filename.',
            'validate': FilenameValidator
        }
    ]
    filename_answer = prompt(filename_question, style=style)
    fl = filename_answer["filename"]

    if check_if_file_exists(fl) == False:
        print(red + "\n>>> " + reset +
              "The file does not exist.")
        return filename()
    else:
        return fl


def parse_info():
    import_file()
    fl = filename()
    file_path = os.path.abspath(os.getcwd()) + "/../external_data/" + fl

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        names = []

        for row in csv_reader:
            if line_count == 0:
                names = row
                line_count += 1
            else:
                ci = ConfigurationItem.ConfigurationItem()
                ip = ""
                if 'IP' in names:
                    ip = row[names.index('IP')]
                    if ip != "" and ip != "[n/a]" and ip != "[n/s]":
                        ci.add_ipv4_address(ip)
                        discovery_info.add_ip(ip)
                if 'Hostname' in names:
                    hostname = row[names.index('Hostname')]
                    if hostname != "" and hostname != "[n/a]" and hostname != "[n/s]":
                        methods.define_attribute("hostname", hostname, ci)
                        ci.set_title(hostname)
                if 'Comments' in names:
                    comments = row[names.index('Comments')]
                    if comments != "" and comments != "[n/a]" and comments != "[n/s]":
                        ci.set_description(comments)
                if 'NetBIOS Info' in names:
                    bios = row[names.index('NetBIOS Info')]
                    if bios != "" and bios != "[n/a]" and bios != "[n/s]":
                        methods.define_attribute("Net BIOS", bios, ci)
                if 'MAC Address' in names:
                    mac = row[names.index('MAC Address')]
                    if mac != "" and mac != "[n/a]" and mac != "[n/s]":
                        ci.set_mac_address(mac)
                        discovery_info.add_mac(mac)
                        if ip != "" and ip != "[n/a]" and ip != "[n/s]":
                            discovery_info.add_ip_to_mac(ip, mac)
                if 'MAC Vendor' in names:
                    vendor = row[names.index('MAC Vendor')]
                    if vendor != "" and vendor != "[n/a]" and vendor != "[n/s]":
                        vendor_type = methods.add_ci_type(
                            ConfigurationItemType.ConfigurationItemType("Vendor"))
                        vendor_obj = ConfigurationItem.ConfigurationItem()
                        vendor_obj.set_title(vendor)
                        vendor_obj.set_type(vendor_type.get_id())

                        rel_type_ci_vendor = methods.add_rel_type(
                            RelationshipType.RelationshipType("has vendor"))
                        rel_ci_vendor = methods.create_relation(
                            ci, vendor_obj, rel_type_ci_vendor)
                        rel_ci_vendor.title = str(ci.get_title()) + \
                            " has vendor " + str(vendor_obj.get_title())

                        rel_type_vendor_ci = methods.add_rel_type(
                            RelationshipType.RelationshipType("is vendor of"))
                        rel_vendor_ci = methods.create_relation(
                            vendor_obj, ci, rel_type_vendor_ci)
                        rel_vendor_ci.title = str(vendor_obj.get_title()) + \
                            " is vendor of " + str(ci.get_title())

                        methods.add_ci(vendor_obj)
                        methods.add_rel(rel_ci_vendor)
                        methods.add_rel(rel_vendor_ci)

                methods.add_ci(ci)
