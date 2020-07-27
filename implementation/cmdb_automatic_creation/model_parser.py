#!/usr/bin/env python3

from collections import Counter
from itertools import zip_longest
import mysql.connector
from mysql.connector import errorcode
import regex as re
import psycopg2
from colored import fg, bg, attr

#cmdb = {"name": "idoit_data", "engine": "mysql", "user": "root", "password": "", "host": "localhost", "port": 3306}

# TODO: considerar a existência de hierarquias
# TODO: considerar que as tabelas possuem os atributos das tabelas a que as chaves estrangeiras se referem
# TODO: implementar para diferentes tipos de ferramentas de gestão de bds
# TODO: questionar sobre características da cim database

cim = {
    "name": "cim_operating_systems",
    "engine": "postgresql",
    "user": "Joana",
    "password": "",
    "host": "localhost",
    "port": 5432
}

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def create_mysql_connection(db):
    cnx = None
    try:
        cnx = mysql.connector.connect(
            user=db["user"],
            password=db["password"],
            host=db["host"],
            database=db["name"])
        print(blue + "\n>>> " + reset + "Connected to " + db["name"] + "...")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(red + "\n>>> " + reset +
                  "Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(red + "\n>>> " + reset + "Database does not exist.")
        else:
            print(red + "\n>>> " + reset + err)
    return cnx


def create_postgresql_connection(db):
    cnx = None
    try:
        cnx = psycopg2.connect(
            host=db["host"], database=db["name"], user=db["user"], password=db["password"])
        print(blue + ">>> " + reset + "Connected to " + db["name"] + "...")
    except (Exception, psycopg2.DatabaseError) as error:
        print(red + ">>> " + reset + error)
    return cnx


def return_tables(cnx, cursor, db, engine):
    res = []
    query = ""
    if engine == "mysql":
        query = ("SELECT table_name FROM information_schema.tables WHERE table_schema=\'" +
                 str(db) + "\';")
    cursor.execute(query)
    for t in cursor:
        res.append(t[0])
    return res


def return_atributes(cnx, cursor, table, db):
    res = []
    query = ("DESCRIBE " + str(db) + "." + str(table) + ";")
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
        avg = prefixes[0][1]/len(l) * 100
        if avg > 80:
            return prefixes[0][0]
        else:
            return ""


def final(model):
    db = model["name"]
    res = {}
    cnx = None
    cursor = None
    if model["engine"] == "mysql":
        cnx = create_mysql_connection(model)
        if(cnx != None):
            cursor = cnx.cursor()
    if model["engine"] == "postgresql":
        cnx = create_postgresql_connection(model)
        if(cnx != None):
            cursor = cnx.cursor()

    if(cnx != None and cursor != None):

        print(blue + ">>> " + reset + "Getting table names from CMDB...")
        table_names = return_tables(cnx, cursor, db, model["engine"])

        print(blue + ">>> " + reset + "Processing table names...")
        # find prefix in names
        prefix = find_prefix(table_names)
        tables = process_names(table_names, prefix)
        new_tables = [x for x in tables]
        tables_atrs = {}
        all_atrs = []
        res['cmdb_tables'] = tables

        for t in table_names:
            all_atrs.extend(return_atributes(cnx, cursor, t, db))
        p = find_prefix(all_atrs)

        print(blue + ">>> " + reset + "Processing attribute names...")
        for t in table_names:
            atrs = return_atributes(cnx, cursor, t, db)
            process_atrs = process_names(atrs, p)
            tables_atrs[t] = process_atrs
        res['cmdb_tables_atrs'] = tables_atrs

        model_proc = {}
        for tb in new_tables:
            org = tables[tb]
            ats = []
            for a in tables_atrs[org]:
                ats.append(a)
            model_proc[tb] = ats
        res['cmdb_proc'] = model_proc

        cursor.close()
        cnx.close()

        print(green + "\n>>> " + reset + "CMDB model processed.")

    return res
