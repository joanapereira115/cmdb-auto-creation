# -*- coding: utf-8 -*-

import regex
from colored import fg, attr
import paramiko

from models import methods
from .linux_discovery import operating_system, processing, storage, software

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

    _, stdout, stderr = client.exec_command("hostnamectl")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        hostnamectl = stdout.readlines()
        info = {}
        if len(hostnamectl) > 0:
            for line in hostnamectl:
                info[regex.sub("\n|\"", "", line.split(":")[0]).strip()] = regex.sub(
                    "\n|\"", "", line.split(":")[1]).strip()
        for at in info:
            if at == "Static hostname":
                ci.set_title(info.get(at))
            else:
                methods.define_attribute(at, info.get(at), ci)

    if ok == True:
        if 'operating systems' in categories:
            operating_system.os_discovery(client, ci)

        if 'processing' in categories:
            processing.processing_discovery(client, ci)

        if 'storage' in categories:
            storage.storage_discovery(client, ci)

        if 'software' in categories:
            software.sw_discovery(client, ci)

        if 'devices' in categories:
            devices.devices_discovery(client, ci)

        # TODO: implement the other discovery mechanisms ('services', 'virtual machines', 'databases', 'containers', 'cloud systems', 'documents', 'people', 'location', 'hardware', 'network')

    client.close()
    return ok
