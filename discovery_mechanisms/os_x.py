# -*- coding: utf-8 -*-

import regex
from colored import fg, bg, attr
import paramiko

from models import methods
from .os_x_discovery import operating_system, processing, location, storage, software, hardware, network

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_os_x_discovery(ci, user, pwd, ip, categories):
    """
    It exploits the OS X machine using SSH according to the categories selected by the user. 

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
    except:
        print(red + ">>> " + reset +
              "Unable to connect with the machine " + ip + " via SSH.\n")
        ok = False
        return ok

    if ok == True:
        _, stdout, stderr = client.exec_command("/bin/hostname")
        error = stderr.read().decode('utf-8')
        if error != "":
            print(red + ">>> " + reset + str(error) + "\n")
        else:
            hostname = stdout.readlines()
            if len(hostname) > 0:
                value = hostname[0].strip('\n')
                hostname_attr = methods.create_attribute("hostname", value)
                methods.add_attribute(hostname_attr, ci)

        _, stdout, stderr = client.exec_command(
            "ioreg -c IOPlatformExpertDevice -d 2 | grep IOPlatformSerialNumber")
        error = stderr.read().decode('utf-8')
        if error != "":
            print(red + ">>> " + reset + str(error) + "\n")
        else:
            serial = stdout.readlines()
            if len(serial) > 0:
                value = serial[0].strip('\n')
                value = regex.sub(r' ', "", value)
                value = regex.sub(r'\"', "", value)
                beg = len('IOPlatformSerialNumber=')
                value = value[beg:]
                ci.set_serial_number(value)

        if 'operating systems' in categories:
            operating_system.os_discovery(client, ci)
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

        # TODO: implement the other discovery mechanisms
        """    
        if 'devices' in categories:
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

    client.close()
    return ok
