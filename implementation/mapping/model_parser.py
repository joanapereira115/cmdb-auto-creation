#!/usr/bin/env python3

from collections import Counter
from itertools import zip_longest
import mysql.connector
from mysql.connector import errorcode
import regex as re

cmdb = {
    "name": "idoit_data",
    "engine": "mysql",
    "user": "root",
    "password": "",
    "host": "localhost",
    "port": 3306
}


def create_connection(cmdb):
    cnx = None
    if cmdb["engine"] == "mysql":
        try:
            cnx = mysql.connector.connect(
                user=cmdb["user"],
                password=cmdb["password"],
                host=cmdb["host"],
                database=cmdb["name"])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    return cnx


def return_tables(cnx, cursor, db):
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


def final(cmdb):
    db = cmdb["name"]
    cnx = create_connection(cmdb)
    cursor = cnx.cursor()
    # return table names from db
    table_names = return_tables(cnx, cursor, db)
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

    cmdb_proc = {}
    for tb in new_tables:
        org = tables[tb]
        ats = []
        for a in tables_atrs[org]:
            ats.append(a)
        cmdb_proc[tb] = ats

    cursor.close()
    cnx.close()


final(cmdb)
