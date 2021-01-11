# -*- coding: utf-8 -*-

from colored import fg, attr
import paramiko
import re

from models import ConfigurationItem, ConfigurationItemType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def find_lldp_neighbors(user, pwd, ip):
    """
    It exploits the Linux machine using SSH according to the categories selected by the user. 

    Parameters
    ----------
    user : string
        The username to logon to the machine.

    pwd : string
        The password to logon to the machine.

    ip : string
        The IPv4 address of the machine.

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

    _, stdout, stderr = client.exec_command("sudo lldpcli show neighbors")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        lldp_info = stdout.readlines()
        lldp_info = lldp_info[3:]
        neighbors = []
        n = {}
        for line in lldp_info:
            if re.match(r'-------', line) != None:
                if n != {}:
                    neighbors.append(n)
                else:
                    n = {}
            else:
                n[line.split(":")[0].strip()] = ' '.join(
                    line.split(":")[1:]).strip()

        for nei in neighbors:
            new_ci = ConfigurationItem.ConfigurationItem()
            cap = nei.get("Capability")
            if cap != None and cap != "":
                tp = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType(cap))
                new_ci.set_type(tp.get_id())

            chassisid = nei.get("ChassisID")
            sysname = nei.get("SysName")
            descr = nei.get("SysDescr")
            mac = nei.get("MgmtIP")

            if chassisid != None and chassisid != "":
                methods.define_attribute("chassis id", chassisid, new_ci)
            if sysname != None and sysname != "":
                methods.define_attribute("system name", sysname, new_ci)
            if descr != None and descr != "":
                new_ci.set_description(descr)
            if mac != None and mac != "":
                i = 0
                new_mac = ""
                for i in mac:
                    if re.match(r'\d|\w', i) != None:
                        if i < 2:
                            i += 1
                            new_mac += str(i)
                        else:
                            i = 0
                            new_mac += ":" + str(i)

                new_ci.set_mac_address(new_mac)

            ci = methods.ci_already_exists(new_ci)

            if ci == None:
                ci = new_ci

            methods.add_ci(ci)
