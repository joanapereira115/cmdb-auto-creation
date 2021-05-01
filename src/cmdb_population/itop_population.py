# -*- coding: utf-8 -*-

import requests
from colored import fg, attr
import json
import stringcase
import wordninja
import re

from similarity import similarity
from cmdb_processor import cmdb_data_model

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def calculate_value_from_dialog(original_value, dialog_values):
    """
    Calculates the most similar value of a dialog attribute based on the discovered value.

    Parameters
    ----------
    original_value : string
        The discovered value.

    dialog_values : dict
        The values available for the attribute.

    Returns
    -------
    string, string
        Returns the most similar value for the attribute.
    """
    mx = 0
    res = None
    for pv in dialog_values:
        sim = similarity.calculate_similarity(
            original_value, dialog_values.get(pv))
        if sim > mx:
            res = pv
            mx = sim
    return res


def hasOrgId(cmdb_type):
    attrs = cmdb_data_model.cmdb_data_model.get("ci_attributes").get(cmdb_type)
    if "org_id" in attrs:
        return True
    else:
        return False


def create_itop_ci(cmdb_info, cmdb_url, ci_type, ci_attrs, rules_ci_types, rules_ci_attributes, ci_attributes_data_types, ci_dialog_attributes):
    """
    Creates a configuration item into the CMDB.

    Parameters
    ----------
    cmdb_info : dict
        The API information (server address, username and password).

    cmdb_url : string
        The url to access the API.

    ci_type : string
        The type of the configuration item in the database.

    ci_attrs : dict
        The attributes of configuration item.

    rules_ci_types : dict
        The transformation rules to the types of the configuration items.

    rules_ci_attributes : dict
        The transformation rules to the attributes of the configuration items.

    ci_attributes_data_types : dict
        The data types of the attributes in the CMDB.

    ci_dialog_attributes : dict
        The values of the dialog attributes in the CMDB.

    Returns
    -------
    string, string
        Returns the identifier of the configuration item in the CMDB, and its type.
    """
    cmdb_id = None
    cmdb_type = rules_ci_types.get(ci_type)

    user = str(cmdb_info.get("username"))
    pwd = str(cmdb_info.get("password"))

    json_req = {}
    json_req['operation'] = "core/create"
    json_req['comment'] = "Synchronization from CMDB automatic creation..."
    json_req["user"] = user
    json_req["password"] = pwd

    if cmdb_type != None:
        json_req["class"] = re.sub(r' ', "", stringcase.titlecase(
            " ".join(wordninja.split(cmdb_type))))

        at_types = ci_attributes_data_types.get(cmdb_type)
        fields = {}

        has_org = hasOrgId(cmdb_type)
        if has_org == True:
            fields["org_id"] = 'SELECT Organization WHERE name = "My Company/Department"'

        for at in ci_attrs:
            cmdb_at = rules_ci_attributes.get(ci_type).get(at)
            value = ci_attrs.get(at)

            if cmdb_type in ci_dialog_attributes:
                if cmdb_at in ci_dialog_attributes.get(cmdb_type):
                    value = calculate_value_from_dialog(
                        value, ci_dialog_attributes.get(cmdb_type).get(cmdb_at))

            at_type = at_types.get(cmdb_type).get(cmdb_at)
            if cmdb_at != None:

                if at_type == "string":
                    fields[str(cmdb_at)] = str(value)

                elif at_type == "int":
                    try:
                        fields[str(cmdb_at)] = str(int(value))
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to int.")

                elif at_type == "float":
                    try:
                        fields[str(cmdb_at)] = str(float(value))
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to float.")

        if ("name" in fields) == False:
            title = ci_attrs.get("title")
            if title != None:
                fields["name"] = title
            else:
                fields["name"] = ci_type

        if cmdb_type == "person":
            if ('first_name' in fields) == False:
                fields["first_name"] = ci_type

        json_req["fields"] = fields

        print()
        print(json_req)

        json_data = json.dumps(json_req)
        payload = dict(json_data=json_data,)
        create_ci = requests.post(cmdb_url, data=payload, auth=(
            user, pwd), verify=False)
        if create_ci.status_code == 200:
            error = create_ci.json().get("message")
            if error != None:
                if re.search(r'Unexpected value for attribute \'org_id\'', error, re.IGNORECASE) != None:
                    fields["org_id"] = 'SELECT Organization WHERE name = "My Company/Department"'
                    json_req["fields"] = fields
                    json_data = json.dumps(json_req)
                    payload = dict(json_data=json_data,)
                    create_ci = requests.post(
                        cmdb_url, data=payload, auth=(user, pwd), verify=False)
                    if create_ci.status_code == 200:
                        try:
                            cmdb_id = create_ci.json().get("objects").get(
                                list(create_ci.json().get("objects").keys())[0]).get("key")
                        except:
                            print(red + "\n>>> " + reset + "Error creating the configuration item of type " +
                                  str(cmdb_type) + ": " + str(create_ci.json().get("message")))
                    else:
                        print(red + "\n>>> " + reset +
                              "Error creating the configuration item of type " + str(cmdb_type) + ".")

            try:
                cmdb_id = create_ci.json().get("objects").get(
                    list(create_ci.json().get("objects").keys())[0]).get("key")
            except:
                print(red + "\n>>> " + reset + "Error creating the configuration item of type " +
                      str(cmdb_type) + ": " + str(create_ci.json().get("message")))
        else:
            print(red + "\n>>> " + reset +
                  "Error creating the configuration item of type " + str(cmdb_type) + ".")
    if cmdb_id != None:
        print(green + "\n>>> " + reset + "Object of type " +
              str(cmdb_type) + " created successfully in the CMDB.")
    return cmdb_id, cmdb_type


