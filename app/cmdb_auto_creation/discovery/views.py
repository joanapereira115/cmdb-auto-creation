from threading import Thread
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import threading
import re
from django.http import JsonResponse
import getpass
import os
from colored import fg, bg, attr

from nmap_discovery import run_nmap
from passwd_vault import vault
from objects import objects

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def vault_setup(request):
    vault.initialize()
    if not os.path.isfile(vault.vault_path):
        return render(request, 'discovery/vault_setup.html', {'vault_created': False})
    else:
        return render(request, 'discovery/vault_setup.html', {'vault_created': True})


def vault_password(request):
    vault.initialize()
    vault_created = request.POST['vault_created']
    if vault_created == "False":
        password = request.POST['password']
        password2 = request.POST['password2']
        if not vault.is_key_valid(password):
            print(red + ">>> " + reset +
                  "The master key should be at least 8 characters.")
            return render(request, 'discovery/vault_setup.html', {
                'error_message': "The master key should be at least 8 characters. Please try again!",
                'vault_created': False
            })
        if not vault.check_key_and_repeat(password, password2):
            print(red + ">>> " + reset +
                  "The master key does not match its confirmation.")
            return render(request, 'discovery/vault_setup.html', {
                'error_message': "The master key does not match its confirmation. Please try again!",
                'vault_created': False
            })
        else:
            vault.define_master_key(password)
            vault.unlock(password)
            return HttpResponseRedirect('http://127.0.0.1:8000/discovery/range', {})
    if vault_created == "True":
        password = request.POST['password']
        v = vault.unlock(password)
        if v == False:
            print(red + ">>> " + reset +
                  "The master key is wrong.")
            return render(request, 'discovery/vault_setup.html', {
                'error_message': "The master key is wrong!",
                'vault_created': True
            })
        else:
            return HttpResponseRedirect('http://127.0.0.1:8000/discovery/range', {})
    return render(request, 'discovery/primary_discovery.html', {})


def range(request):
    user = getpass.getuser()
    users = vault.get_usernames()
    if user in users:
        return render(request, 'discovery/range.html', {'secret': False})
    else:
        return render(request, 'discovery/range.html', {'secret': True})


def handle_range(request):
    addresses = request.POST['range']
    secret = request.POST['secret']
    if secret == "True":
        password = request.POST['password']
        if password == "":
            return render(request, 'discovery/range.html', {
                'error_message': "Specify the machine password.",
                'secret': True
            })
        else:
            user = getpass.getuser()
            # vault.unlock('olaolaola')
            vault.add_secret("discovery machine", user, password)
    if addresses == "":
        # TODO: descobrir endereços IP ativos
        request.session['range'] = "192.168.001.001-010"
        return HttpResponseRedirect('http://127.0.0.1:8000/discovery/primary_discovery/')
    elif re.search(r"(\d{3}\.){3}\d{3}\-\d{3}", addresses) != None:
        request.session['range'] = addresses
        return HttpResponseRedirect('http://127.0.0.1:8000/discovery/primary_discovery/')
    else:
        return render(request, 'discovery/range.html', {
            'error_message': "Specify the address range in the right format.",
            'secret': secret
        })


def basic_discovery(request):
    addresses = request.session['range']
    run_nmap(addresses)
    result = objects
    res = []
    for o in result:
        res.append(o.toJSON())
    data = {'data': res}
    return JsonResponse(data)


def primary_discovery(request):
    addresses = request.session['range']
    return render(request, 'discovery/primary_discovery.html', {'range': addresses})


"""
print(getpass.getuser())

initialize()
if not os.path.isfile(vault_path):
    define_master_key('ola')
unlock('ola')
#add_secret('Windows de Joana', 'winjoana', 'winwin')
print(get_usernames())
show_secret('joana')
lock()
"""
