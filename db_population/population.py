# -*- coding: utf-8 -*-

import regex
import os
from colored import fg, attr
from stringcase import snakecase

from models import ConfigurationItem, Relationship, ConfigurationItemType, RelationshipType, Attribute, methods, objects

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def create_file():
    """
    If it doesn't exist, creates the .ttl file that will store the discovered info and the database structure.
    """
    if not os.path.exists('graphdb-import'):
        print(blue + ">>> " + reset + "Creating graphdb-import folder...\n")
        os.makedirs('graphdb-import')
    if not os.path.exists('graphdb-import/cmdb.ttl'):
        print(blue + ">>> " + reset + "Creating cmdb.ttl file...\n")
        f = open('graphdb-import/cmdb.ttl', "x")
        f.close()


def create_structure():
    """
    Writes the database structure to the .ttl file.
    """
    f = open("graphdb-import/cmdb.ttl", "w")
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
    """
    Creates the configuration item type and writes its gathered information to the .ttl file.

    Parameters
    ----------
    obj : ConfigurationItemType
        The configuration item type that is going to be stored.

    Returns
    -------
    string or None
        Returns the configuration item type identifier if its successfully created, and None otherwise.
    """
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = str(regex.sub(r'[()/]', "", obj.get_title()))
        if id_ != "" and title != "":
            f = open("graphdb-import/cmdb.ttl", "a")
            res += ":" + str(snakecase(title)) + str(id_) + \
                " rdf:type :ConfigurationItemType ;\n\t :title \"" + \
                str(title) + "\".\n"
            f.write(res)
            f.close()
            return ":" + str(snakecase(title)) + str(id_)
    else:
        return None


def create_rel_type(obj):
    """
    Creates the relationship type and writes its gathered information to the .ttl file.

    Parameters
    ----------
    obj : RelationshipType
        The relationship type that is going to be stored.

    Returns
    -------
    string or None
        Returns the relationship type identifier if its successfully created, and None otherwise.
    """
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = str(regex.sub(r'[()/]', "", obj.get_title()))
        if id_ != "" and title != "":
            f = open("graphdb-import/cmdb.ttl", "a")
            res += ":" + str(snakecase(title)) + str(id_) + \
                " rdf:type :RelationshipType ;\n\t :title \"" + \
                str(title) + "\".\n"
            f.write(res)
            f.close()
            return ":" + str(snakecase(title)) + str(id_)
    else:
        return None


def create_attribute(obj):
    """
    Creates the attribute and writes its gathered information to the .ttl file.

    Parameters
    ----------
    obj : Attribute
        The attribute that is going to be stored.

    Returns
    -------
    string or None
        Returns the attribute identifier if its successfully created, and None otherwise.
    """
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = str(regex.sub(r'[()/]', "", obj.get_title()))
        value = obj.get_value()

        if id_ != "" and title != "":
            f = open("graphdb-import/cmdb.ttl", "a")
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
    """
    Creates the configuration item and writes its gathered information to the .ttl file.

    Parameters
    ----------
    obj : ConfigurationItem
        The configuration item that is going to be stored.

    ci_types: list
        The list of the correspondent identifiers of the configuration item types.

    Returns
    -------
    string or None
        Returns the configuration item type identifier if its successfully created, and None otherwise.
    """
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = regex.sub(r'[()/]', "", str(obj.get_title()))
        uuid = obj.get_uuid()
        serial_number = obj.get_serial_number()
        description = obj.get_description()
        status = obj.get_status()
        os_family = obj.get_os_family()
        mac_address = obj.get_mac_address()
        ipv4_addresses = obj.get_ipv4_addresses()
        ipv6_addresses = obj.get_ipv6_addresses()
        type_id = obj.get_type()
        attributes = obj.get_attributes()
        if id_ != "" and type_id != "":
            f = open("graphdb-import/cmdb.ttl", "a")
            res += ":" + str(id_) + str(type_id) + str(snakecase(title)) + \
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
            if os_family != "":
                res += ";\n\t :os_family \"" + str(os_family) + "\""
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
            return ":" + str(id_) + str(type_id) + str(snakecase(title))
    else:
        return None


def create_rel(obj, rel_types, ci_ids):
    """
    Creates the relationship and writes its gathered information to the .ttl file.

    Parameters
    ----------
    obj : Relationship
        The relationship that is going to be stored.

    rel_types: list
        The list of the correspondent identifiers of the relationship types.

    ci_ids: list
        The list of the correspondent identifiers of the configuration items already created.

    Returns
    -------
    string or None
        Returns the configuration item type identifier if its successfully created, and None otherwise.
    """
    if obj != None:
        res = ""
        id_ = obj.get_id()
        title = str(regex.sub(r'[()/]', "", obj.get_title()))
        source_id = obj.get_source_id()
        target_id = obj.get_target_id()
        type_id = obj.get_type()
        attributes = obj.get_attributes()

        if id_ != "" and type_id != "":
            f = open("graphdb-import/cmdb.ttl", "a")
            res += ":" + str(id_) + str(type_id) + \
                str(snakecase(title)) + " rdf:type :Relationship "
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
                    res += ";\n\t :has_rel_type " + \
                        str(rel_types.get(type_id))
            res += ".\n"

            f.write(res)
            f.close()
            return ":" + str(id_) + str(type_id) + str(snakecase(title))
    else:
        return None


def parse_discovered():
    """
    Goes through the configuration item and relationship types, and configuration items and relationships created in the discovery.
    """
    f = open("graphdb-import/cmdb.ttl", "a")

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


def run_population():
    """
    Creates the file to store de strucutre and data to populate the database.
    """
    create_file()
    create_structure()
    parse_discovered()