def create_itop_relationship(cmdb_info, cmdb_url, rel_type, rel_attrs, rules_rel_types, rules_rel_attributes, ci_ids, ci_types, source, target, rel_attributes_data_types, rel_dialog_attributes, rel_restrictions):
    """
    Creates a relationship into the CMDB.

    Parameters
    ----------
    cmdb_info : dict
        The API information (server address, username and password).

    cmdb_url : string
        The url to access the API.

    rel_type : string
        The type of the relationship in the database.

    rel_attrs : dict
        The attributes of relationship.

    rules_rel_types : dict
        The transformation rules to the types of the relationships.

    rules_rel_attributes : dict
        The transformation rules to the attributes of the relationships.

    ci_ids : dict
        The identifiers of the configuration items in the CMDB.

    ci_types : dict
        The identifiers of the configuration items in the CMDB.

    source : string
        The source configuration item involved in the relationship.

    target : string
        The target configuration item involved in the relationship.

    rel_attributes_data_types : dict
        The data types of the attributes in the CMDB.

    rel_dialog_attributes : dict
        The values of the dialog attributes in the CMDB.

    rel_restrictions : dict
        The types restrictions of the configuration items involved in the relationship.

    Returns
    -------
    string
        Returns the identifier of the relationship in the CMDB.
    """
    cmdb_id = None
    cmdb_type = rules_rel_types.get(rel_type)

    user = str(cmdb_info.get("username"))
    pwd = str(cmdb_info.get("password"))

    json_req = {}
    json_req['operation'] = "core/create"
    json_req['comment'] = "Synchronization from CMDB automatic creation..."
    json_req["user"] = user
    json_req["password"] = pwd

    if cmdb_type != None:
        json_req["class"] = re.sub(r' ', "", stringcase.titlecase(
            " ".join(wordninja.split(cmdb_type))))

        at_types = rel_attributes_data_types.get(cmdb_type)

        fields = {}
        fields["org_id"] = 'SELECT Organization WHERE name = \"My Company/Department\"'

        if (cmdb_type in rel_restrictions) == True:
            if ci_ids.get(source) != None and ci_ids.get(target) != None:
                source_type = ci_types.get(source)
                target_type = ci_types.get(target)
                restrictions = {x: y for y,
                                x in rel_restrictions.get(cmdb_type).items()}
                if source_type in restrictions and target_type in restrictions:
                    fields[restrictions.get(source_type)] = ci_ids.get(source)
                    fields[restrictions.get(target_type)] = ci_ids.get(target)

                    for at in rel_attrs:
                        cmdb_at = rules_rel_attributes.get(rel_type).get(at)
                        value = rel_attrs.get(at)

                        if cmdb_type in rel_dialog_attributes:
                            if cmdb_at in rel_dialog_attributes.get(cmdb_type):
                                value = calculate_value_from_dialog(
                                    value, rel_dialog_attributes.get(cmdb_type).get(cmdb_at))

                        at_type = at_types.get(cmdb_at)
                        if cmdb_at != None:
                            if at_type == "string":
                                fields[str(cmdb_at)] = str(value)

                            elif at_type == "int":
                                try:
                                    fields[str(cmdb_at)] = str(int(value))
                                except ValueError:
                                    print(red + "\n>>> " + reset +
                                          "Error converting string '" + str(value) + "' to int.")

                            elif at_type == "float":
                                try:
                                    fields[str(cmdb_at)] = str(float(value))
                                except ValueError:
                                    print(red + "\n>>> " + reset +
                                          "Error converting string '" + str(value) + "' to float.")

                    if ("name" in fields) == False:
                        fields["name"] = cmdb_type

                    json_req["fields"] = fields

                    print()
                    print(json_req)

                    json_data = json.dumps(json_req)
                    payload = dict(json_data=json_data,)
                    create_ci = requests.post(cmdb_url, data=payload, auth=(
                        user, pwd), verify=False)
                    if create_ci.status_code == 200:
                        try:
                            cmdb_id = create_ci.json().get("objects").get(
                                list(create_ci.json().get("objects").keys())[0]).get("key")
                        except:
                            print(red + "\n>>> " + reset +
                                  "Error creating the configuration item of type " + str(cmdb_type) + ": " + str(create_ci.json().get("message")))
                    else:
                        print(red + "\n>>> " + reset +
                              "Error creating the relationship of type " + str(cmdb_type) + ".")
                if cmdb_id != None:
                    print(green + "\n>>> " + reset + "Object of type " +
                          str(cmdb_type) + " created successfully in the CMDB.")

    return cmdb_id


