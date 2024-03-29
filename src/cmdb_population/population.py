# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
from colored import fg, attr
import regex
from .idoit_population import run_idoit_population
from .itop_population import run_itop_population
from cmdb_processor import cmdb_data_model
from model_mapper import transformation_rules

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


prefix = 'prefix : <http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#>'


def get_cis(db_info):
    """
    Obtains the existing configuration items in the database.

    Parameters
    -------
    db_info : dict
        The information (server address, port number and repository name) about the database.

    Returns
    -------
    list
        Returns the list of identifiers of the existing configuration items.
    """
    global db_url
    db_url = "http://" + \
        db_info.get("server") + ":" + db_info.get("port") + \
        "/repositories/" + db_info.get("repository")

    cis_ids = []
    query = "select distinct ?s where { ?s rdf:type :ConfigurationItem .}"
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)
    objects = response.text.split()[1:]

    for o in objects:
        if o.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
            o = ":" + \
                o[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            cis_ids.append(o)

    return cis_ids


def get_rels(db_info):
    """
    Obtains the existing relationships in the database.

    Parameters
    -------
    db_info : dict
        The information (server address, port number and repository name) about the database.

    Returns
    -------
    list
        Returns the list of identifiers of the existing relationships.
    """
    rels_ids = []
    query = "select distinct ?s where { ?s rdf:type :Relationship .}"
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)
    objects = response.text.split()[1:]

    for o in objects:
        if o.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
            o = ":" + \
                o[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            rels_ids.append(o)

    return rels_ids


def get_ci_type(ci_id):
    """
    Obtains the type of a configuration item.

    Parameters
    -------
    ci_id : string
        The identifier of the configuration item.

    Returns
    -------
    string
        Returns the type of the configuration item.
    """
    query = """
    select distinct ?k where { 
        """ + ci_id + """ :has_ci_type ?s .
        ?s :title ?k .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    ci_type = response.text.split("\n")[1:]
    ci_type = regex.sub(r"\r", "", ci_type[0])

    return ci_type


def get_rel_type(rel_id):
    """
    Obtains the type of a relationship.

    Parameters
    -------
    ci_id : string
        The identifier of the relationship.

    Returns
    -------
    string
        Returns the type of the relationship.
    """
    query = """
    select distinct ?k where { 
        """ + rel_id + """ :has_rel_type ?s .
        ?s :title ?k .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    rel_type = response.text.split("\n")[1:]
    rel_type = regex.sub(r"\r", "", rel_type[0])

    return rel_type


def get_ci_attributes(ci_id):
    """
    Obtains the attributes, and its corresponding values, of a configuration item.

    Parameters
    -------
    ci_id : string
        The identifier of the configuration item.

    Returns
    -------
    dict
        Returns the attributes, and its corresponding values, of the configuration item.
    """
    attrs = {}
    query = """
    select distinct ?at ?v where { 
    """ + ci_id + """ :has_attribute ?a .
        ?a :title ?at .
        ?a :value ?v .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    ats = response.text.split('\n')[1:]
    for at in ats:
        if at != "":
            at = regex.sub(r"\r", "", at)
            name = at.split(',')[0]
            value = at.split(',')[1]
            attrs[name] = value

    query = """select distinct ?s ?a where { 
        """ + ci_id + """ ?s ?a .
        ?s rdfs:range xsd:string .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    ats = response.text.split('\n')[1:]
    for at in ats:
        if at != "":
            at = regex.sub(r"\r", "", at)
            name = at.split(',')[0]
            if name.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                name = name[len(
                    "http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            value = at.split(',')[1]
            if name in attrs:
                # TODO: how to deal with duplicate attributes?
                pass
            attrs[name] = value

    return attrs


def get_rel_attributes(rel_id):
    """
    Obtains the attributes, and its corresponding values, of a relationship.

    Parameters
    -------
    rel_id : string
        The identifier of the relationship.

    Returns
    -------
    dict
        Returns the attributes, and its corresponding values, of the relationship.
    """
    attrs = {}
    query = """
    select distinct ?at ?v where { 
    """ + rel_id + """ :has_attribute ?a .
        ?a :title ?at .
        ?a :value ?v .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    ats = response.text.split('\n')[1:]
    for at in ats:
        if at != "":
            at = regex.sub(r"\r", "", at)
            name = at.split(',')[0]
            value = at.split(',')[1]
            attrs[name] = value

    query = """select distinct ?s ?a where { 
        """ + rel_id + """ ?s ?a .
        ?s rdfs:range xsd:string .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    ats = response.text.split('\n')[1:]
    for at in ats:
        if at != "":
            at = regex.sub(r"\r", "", at)
            name = at.split(',')[0]
            if name.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
                name = name[len(
                    "http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]
            value = at.split(',')[1]
            attrs[name] = value

    return attrs


def get_source(rel_id):
    """
    Obtains the identifier of the source configuration item of a relationship.

    Parameters
    -------
    rel_id : string
        The identifier of the relationship.

    Returns
    -------
    string
        Returns the identifier of the source configuration item of the relationship.
    """
    query = """
    select distinct ?s where { 
        """ + rel_id + """ :has_source ?s .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    source = response.text.split("\n")[1:]
    source = regex.sub(r"\r", "", source[0])

    if source.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
        source = ":" + \
            source[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]

    return source


def get_target(rel_id):
    """
    Obtains the identifier of the target configuration item of a relationship.

    Parameters
    -------
    rel_id : string
        The identifier of the relationship.

    Returns
    -------
    string
        Returns the identifier of the target configuration item of the relationship.
    """
    query = """
    select distinct ?s where {
        """ + rel_id + """ :has_target ?s .
    }"""
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded
    s = requests.Session()
    response = s.get(url)

    target = response.text.split("\n")[1:]
    target = regex.sub(r"\r", "", target[0])

    if target.startswith("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):
        target = ":" + \
            target[len("http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#"):]

    return target


def run_cmdb_population(db_info, cmdb_info):
    """
    Executes the population of the CMDB, based on its software and the existing objects in the database.

    Parameters
    -------
    db_info : dict
        The information (server address, port number and repository name) about the database.

    cmdb_info : dict
        The information about the CMDB.
    """
    cis_types = {}
    rels_types = {}

    cis_attributes = {}
    rels_attributes = {}

    sources = {}
    targets = {}

    rules = transformation_rules.rules

    print(blue + "\n>>> " + reset +
          "Obtaining the existing CI's in the database...")
    cis_ids = get_cis(db_info)
    for ci in cis_ids:
        cis_types[ci] = get_ci_type(ci)
        cis_attributes[ci] = get_ci_attributes(ci)

    print(blue + "\n>>> " + reset +
          "Obtaining the existing relationships in the database...")
    rels_ids = get_rels(db_info)
    for rel in rels_ids:
        rels_types[rel] = get_rel_type(rel)
        rels_attributes[rel] = get_rel_attributes(rel)
        sources[rel] = get_source(rel)
        targets[rel] = get_target(rel)

    print(blue + "\n>>> " + reset +
          "Starting the population of the CMDB...")

    sw = cmdb_info.get("software")

    if sw == "i-doit":
        success = run_idoit_population(cmdb_info.get("cmdb"), cmdb_data_model.cmdb_data_model, rules, cis_types,
                                       rels_types, cis_attributes, rels_attributes, sources, targets)
        if success:
            print(green + "\n>>> " + reset +
                  "CMDB population completed.")
        else:
            print(red + "\n>>> " + reset +
                  "The CMDB population was not successful...")

    if sw == "iTop":
        success = run_itop_population(cmdb_info.get("cmdb"), cmdb_data_model.cmdb_data_model, rules, cis_types,
                                      rels_types, cis_attributes, rels_attributes, sources, targets)
        if success:
            print(green + "\n>>> " + reset +
                  "CMDB population completed.")
        else:
            print(red + "\n>>> " + reset +
                  "The CMDB population was not successful...")
