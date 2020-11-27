# -*- coding: utf-8 -*-

import regex
from colored import fg, attr
import paramiko

from models import methods
from .linux_discovery import operating_system

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_linux_discovery(ci, user, pwd, ip, categories):
    """
    It exploits the Linux machine using SSH according to the categories selected by the user. 

    Parameters
    ----------
    ci : ConfigurationItem
        The configuration item that represents the machine that is going to be explored.

    user : string
        The username to logon to the machine.

    pwd : string
        The password to logon to the machine.

    ip : string
        The IPv4 address of the machine.

    categories : list
        The list of categories selected by the user.

    Returns
    -------
    boolean
        Returns True if it was possible to connect to the machine, and False otherwise.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ok = True
    try:
        client.connect(ip, 22, user, pwd)
    except paramiko.ssh_exception.AuthenticationException:
        print(red + ">>> " + reset +
              "Wrong credentials! Unable to connect with the machine " + ip + " via SSH.\n")
        ok = False
        return ok
    except TimeoutError:
        print(red + ">>> " + reset +
              "Cannot reach the server! Unable to connect with the machine " + ip + " via SSH.\n")
        ok = False
        return ok
    except:
        print(red + ">>> " + reset +
              "Unable to connect with the machine " + ip + " via SSH.\n")
        ok = False
        return ok

    if ok == True:
        if 'operating systems' in categories:
            operating_system.os_discovery(client, ci)

        # TODO: implement the other discovery mechanisms ('services', 'devices', 'virtual machines', 'databases', 'processing', 'containers', 'cloud systems', 'documents', 'people', 'location', 'storage', 'software', 'hardware', 'network')

    client.close()
    return ok
