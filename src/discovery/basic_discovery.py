# -*- coding: utf-8 -*-

import ping3
from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import ipaddress

from password_vault import vault
from discovery_mechanisms import nmap, snmp, packets
from .discovery_info import discovery_info
from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

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


def define_snmp_community():
    """
    Asks the user for the community string for the SNMP discovery.
    """
    users = vault.get_usernames()
    if "SNMP" in users:
        print()
        more_community = [
            {
                'type': 'list',
                'message': 'Do you want to specify another SNMP community string? ("public" is the default)',
                'name': 'more',
                'choices': [{'name': 'Yes'}, {'name': 'No'}]
            }
        ]

        more_community_answer = prompt(more_community, style=style)
        if more_community_answer.get('more') == "Yes":
            print()
            community = [
                {
                    'type': 'password',
                    'message': 'Enter your SNMP devices\' community string:',
                    'name': 'community',
                    'validate': NotEmpty
                }
            ]
            community_answer = prompt(community, style=style)
            community = community_answer.get("community")
            vault.add_secret(community, "SNMP", community)
            define_snmp_community()
    else:
        vault.add_secret("public", "SNMP", "public")
        print()
        more_community = [
            {
                'type': 'list',
                'message': 'Do you want to specify another SNMP community string? ("public" is the default)',
                'name': 'more',
                'choices': [{'name': 'Yes'}, {'name': 'No'}]
            }
        ]

        more_community_answer = prompt(more_community, style=style)
        if more_community_answer.get('more') == "Yes":
            print()
            community = [
                {
                    'type': 'password',
                    'message': 'Enter your SNMP devices\' community string:',
                    'name': 'community',
                    'validate': NotEmpty
                }
            ]
            community_answer = prompt(community, style=style)
            community = community_answer.get("community")
            vault.add_secret(community, "SNMP", community)
            define_snmp_community()


def check_ip(ip):
    """
    Checks if the IPv4 addresse is available via ping.

    Parameters
    --------
    ip : string
        The IP address that we want to check.
    """
    print(blue + "\n>>> " + reset +
          "Checking the availability of the IP address " + str(ip) + "...")

    r = None
    try:
        r = ping3.ping(ip, timeout=1)
    except:
        r = None
    if r == None:
        if ip in discovery_info.get("ip_addresses"):
            print(red + ">>> " + reset + "Not available via ping.")
            return False
    return True


def define_networks():
    """
    Groups the various addresses in its subnets and creates the respective objects.
    """
    for net in discovery_info.get("networks"):
        net_ips = [str(x) for x in list(ipaddress.ip_network(net).hosts())]
        for ip in net_ips:
            if ip in discovery_info.get("ip_addresses"):
                if ip not in discovery_info.get("networks").get(net):
                    discovery_info["networks"][net].append(ip)

    for net in discovery_info.get("networks"):
        net_obj = ConfigurationItem.ConfigurationItem()
        tp = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Layer 3 Network"))
        net_obj.set_type(tp.get_id())
        net_obj.set_title(net)

        for ip in discovery_info.get("networks").get(net):
            ci = ConfigurationItem.ConfigurationItem()
            ci.add_ipv4_address(ip)

            rel_type_1 = methods.add_rel_type(
                RelationshipType.RelationshipType("part of network"))
            rel_obj_1 = methods.create_relation(ci, net_obj, rel_type_1)
            rel_obj_1.set_title(str(ci.get_title()) +
                                " part of network " + str(net_obj.get_title()))

            rel_type_2 = methods.add_rel_type(
                RelationshipType.RelationshipType("has address"))
            rel_obj_2 = methods.create_relation(net_obj, ci, rel_type_2)
            rel_obj_2.set_title(str(net_obj.get_title()) + " has address " +
                                str(ci.get_title()))

            methods.add_ci(ci)
            methods.add_rel(rel_obj_1)
            methods.add_rel(rel_obj_2)

        methods.add_ci(net_obj)


def basic_discovery():
    """
    Executes the basic discovery of the infrastructure.
    It uses the following methods:
        - ping
        - Nmap
        - SNMP 
        - LLDP
    """
    rem = []

    packets.explore_packets()

    unlock_vault()
    define_snmp_community()
    secrets = vault.show_secrets("SNMP")

    for ip in discovery_info.get("ip_addresses"):
        if ip not in discovery_info.get("visited_addresses"):
            discovery_info["visited_addresses"].append(ip)

            av = check_ip(ip)
            if av == True:
                nmap.run_nmap(ip)
                snmp.run_snmp(ip, secrets)
            else:
                rem.append(ip)

    for i in rem:
        discovery_info["ip_addresses"].remove(i)

    define_networks()

    print(green + "\n>>> " + reset + "Basic discovery ended.")
    discovery_info["visited_addresses"] = []
