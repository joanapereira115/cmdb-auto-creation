#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex
import sys
import os
from pprint import pprint
from colored import fg, bg, attr
from elevate import elevate
import getpass
import subprocess
import xml.etree.ElementTree as ET
import requests
from stringcase import snakecase

from models import ConfigurationItem, Relationship, ConfigurationItemType, RelationshipType, Attribute, methods, objects


blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

repository = "http://192.168.1.4:7200/repositories/cmdb"

""" criar ficheiro ttl com a definição das classes, object properties e data properties """


def create_file():
    # TODO: criar no sítio certo
    if not os.path.exists('/Users/Joana/graphdb-import'):
        print("Creating graphdb-import folder...")
        os.makedirs('/Users/Joana/graphdb-import')
    if not os.path.exists('/Users/Joana/graphdb-import/cmdb.ttl'):
        print("Creating cmdb.ttl file...")
        f = open('/Users/Joana/graphdb-import/cmdb.ttl', "x")


def create_structure():
    f = open("/Users/Joana/graphdb-import/cmdb.ttl", "w")
    f.write("""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix : <http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#> .
@base <http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb> .

<http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#> rdf:type owl:Ontology .

#################################################################
#    Classes
#################################################################

###  http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#ConfigurationItem
:ConfigurationItem rdf:type owl:Class ;
    rdfs:label "Configuration Item" ;
    rdfs:comment "Represents an organization's infrastructure component." .

###  http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#Relationship
:Relationship rdf:type owl:Class ;
    rdfs:label "Relationship" ;
    rdfs:comment "Represents the relationship between two organization's infrastructure components." .

###  http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#ConfigurationItemType
:ConfigurationItemType rdf:type owl:Class ;
    rdfs:label "Configuration Item Type" ;
    rdfs:comment "Represents the type of a configuration item." .

###  http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#RelationshipType
:RelationshipType rdf:type owl:Class ;
    rdfs:label "Relationship Type" ;
    rdfs:comment "Represents the type of a relationship." .

###  http://www.semanticweb.org/cmdb_auto_creation/2020/cmdb#Attribute
:Attribute rdf:type owl:Class ;
    rdfs:label "Attribute" ;
    rdfs:comment "Represents an attribute of a configuration item or relationship." .

#################################################################
#    Data Properties
#################################################################

:uuid rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range xsd:string ;
    rdfs:comment "The universally unique identifier (128-bit number) assigned to the item.".

:serial_number rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range xsd:string ;
    rdfs:comment "The manufacturer-allocated number used to identify the item.".

:title rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ,
                :Relationship ,
                :ConfigurationItemType ,
                :RelationshipType ,
                :Attribute ; 
    rdfs:range xsd:string ;
    rdfs:comment "The label by which the item is known.".

:description rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range xsd:string ;
    rdfs:comment "The textual description of the item.".

:cmdb_status rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range xsd:string ;
    rdfs:comment "The current status value for the operational condition of the item.".

:mac_address rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range xsd:string ;
    rdfs:comment "The media access control address assigned to the item.".

:value rdf:type owl:DatatypeProperty ;
    rdfs:domain :Attribute ; 
    rdfs:range xsd:string ;
    rdfs:comment "The value of the attribute.".

:has_ipv4 rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ; 
    rdfs:range xsd:string ;
    rdfs:comment "The associated IPv4 address.".

:has_ipv6 rdf:type owl:DatatypeProperty ;
    rdfs:domain :ConfigurationItem ; 
    rdfs:range xsd:string ;
    rdfs:comment "The associated IPv6 address.".

#################################################################
#    Object Properties
#################################################################

:has_ci_type rdf:type owl:ObjectProperty ;
    rdfs:domain :ConfigurationItem ;
    rdfs:range :ConfigurationItemType .

:has_rel_type rdf:type owl:ObjectProperty ;
    rdfs:domain :Relationship ;
    rdfs:range :RelationshipType .

:has_source rdf:type owl:ObjectProperty ;
    rdfs:domain :Relationship ;
    rdfs:range [rdf:type owl:Restriction;
                owl:onProperty :has_source;
                owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger;
                owl:onClass :ConfigurationItem ] .

:has_target rdf:type owl:ObjectProperty ;
    rdfs:domain :Relationship ;
    rdfs:range [rdf:type owl:Restriction;
                owl:onProperty :has_target;
                owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger;
                owl:onClass :ConfigurationItem ] .

:has_attribute rdf:type owl:ObjectProperty ;
    rdfs:domain :Relationship , 
                :ConfigurationItem ;
    rdfs:range :Attribute .

#################################################################
#    Instances
#################################################################

    """)
    f.close()


def create_ci_type(obj):
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = obj.get_title()
        if id_ != "" and title != "":
            f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")
            res += ":" + str(snakecase(title)) + str(id_) + \
                " rdf:type :ConfigurationItemType ;\n\t :title \"" + \
                str(title) + "\".\n"
            f.write(res)
            f.close()
            return ":" + str(snakecase(title)) + str(id_)
    return None


