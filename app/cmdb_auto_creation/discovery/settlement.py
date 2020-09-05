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

from models import Element, Relation, get_name_from_id
from objects import objects
from passwd_vault import vault
from reconciliation import reconcile
from normalization import normalize
from nmap_discovery import parse_nmap_results


blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

repository = "http://192.168.1.4:7200/repositories/cmdb_creation"

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
    f = open("cmdb.ttl", "w")
    f.write("""
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix : <http://www.semanticweb.org/joana/ontologies/2020/cmdb#> .
    @base <http://www.semanticweb.org/joana/ontologies/2020/cmdb> .

    <http://www.semanticweb.org/joana/ontologies/2020/cmdb#> rdf:type owl:Ontology .

    #################################################################
    #    Classes
    #################################################################

    ###  http://www.semanticweb.org/joana/ontologies/2020/cmdb#Element
    :Element rdf:type owl:Class ;
        rdfs:label "Element" ;
        rdfs:comment "Abstract element that is part of the IT infrastructure." .

    ###  http://www.semanticweb.org/joana/ontologies/2020/cmdb#Relationship
    :Relationship rdf:type owl:Class ;
        rdfs:label "Relationship" ;
        rdfs:comment "Relationship between two elements." .

    #################################################################
    #    Data Properties
    #################################################################

    :rel_type rdf:type owl:DatatypeProperty ;
        rdfs:domain :Relationship ;
        rdfs:range xsd:string .

    :ci_type rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :name rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :value rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :status rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :description rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :generation rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :install_date rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :availability rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :serial_number rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :version rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :model rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :manufacturer rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :number rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :hostname rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :management_address rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :connectivity_status rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :net_mask rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :net_number rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :type rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :size rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :layout rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :bandwidth rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :height rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :width rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :speed rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :resolution rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :business_category rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :email rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :fax rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :mobile_phone rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :department rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :title rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :webpage rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :core_number rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :architecture rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :family rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :power rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :ip_range rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :capacity rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :removable rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :block_size rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :number_of_blocks rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :compression_method rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :transfer_rate rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :address rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string . 

    :city rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string . 

    :price rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :available_space rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :max_number_of_processes rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :author rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :filename rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :date rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :path rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .

    :provider rdf:type owl:DatatypeProperty ;
        rdfs:domain :Element ;
        rdfs:range xsd:string .


    #################################################################
    #    Object Properties
    #################################################################

    :source rdf:type owl:ObjectProperty ;
        rdfs:domain :Relationship ;
        rdfs:range :Element .

    :target rdf:type owl:ObjectProperty ;
        rdfs:domain :Relationship ;
        rdfs:range :Element .

    #################################################################
    #    Instances
    #################################################################

    """)
    f.close()


def create_element(object):
    f = open("cmdb.ttl", "a")
    res = ""
    if object.id != "" and object.ci_type != "":
        res += ":" + str(object.id) + str(object.ci_type) + \
            " rdf:type :Element .\n"
    f.write(res)
    f.close()


def create_relation(obj):
    f = open("cmdb.ttl", "a")
    res = ""
    if obj.rel_type != "" and obj.source_id != "" and obj.target_id != "":
        res += ":" + str(obj.rel_type) + \
            str(obj.source_id) + str(obj.target_id) + \
            " rdf:type :Relationship .\n"

        res += ":" + str(obj.rel_type) + str(obj.source_id) + str(obj.target_id) + \
            " :source :" + str(obj.source_id) + str(obj.source_type) + " .\n"
        res += ":" + str(obj.rel_type) + str(obj.source_id) + str(obj.target_id) + \
            " :target :" + str(obj.target_id) + str(obj.target_type) + " .\n"
        #source_name = get_name_from_id(obj.source_id)
        # if source_name != "":
        #    res += ":" + str(obj.rel_type) + str(obj.source_id) + str(
        #        obj.target_id) + " :source :" + str(obj.source_id) + str(source_name) + " .\n"

        #target_name = get_name_from_id(obj.target_id)
        # if target_name != "":
        #    res += ":" + str(obj.rel_type) + str(obj.target_id) + str(
        #        obj.target_id) + " :target :" + str(obj.target_id) + str(target_name) + " .\n"
    f.write(res)
    f.close()


def parse_discovered():
    for o in objects:
        if type(o) is Element:
            create_element(o)
        if type(o) is Relation:
            create_relation(o)


def upload_to_graphdb(repository_id):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = '{"fileNames": ["cmdb.ttl"]}'

    # file import to graphdb
    response = requests.post(
        'http://localhost:7200/rest/data/import/server/' + str(repository_id), headers=headers, data=data)
    print(response.json())


# create_file()
# parse_nmap_results()
# create_structure()
# parse_discovered()
upload_to_graphdb('cmdb_creation')


# curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"fileNames": ["cmdb.ttl"]}' 'http://localhost:7200/rest/data/import/server/cmdb_creation'
