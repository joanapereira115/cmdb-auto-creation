# definir o modelo de dados com base nos objetos descobertos (aceder à BD)

import requests
from urllib.parse import quote
import json
from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import regex

from normalization import normalization
from .db_data_model import db_data_model

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

prefix = 'prefix : <http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#>'


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


class NumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'\d+', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid port number.',
                cursor_position=len(document.text))  # Move cursor to end


def db_specification():
    """
    Asks the user to enter the necessary information (server address, port number and repository name) to access the database.

    Returns
    -------
    dict
        The database information (server address, port number and repository name).

    """
    db_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the IP address of the GraphDB server (use format yyx.yyx.yyx.yyx where \'y\' is optional):',
            'name': 'server',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter the port number where GraphDB is running:',
            'name': 'port',
            'validate': NumberValidator
        },
        {
            'type': 'input',
            'message': 'Enter the name of the GraphDB repository:',
            'name': 'repository',
            'validate': NotEmpty
        }
    ]

    db_specification_answer = prompt(db_specification_question, style=style)
    return db_specification_answer


def test_db_connection(server, port, repository):
    """
    Tests the access to the database.

    Parameters
    ----------
    server : string
        The IP address of the database server.

    port : string
        The port where the database is running.

    repository : string
        The name of the database repository.

    Returns
    -------
    boolean
        Returns true if the connection was successful and false otherwise.

    """
    global db_url
    db_url = "http://" + server + ":" + port + "/repositories/" + repository

    try:
        s = requests.Session()
        connection = s.get(db_url)
        unknown = regex.search(r'unknown repository',
                               connection.text, regex.IGNORECASE)
        if unknown != None:
            print(red + "\n>>> " + reset +
                  "Unknown repository. Please verify the connection information.\n")
            return False
        else:
            print(green + "\n>>> " + reset + "Successfully connected.\n")
            return True
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to GraphDB. Please verify the connection information.\n")
        return False

# TODO: verificar que o pedido é executado com sucesso!


def execQuery(query):
    """
    Executes a request to the database based on a SPARQL query.

    Parameters
    ----------
    query : string
        The SPARQL query.

    Returns
    -------
    Response()
        Returns the response of the request.

    """
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded

    s = requests.Session()
    response = s.get(url)
    return response


def get_ci_types():
    """
    Processes the types of CIs existing in the database.

    Returns
    -------
    list
        Returns the list of the CI types.

    """
    res = []
    query_string = "select distinct ?t where {?s rdf:type :ConfigurationItemType. ?s :name ?t .}"
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            res.append(w)
    return res


def get_relation_types():
    """
    Processes the types of relationships existing in the database.

    Returns
    -------
    list
        Returns the list of the relationship types.

    """
    res = []
    query_string = "select distinct ?t where {?s rdf:type :RelationshipType. ?s :name ?t .}"
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            res.append(w)
    return res


def get_ci_attributes(ci_type):
    """
    Processes the attributes of a configuration item type in the database.

    Returns
    -------
    list
        Returns the list of attributes.

    """
    res = []
    query_string = """
    select distinct ?at where {?s rdf:type :ConfigurationItem .
        ?s :has_ci_type ?x .
        ?x :name \"""" + ci_type + """\" .
        ?s :has_attribute ?a .
        ?a :name ?at .
    }"""

    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            if w.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                w = w[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            res.append(w)

    query_string = "select ?s where { ?s rdfs:domain :ConfigurationItem . ?s rdfs:range xsd:string . }"
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            if w.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                w = w[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            res.append(w)
    return res


def get_rel_attributes(rel_type):
    """
    Processes the attributes of a relationship type in the database.

    Returns
    -------
    list
        Returns the list of attributes.

    """
    res = []
    query_string = """
    select distinct ?at where {?s rdf:type :Relationship .
        ?s :has_rel_type ?x .
        ?x :name \"""" + rel_type + """\" .
        ?s :has_attribute ?a .
        ?a :name ?at .
    }"""
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            if w.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                w = w[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            res.append(w)
    return res


def process_db_data_model():
    """
    Handles the information about the database, processing, and saving it to the data model.
    """
    print(blue + ">>> " + reset + "Make sure that GraphDB is running.\n")
    db_info = db_specification()

    server = db_info.get("server")
    port = db_info.get("port")
    repository = db_info.get("repository")

    connection = test_db_connection(server, port, repository)
    if connection == False:
        process_db_data_model()
    else:
        ci_types = get_ci_types()
        rel_types = get_relation_types()

        ci_attributes = {}
        for ci in ci_types:
            ci_attributes[ci] = get_ci_attributes(ci)

        rel_attributes = {}
        for rel in rel_types:
            rel_attributes[rel] = get_rel_attributes(rel)

        new_ci_types = {x: normalization.clean_text(x) for x in ci_types}
        new_rel_types = {x: normalization.clean_text(x) for x in rel_types}
        new_ci_attributes = {}
        for ci in ci_attributes:
            new_ci_attributes[ci] = {x: normalization.clean_text(
                x) for x in ci_attributes.get(ci)}

        new_rel_attributes = {}
        for rel in rel_attributes:
            new_rel_attributes[rel] = {x: normalization.clean_text(
                x) for x in rel_attributes.get(rel)}

        db_data_model["ci_types"] = new_ci_types
        db_data_model["rel_types"] = new_rel_types
        db_data_model["ci_attributes"] = new_ci_attributes
        db_data_model["rel_attributes"] = new_rel_attributes
    return db_info

# TODO: devo fazer o logout?