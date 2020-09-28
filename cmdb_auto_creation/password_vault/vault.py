# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json
import os.path
import sys
from uuid import uuid4
from hashlib import sha256
from .carry import global_scope
from .Config import Config
from .setup import s_initialize, create_db
from .Encryption import Encryption
from .users import validation_key_validate
from .base import get_session
from .Secret import SecretModel
from colored import fg, bg, attr

dir_ = os.path.expanduser('~') + '/.vault/'
config_path = dir_ + '.config'
vault_path = dir_ + '.secure.db'
sessions = {}

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def checkExistence():
    import os

    if os.path.isdir(dir_):
        print(blue + "\n>>> " + reset + "Vault initialized.\n")
        pass
    else:
        print(blue + "\n>>> " + reset + "Creating vault...")
        import os
        try:
            if not os.path.exists(dir_):
                os.makedirs(dir_)
                return True
            return False
        except Exception:
            import sys
            print(red + "\n>>> " + reset +
                  "We were unable to create the folder `%s` to store the vault and configuration file." % (dir_))
            sys.exit()

    if not os.path.isfile(config_path) and os.path.isfile(vault_path):
        print(red + "\n>>> " + reset +
              "It looks like you have a vault setup but your config file is missing. The vault cannot be unlocked without a critical piece of information from the config file (the salt). Please restore the config file before proceeding.")
        sys.exit()


def define_master_key(master_key):
    print(blue + "\n>>> " + reset + "Defining vault password...")
    res = s_initialize(master_key, global_scope['conf'].salt)
    if res is False:
        print()
        return False


def unlock(attempt):
    # Get master key
    key = attempt

    if validate_key(key):
        print(green + "\n>>> " + reset + "Vault unlocked.")
        return True
    else:
        print(red + "\n>>> " + reset + "The password is incorrect.\n")
        return False


def validate_key(key):
    # Create instance of Encryption class with the given key
    global_scope['enc'] = Encryption(key.encode())
    return validation_key_validate(key.encode())


def initialize():
    print(blue + ">>> " + reset + "Initializing the vault...")
    global_scope['db_file'] = vault_path
    checkExistence()
    global_scope['conf'] = Config(config_path)


def get_usernames():
    secrets = get_session().query(SecretModel.login).order_by(SecretModel.id).all()
    if secrets:
        return [result.login for result in secrets]
    return []


def add_secret(name, login, password):
    secret = SecretModel(name=name,
                         login=login,
                         password=password)
    get_session().add(secret)
    get_session().commit()
    print(green + "\n>>> " + reset + "'%s' password added to the vault." % (login))
    return True


def show_secret(login):
    print(blue + "\n>>> " + reset +
          "Checking '%s' password in the vault." % (login))
    item = get_session().query(SecretModel).filter(
        SecretModel.login.like(login)).order_by(SecretModel.id).all()[0]
    return item.password


def lock():
    print(green + "\n>>> " + reset + "Vault locked.")
    global_scope['enc'] = None


def is_key_valid(key):
    if len(key) < 8:
        return False
    return True


def check_key_and_repeat(key, repeat):
    if key != repeat:
        return False
    return True
