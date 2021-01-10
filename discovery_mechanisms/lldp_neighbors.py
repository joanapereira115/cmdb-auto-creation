# -*- coding: utf-8 -*-

from colored import fg, attr
import paramiko

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
        print(stdout.readlines())