def create_rel_type(obj):
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = obj.get_title()
        if id_ != "" and title != "":
            f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")
            res += ":" + str(snakecase(title)) + str(id_) + \
                " rdf:type :RelationshipType ;\n\t :title \"" + \
                str(title) + "\".\n"
            f.write(res)
            f.close()
            return ":" + str(snakecase(title)) + str(id_)
    return None


def create_attribute(obj):
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = obj.get_title()
        value = obj.get_value()

        if id_ != "" and title != "":
            f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")
            res += ":" + str(id_) + str(snakecase(title)) + \
                " rdf:type :Attribute ;\n"
            res += "\t :title \"" + str(title) + "\";\n"
            res += "\t :value \"" + str(value) + "\".\n"

            f.write(res)
            f.close()

            return ":" + str(id_) + str(snakecase(title))
    else:
        return None


def create_ci(obj, ci_types):
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = obj.get_title()
        uuid = obj.get_uuid()
        serial_number = obj.get_serial_number()
        description = obj.get_description()
        status = obj.get_status()
        mac_address = obj.get_mac_address()
        ipv4_addresses = obj.get_ipv4_addresses()
        ipv6_addresses = obj.get_ipv6_addresses()
        type_id = obj.get_type()
        attributes = obj.get_attributes()
        if id_ != "" and type_id != "":
            f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")
            res += ":" + str(id_) + str(type_id) + \
                " rdf:type :ConfigurationItem "
            if title != "":
                res += ";\n\t :title \"" + str(title) + "\""
            if uuid != "":
                res += ";\n\t :uuid \"" + str(uuid) + "\""
            if serial_number != "":
                res += ";\n\t :serial_number \"" + str(serial_number) + "\""
            if description != "":
                res += ";\n\t :description \"" + str(description) + "\""
            if status != "":
                res += ";\n\t :cmdb_status \"" + str(status) + "\""
            if mac_address != "":
                res += ";\n\t :mac_address \"" + str(mac_address) + "\""
            for ipv4 in ipv4_addresses:
                res += ";\n\t :has_ipv4 \"" + str(ipv4) + "\""
            for ipv6 in ipv6_addresses:
                res += ";\n\t :has_ipv6 \"" + str(ipv6) + "\""
            for at_id in attributes:
                at = methods.get_attribute_from_id(at_id)
                at_db_id = create_attribute(at)
                if at_db_id != None:
                    res += ";\n\t :has_attribute " + str(at_db_id)
            if type_id in ci_types:
                if ci_types.get(type_id) != None:
                    res += ";\n\t :has_ci_type " + \
                        str(ci_types.get(type_id))
            res += ".\n"

            f.write(res)
            f.close()
            return ":" + str(id_) + str(type_id)
    return None


def create_rel(obj, rel_types, ci_ids):
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = obj.get_title()
        source_id = obj.get_source_id()
        target_id = obj.get_target_id()
        type_id = obj.get_type()
        attributes = obj.get_attributes()

        if id_ != "" and type_id != "":
            f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")
            res += ":" + str(id_) + str(type_id) + " rdf:type :Relationship "
            if title != "":
                res += ";\n\t :title \"" + str(title) + "\""
            if source_id != "":
                if ci_ids.get(source_id) != None:
                    res += ";\n\t :has_source " + \
                        str(ci_ids.get(source_id))
            if target_id != "":
                if ci_ids.get(target_id) != None:
                    res += ";\n\t :has_target " + \
                        str(ci_ids.get(target_id))
            for at_id in attributes:
                at = methods.get_attribute_from_id(at_id)
                at_db_id = create_attribute(at)
                if at_db_id != None:
                    res += ";\n\t :has_attribute " + str(at_db_id)
            if type_id in rel_types:
                if rel_types.get(type_id) != None:
                    res += ";\n\t :has_ci_type " + \
                        str(rel_types.get(type_id))
            res += ".\n"

            f.write(res)
            f.close()
            return ":" + str(id_) + str(type_id)
    return None


def parse_discovered():
    f = open("/Users/Joana/graphdb-import/cmdb.ttl", "a")

    ci_types = {}
    for o in objects.objects.get("configuration_item_types"):
        db_id = create_ci_type(o)
        ci_types[o.get_id()] = db_id
    f.write("\n")

    rel_types = {}
    for o in objects.objects.get("relationship_types"):
        db_id = create_rel_type(o)
        rel_types[o.get_id()] = db_id
    f.write("\n")

    ci_ids = {}
    for o in objects.objects.get("configuration_items"):
        db_id = create_ci(o, ci_types)
        ci_ids[o.get_id()] = db_id
    f.write("\n")

    for o in objects.objects.get("relationships"):
        create_rel(o, rel_types, ci_ids)
    f.write("\n")

    f.close()


def upload_to_graphdb(repository_id):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = '{"fileNames": ["/Users/Joana/graphdb-import/cmdb.ttl"]}'

    # file import to graphdb
    response = requests.post(
        'http://192.168.1.72:7200/rest/data/import/server/' + str(repository_id), headers=headers, data=data)
    print(response.json())


def run_population():
    create_file()
    create_structure()
    parse_discovered()
    upload_to_graphdb('cmdb')


# curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"fileNames": ["cmdb.ttl"]}' 'http://localhost:7200/rest/data/import/server/cmdb_creation'
