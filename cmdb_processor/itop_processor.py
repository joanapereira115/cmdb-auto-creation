# -*- coding: utf-8 -*-

import requests
import json
from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import regex
import mysql.connector
from mysql.connector import errorcode
import wordninja

from normalization import normalization
from .cmdb_data_model import cmdb_data_model

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
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
                cursor_position=len(document.text))  # Move cursor to end


class AddressValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'(\d{1,3}\.){3}\d{1,3}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address.',
                cursor_position=len(document.text))  # Move cursor to end


def db_specification():
    """
    Asks the user to enter the necessary information (server address, username, password and database name) to access the iTop CMDB.

    Returns
    -------
    dict
        The database information (server address, username, password and database name).

    """
    db_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the IP address of your database server (use format yyx.yyx.yyx.yyx where \'y\' is optional):',
            'name': 'server',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter your database name:',
            'name': 'db_name',
            'validate': NotEmpty
        },
        {
            'type': 'input',
            'message': 'Enter your database username:',
            'name': 'username',
            'validate': NotEmpty
        },
        {
            'type': 'password',
            'message': 'Enter your database password:',
            'name': 'password'
        }
    ]
    db_specification_answer = prompt(db_specification_question, style=style)
    return db_specification_answer


def test_db_connection(server, db_name, username, passwd):
    """
    Tests the access to the CMDB.

    Parameters
    ----------
    server : string
        The IP address of the CMDB server.

    db_name: string
        The CMDB database name.

    username : string
        The CMDB username.

    password : string
        The CMDB password.

    Returns
    -------
    boolean
        Returns true if the connection was successful and false otherwise.

    """
    print(blue + "\n>>> " + reset + "Checking iTop database connection...")
    cnx = None
    try:
        cnx = mysql.connector.connect(
            user=username,
            password=passwd,
            host=server,
            database=db_name)
        print(green + "\n>>> " + reset + "Successfully connected.\n")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(red + "\n>>> " + reset +
                  "Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(red + "\n>>> " + reset + "Database does not exist.")
        else:
            print(red + "\n>>> " + reset + str(err))
    return cnx


def return_tables(cnx, cursor, db):
    res = []
    query = ""
    query = (
        "SELECT table_name FROM information_schema.tables WHERE table_schema=\'" + str(db) + "\';")
    cursor.execute(query)
    for t in cursor:
        res.append(t[0])
    return res


def get_ci_types(tables):
    res = []
    for t in tables:
        if regex.search(r'view_', t) == None and regex.search(r'lnk', t) == None:
            res.append(t)
    return res


def get_rel_types(tables):
    res = []
    for t in tables:
        if regex.search(r'lnk', t) != None and regex.search(r'view_', t) == None:
            res.append(t)
    return res


def get_attributes(table, db_name, cursor):
    res = {}
    query = ("DESCRIBE " + str(db_name) + "." + str(table) + ";")
    cursor.execute(query)
    for t in cursor:
        res[t[0]] = t[1]
    return res


def get_type(what, table, text):
    int_ = regex.search(r'int', text, flags=regex.IGNORECASE)
    txt = regex.search(r'varchar', text, flags=regex.IGNORECASE) or regex.search(
        r'text', text, flags=regex.IGNORECASE) or regex.search(
        r'date', text, flags=regex.IGNORECASE) or regex.search(
        r'blob', text, flags=regex.IGNORECASE)
    dec = regex.search(r'decimal', text, flags=regex.IGNORECASE)
    enum = regex.search(r'enum', text, flags=regex.IGNORECASE)

    if int_ != None:
        return "int"
    if txt != None:
        return "string"
    if dec != None:
        return "float"
    if enum != None:
        enums = regex.findall(r'\'([^\']*)\'', text)
        proc_enums = {}
        for e in enums:
            if regex.search(r'_', e) == None:
                proc_enums[e] = normalization.clean_text(
                    " ".join(wordninja.split(e)))
            else:
                proc_enums[e] = normalization.clean_text(e)
        if what == "ci":
            cmdb_data_model["ci_dialog_attributes"][table] = {}
            cmdb_data_model["ci_dialog_attributes"][table][text] = proc_enums
        elif what == "rel":
            cmdb_data_model["rel_dialog_attributes"][table] = {}
            cmdb_data_model["rel_dialog_attributes"][table][text] = proc_enums
        return "string"
    return "string"


def restrictions(rel_attributes):
    # {"relationship type": [{"source CI attribute": "CI type", "target CI attribute": "CI type"}, ...], ...}
    for rel in rel_attributes:
        attrs = rel_attributes.get(rel)
        cmdb_data_model["rel_restrictions"][rel] = {}
        for a in attrs:
            if regex.search(r'_id', a) != None:
                cmdb_data_model["rel_restrictions"][rel][a] = regex.sub(
                    r'_id', "", a)
                if regex.sub(r'_id', "", a) not in cmdb_data_model["ci_types"]:
                    print(regex.sub(r'_id', "", a))
        # TODO: corrigir!
    print(json.dumps(
        cmdb_data_model["rel_restrictions"], indent=4, sort_keys=True))


def process_itop():
    """
    Processes the iTop CMDB data model, obtaining information about configuration item types,
    relationship types, configuration items, and relationship attributes, restrictions between relationships,
    data types of attributes, and values for dialog type attributes.

    Returns
    -------
    dict
        Returns the CMDB information (server address, username, password and database name).

    """
    print(blue + "\n>>> " + reset + "Make sure that i-Top is running.\n")
    db_info = db_specification()

    server = db_info.get("server")
    username = db_info.get("username")
    password = db_info.get("password")
    db_name = db_info.get("db_name")

    connection = test_db_connection(server, db_name, username, password)
    if connection == None:
        process_itop()
    else:
        print(blue + ">>> " + reset + "Processing iTop CMDB data model...\n")
        cursor = connection.cursor()
        table_names = return_tables(connection, cursor, db_name)

        ci_types = get_ci_types(table_names)
        for ci in ci_types:
            if regex.search(r'_', ci) == None:
                cmdb_data_model["ci_types"][ci] = normalization.clean_text(
                    " ".join(wordninja.split(ci)))
            else:
                cmdb_data_model["ci_types"][ci] = normalization.clean_text(
                    ci)

        rel_types = get_rel_types(table_names)
        for rel in rel_types:
            if regex.search(r'_', rel) == None:
                cmdb_data_model["rel_types"][rel] = normalization.clean_text(
                    " ".join(wordninja.split(rel[len("lnk"):])))
            else:
                cmdb_data_model["rel_types"][rel] = normalization.clean_text(
                    rel[len("lnk"):])

        for ci_type in ci_types:
            attrs = get_attributes(ci_type, db_name, cursor)
            proc_attrs = {}
            types_attrs = {}
            for a in attrs:
                if regex.search(r'_', a) == None:
                    proc_attrs[a] = normalization.clean_text(
                        " ".join(wordninja.split(a)))
                else:
                    proc_attrs[a] = normalization.clean_text(a)
                types_attrs[ci_type] = get_type("ci", ci_type, attrs.get(a))
            cmdb_data_model["ci_attributes"][ci_type] = proc_attrs
            cmdb_data_model["ci_attributes_data_types"][ci_type] = types_attrs

        for rel_type in rel_types:
            attrs = get_attributes(rel_type, db_name, cursor)
            proc_attrs = {}
            types_attrs = {}
            for a in attrs:
                if regex.search(r'_', a) == None:
                    proc_attrs[a] = normalization.clean_text(
                        " ".join(wordninja.split(a)))
                else:
                    proc_attrs[a] = normalization.clean_text(a)
                types_attrs[rel_type] = get_type("rel", rel_type, attrs.get(a))
            cmdb_data_model["rel_attributes"][rel_type] = proc_attrs
            cmdb_data_model["rel_attributes_data_types"][ci_type] = types_attrs

    restrictions(cmdb_data_model["rel_attributes"])
    return db_info