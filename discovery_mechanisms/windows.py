# -*- coding: utf-8 -*-

from colored import fg, bg, attr
import winrm

from models import methods
from .windows_discovery import operating_system, services, devices


blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def run_windows_discovery(ci, user, pwd, ip, categories):
    """
    It exploits the Windows machine using WinRM according to the categories selected by the user. 

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

    ok = True
    try:
        s = winrm.Session(ip, auth=(user, pwd))
    except:
        print(red + ">>> " + reset +
              "Unable to connect with the machine " + ip + " via WinRM.\n")
        ok = False
        return ok
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
        if 'services' in categories:
            services.services_discovery(s, ci)
        if 'devices' in categories:
            devices.devices_discovery(s, ci)

        # TODO: implement the other discovery mechanisms
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
        if 'virtual machines' in categories:
            vm_discovery(client, ci)
        if 'databases' in categories:
            db_discovery(client, ci)
        if 'containers' in categories:
            containers_discovery(client, ci)
        if 'cloud systems' in categories:
            cloud_discovery(client, ci)
        if 'documents' in categories:
            doc_discovery(client, ci)
        if 'people' in categories:
            people_discovery(client, ci)
        """

    return ok