def run_itop_population(cmdb_info, cmdb_data_model, rules, cis_types, rels_types, cis_attributes, rels_attributes, sources, targets):
    """
    Executes the population in the iTop CMDB.

    Parameters
    ----------
    cmdb_info : dict
        The API information (server address, username and password).

    cmdb_data_model : dict
        The CMDB data model.

    rules : dict
        The transformation rules between the two models.

    cis_types : dict
        The types of configuration items.

    rels_types : dict
        The types of relationships.

    cis_attributes : dict
        The attributes of configuration items.

    rels_attributes : dict  
        The attributes of relationships.

    sources : dict
        The configuration item sources of the relationships.

    targets : dict
        The configuration item targets of the relationships.

    Returns
    -------
    boolean
        Returns true if the population was successfully executed, and false otherwise.
    """
    cmdb_url = "http://" + str(cmdb_info.get("url")) + \
        "/webservices/rest.php?version=1.3"

    ids = {}
    types = {}
    ci_attributes_data_types = cmdb_data_model.get("ci_attributes_data_types")
    rel_attributes_data_types = cmdb_data_model.get(
        "rel_attributes_data_types")
    rel_restrictions = cmdb_data_model.get("rel_restrictions")
    ci_dialog_attributes = cmdb_data_model.get("ci_dialog_attributes")
    rel_dialog_attributes = cmdb_data_model.get("rel_dialog_attributes")

    print(blue + "\n>>> " + reset +
          "Creating the configuration items...")
    for ci in cis_types:
        id_ci, type_ci = create_itop_ci(cmdb_info, cmdb_url, cis_types.get(ci), cis_attributes.get(
            ci), rules.get("ci_types"), rules.get("ci_attributes"), ci_attributes_data_types, ci_dialog_attributes)
        if id_ci != None:
            ids[ci] = id_ci
        if type_ci != None:
            types[ci] = type_ci

    print(blue + "\n>>> " + reset +
          "Creating the relationships...")
    for rel in rels_types:
        _ = create_itop_relationship(cmdb_info, cmdb_url, rels_types.get(
            rel), rels_attributes.get(rel), rules.get("rel_types"), rules.get("rel_attributes"), ids, types, sources.get(rel), targets.get(rel), rel_attributes_data_types, rel_dialog_attributes, rel_restrictions)

    return True
