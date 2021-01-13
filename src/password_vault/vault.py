# -*- coding: utf-8 -*-

import os
import sqlite3
from colored import fg, attr
import codecs

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

dbFolder = os.path.abspath(os.getcwd())
dbPath = os.path.join(os.path.abspath(os.getcwd()), 'pwd.db')


def checkExistence():
    if os.path.isdir(dbFolder):
        print(green + "\n>>> " + reset + "Vault exists.")
        pass
    else:
        print(blue + "\n>>> " + reset +
              "Password vault does not exists. Creating vault...")
        try:
            if not os.path.exists(dbFolder):
                os.makedirs(dbFolder)
        except Exception:
            import sys
            print(red + "\n>>> " + reset +
                  "We were unable to create the folder `%s` to store the vault and configuration file." % (dbFolder))
            sys.exit()

    if not os.path.isfile(dbPath):
        f = open(dbPath, "x")
        print(blue + "\n>>> " + reset +
              "Creating the database file...")
        f.close()


def initialize():
    print(blue + ">>> " + reset + "Initializing the vault...")
    checkExistence()

    global db_conn
    db_conn = sqlite3.connect(dbPath)
    global cursor
    cursor = db_conn.cursor()

    create_table_query = """CREATE TABLE IF NOT EXISTS Passwords (name text, username text, password text)"""
    cursor.execute(create_table_query)


def define_master_key(master_key):
    if len(master_key) < 8:
        return False
    else:
        create_user_query = """INSERT INTO Passwords (name, username, password) VALUES (?, ?, ?)"""
        cursor.execute(create_user_query, [
            'vault', 'vault', codecs.encode(master_key, 'rot-13')])

        db_conn.commit()
        print(green + "\n>>> " + reset +
              "Your vault has been created and encrypted with your master key.")
        return True


def password_already_definined():
    user_exists_query = 'SELECT * FROM Passwords WHERE name = \'vault\''
    if cursor.execute(user_exists_query).fetchone() == None:
        return False
    else:
        return True


def unlock(attempt):
    global db_conn
    db_conn = sqlite3.connect(dbPath)
    global cursor
    cursor = db_conn.cursor()

    query = 'SELECT * FROM Passwords WHERE name = ?'
    entry = cursor.execute(query, ["vault"]).fetchone()

    correct_pass = codecs.decode(entry[2], 'rot-13')

    if attempt == correct_pass:
        print(green + "\n>>> " + reset + "Vault unlocked.")
        return True
    else:
        print(red + "\n>>> " + reset + "The password is incorrect.")
        return False


def add_secret(name, login, password):
    if name == 'vault':
        print(red + "\n>>> " + reset + "Sorry, user is a reserved name.")
        return False

    entry_exist_query = 'SELECT * FROM Passwords WHERE name = ?'
    query = 'INSERT INTO Passwords (name, username, password) VALUES (?, ?, ?)'

    encrypted_pass = codecs.encode(password, 'rot-13')

    try:
        if len(cursor.execute(entry_exist_query, [name]).fetchall()) >= 1:
            print(red + "\n>>> " + reset + "Sorry, this name already exists.")
            return False
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    ok = False

    try:
        cursor.execute(query, [name, login, encrypted_pass])
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        db_conn.commit()
        print(green + "\n>>> " + reset + "Password added to the vault.")
        return True
    else:
        return False


def show_secrets(name):
    res = []
    query = 'SELECT * FROM Passwords WHERE name = ?'
    ok = False

    try:
        entry = cursor.execute(query, [name]).fetchall()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        for e in entry:
            res.append(codecs.decode(e[2], 'rot-13'))
        return res
    else:
        return []


def show_secret_by_name(name):
    query = 'SELECT * FROM Passwords WHERE name = ?'
    ok = False

    try:
        entry = cursor.execute(query, [name]).fetchone()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        return codecs.decode(entry[2], 'rot-13')
    else:
        return None


def show_secret_by_username(username):
    query = 'SELECT * FROM Passwords WHERE username = ?'
    ok = False

    try:
        entry = cursor.execute(query, [username]).fetchone()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        return codecs.decode(entry[2], 'rot-13')
    else:
        return None


def show_username_by_name(name):
    query = 'SELECT * FROM Passwords WHERE name = ?'
    ok = False

    try:
        entry = cursor.execute(query, [name]).fetchone()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        return entry[1]
    else:
        return None


def get_usernames():
    res = []
    query = 'SELECT username FROM Passwords'
    ok = False

    try:
        entry = cursor.execute(query, []).fetchall()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        for e in entry:
            res.append(e[0])
        return res
    else:
        return []


def get_names():
    res = []
    query = 'SELECT name FROM Passwords'
    ok = False

    try:
        entry = cursor.execute(query, []).fetchall()
        ok = True
    except sqlite3.ProgrammingError as e:
        print(red + "\n>>> " + reset + "Vault is locked.")

    if ok == True:
        for e in entry:
            res.append(e[0])
        return res
    else:
        return []


def lock():
    cursor.close()
    db_conn.close()
    print(green + "\n>>> " + reset + "Vault locked.")


def delete_vault():
    os.remove(dbPath)
