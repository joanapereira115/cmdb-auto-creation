#!/usr/bin/env python3

from collections import Counter
from itertools import zip_longest
import mysql.connector
from mysql.connector import errorcode
import regex as re
import psycopg2

cmdb = {"name": "idoit_data", "engine": "mysql", "user": "root",
        "password": "", "host": "localhost", "port": 3306}

cim = {
    "name": "cim_operating_systems",
    "engine": "postgresql",
    "user": "Joana",
    "password": "",
    "host": "localhost",
    "port": 5432
}


def create_mysql_connection(db):
    cnx = None
    try:
        cnx = mysql.connector.connect(
            user=db["user"],
            password=db["password"],
            host=db["host"],
            database=db["name"])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return cnx


def create_postgresql_connection(db):
    cnx = None
    try:
        cnx = psycopg2.connect(
            host=db["host"], database=db["name"], user=db["user"], password=db["password"])
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return cnx


def return_tables(cnx, cursor, db, engine):
    res = []
    query = ("SELECT table_name FROM information_schema.tables WHERE table_schema=\'" +
             str(db) + "\';")
    cursor.execute(query)
    for t in cursor:
        res.append(t[0])
    return res


def return_atributes(cnx, cursor, table):
    res = []
    query = ("DESCRIBE " + str(table) + ";")
    cursor.execute(query)
    for t in cursor:
        res.append(t[0])
    return res


def process_names(l, prefix):
    res = {}
    for t in l:
        # remove prefix
        new_t = re.sub(rf"{prefix}", "", t, re.DOTALL)
        # check for snake_case
        new_t = re.sub(r"_", " ", new_t, re.DOTALL)
        # check for kebab-case
        new_t = re.sub(r"-", " ", new_t, re.DOTALL)
        # check for camelCase and PascalCase
        new_t = re.sub(r"([a-z0-9])([A-Z0-9])", r"\1 \2", new_t, re.DOTALL)
        # trim spaces at the begin and end
        new_t = re.sub(r"^\s+", "", new_t)
        # trim multiple spaces
        new_t = re.sub(r"\s+", " ", new_t)
        res[new_t.lower()] = t
    return res


def find_prefix(l):
    if len(l) <= 1:
        return ""
    else:
        assert len(l) > 1
        threshold = len(l)
        prefix = []
        prefixes = []
        for chars in zip_longest(*l, fillvalue=''):
            char, count = Counter(chars).most_common(1)[0]
            if count == 1:
                break
            elif count < threshold:
                if prefix:
                    prefixes.append((''.join(prefix), threshold))
                threshold = count
            prefix.append(char)
        if prefix:
            prefixes.append((''.join(prefix), threshold))
        return prefixes[0][0]


def final(model):
    db = model["name"]
    print(model)
    cnx = None
    cursor = None
    if model["engine"] == "mysql":
        cnx = create_mysql_connection(model)
        cursor = cnx.cursor()
    if model["engine"] == "postgresql":
        cnx = create_postgresql_connection(model)
        cursor = cnx.cursor()

    cursor.close()
    cnx.close()


"""
    # return table names from db
    table_names = return_tables(cnx, cursor, db, model["engine"])
    # find prefix in names

    prefix = find_prefix(table_names)
    tables = process_names(table_names, prefix)
    new_tables = [x for x in tables]
    tables_atrs = {}
    all_atrs = []

    for t in table_names:
        all_atrs.extend(return_atributes(cnx, cursor, t))
    p = find_prefix(all_atrs)

    for t in table_names:
        atrs = return_atributes(cnx, cursor, t)
        process_atrs = process_names(atrs, p)
        tables_atrs[t] = process_atrs
    print(tables_atrs)
    model_proc = {}
    for tb in new_tables:
        org = tables[tb]
        ats = []
        for a in tables_atrs[org]:
            ats.append(a)
        model_proc[tb] = ats
    # print(new_tables)
"""


# final(cmdb)
