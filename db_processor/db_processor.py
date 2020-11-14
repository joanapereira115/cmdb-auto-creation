# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
from colored import fg, attr
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
    query_string = "select distinct ?t where {?s rdf:type :ConfigurationItemType. ?s :title ?t .}"
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
    query_string = "select distinct ?t where {?s rdf:type :RelationshipType. ?s :title ?t .}"
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            res.append(w)
    return res


def get_ci_attributes(ci_type):
    """
    Processes the attributes of a configuration item type in the database.

    Parameters
    ----------
    ci_type : string
        The configuration item type.

    Returns
    -------
    list
        Returns the list of attributes.
    """
    res = []
    query_string = """
    select distinct ?at where {?s rdf:type :ConfigurationItem .
        ?s :has_ci_type ?x .
        ?x :title \"""" + ci_type + """\" .
        ?s :has_attribute ?a .
        ?a :title ?at .
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

    Parameters
    ----------
    rel_type : string
        The relationship type.

    Returns
    -------
    list
        Returns the list of attributes.
    """
    res = []
    query_string = """
    select distinct ?at where {?s rdf:type :Relationship .
        ?s :has_rel_type ?x .
        ?x :title \"""" + rel_type + """\" .
        ?s :has_attribute ?a .
        ?a :title ?at .
    }"""
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            if w.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                w = w[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            res.append(w)

    query_string = "select ?s where { ?s rdfs:domain :Relationship . ?s rdfs:range xsd:string . }"
    r = execQuery(query_string)
    for w in r.text.split('\n')[1:]:
        w = regex.sub(r"\r", "", w)
        if w != "":
            if w.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                w = w[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            res.append(w)
    return res


def process_db_data_model(db_info):
    """
    Processes the GraphDB database data model, obtaining information about configuration item types, 
    relationship types, configuration items, and relationship attributes.

    Parameters
    ----------
    db_info : dict
        The information (server address, port number and repository name) about the database.
    """

    server = db_info.get("server")
    port = db_info.get("port")
    repository = db_info.get("repository")

    global db_url
    db_url = "http://" + server + ":" + port + "/repositories/" + repository

    global prefix
    prefix = 'prefix : <http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#>'

    ci_types = get_ci_types()
    rel_types = get_relation_types()

    ci_attributes = {}
    for ci in ci_types:
        ci_attributes[ci] = get_ci_attributes(ci)

    rel_attributes = {}
    for rel in rel_types:
        rel_attributes[rel] = get_rel_attributes(rel)

    new_ci_types = {
        x: normalization.parse_text_to_compare(x) for x in ci_types}
    new_rel_types = {
        x: normalization.parse_text_to_compare(x) for x in rel_types}
    new_ci_attributes = {}
    for ci in ci_attributes:
        new_ci_attributes[ci] = {x: normalization.parse_text_to_compare(
            x) for x in ci_attributes.get(ci)}

    new_rel_attributes = {}
    for rel in rel_attributes:
        new_rel_attributes[rel] = {x: normalization.parse_text_to_compare(
            x) for x in rel_attributes.get(rel)}

    db_data_model["ci_types"] = new_ci_types
    db_data_model["rel_types"] = new_rel_types
    db_data_model["ci_attributes"] = new_ci_attributes
    db_data_model["rel_attributes"] = new_rel_attributes

    print(green + "\n>>> " + reset +
          "The database model was successfully processed.")
