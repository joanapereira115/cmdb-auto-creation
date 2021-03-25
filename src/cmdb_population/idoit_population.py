# -*- coding: utf-8 -*-

import requests
from colored import fg, attr
import json

from similarity import similarity

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def idoit_specification(cmdb_info):
    """
    Defines the necessary elements to access the API.

    Parameters
    ----------
    cmdb_info : dict
        The API information (server address, username, password and API key).
    """
    global cmdb_url
    cmdb_url = "http://" + \
        cmdb_info.get("server") + "/i-doit/src/jsonrpc.php"

    global headers
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["X-RPC-Auth-Username"] = cmdb_info.get("username")
    headers["X-RPC-Auth-Password"] = cmdb_info.get("password")

    global apikey
    apikey = cmdb_info.get("api_key")


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


def define_attribute_categories(cmdb_type, attrs):

    categories = []
    categorie_attributes = {}
    obj_categories_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.object_type_categories.read\",\"params\": {\"type\": \"" +
                                     cmdb_type + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")

    try:
        s = requests.Session()
        obj_categories_request = s.post(
            cmdb_url, json=obj_categories_body, headers=headers)

        if obj_categories_request.text != "":
            if "result" in obj_categories_request.json():
                if "catg" in obj_categories_request.json().get("result"):
                    for cat_g in obj_categories_request.json().get("result").get("catg"):
                        cat = cat_g["const"]
                        categories.append(cat)
                if "cats" in obj_categories_request.json().get("result"):
                    for cat_s in obj_categories_request.json().get("result").get("cats"):
                        cat = cat_s["const"]
                        categories.append(cat)

        for cat in categories:
            try:
                categories_attributes_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.category_info\",\"params\": {\"category\": \"" +
                                                        cat + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")

                s = requests.Session()
                categories_attributes_request = s.post(
                    cmdb_url, json=categories_attributes_body, headers=headers)

                if categories_attributes_request.text != "":
                    if "result" in categories_attributes_request.json():
                        for attr in categories_attributes_request.json().get("result"):
                            if attr in attrs:
                                categorie_attributes[attr] = cat

            except requests.exceptions.RequestException:
                print(red + "\n>>> " + reset +
                      "Unable to connect to the API. Please verify the connection information.\n")

        if "title" in categorie_attributes:
            categorie_attributes["title"] = "C__CATG__GLOBAL"

        if "status" in categorie_attributes:
            categorie_attributes["status"] = "C__CATG__GLOBAL"

        if "cmdb_status" in categorie_attributes:
            categorie_attributes["cmdb_status"] = "C__CATG__GLOBAL"

        if "description" in categorie_attributes:
            categorie_attributes["description"] = "C__CATG__GLOBAL"

    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.\n")

    return categorie_attributes


def create_idoit_ci(ci_type, ci_attrs, rules_ci_types, rules_ci_attributes, ci_attributes_data_types, ci_dialog_attributes):
    """
    Creates a configuration item into the CMDB.

    Parameters
    ----------
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
    string
        Returns the identifier of the configuration item in the CMDB.
    """
    cmdb_id = None
    cmdb_type = rules_ci_types.get(ci_type)

    body = {}
    body["version"] = "2.0"
    body["method"] = "cmdb.object.create"
    body["params"] = {}
    body["params"]["apikey"] = apikey
    body["params"]["language"] = "en"
    body["id"] = 1

    if cmdb_type != None:
        body["params"]["type"] = cmdb_type
        body["params"]["title"] = cmdb_type

        at_types = ci_attributes_data_types.get(cmdb_type)
        attrs = [rules_ci_attributes.get(ci_type).get(at) for at in ci_attrs]

        categorie_attributes = define_attribute_categories(cmdb_type, attrs)
        body["params"]["categories"] = {}

        for at in ci_attrs:
            cmdb_at = rules_ci_attributes.get(ci_type).get(at)
            value = ci_attrs.get(at).strip("\"")

            if cmdb_type in ci_dialog_attributes:
                if cmdb_at in ci_dialog_attributes.get(cmdb_type):
                    value = calculate_value_from_dialog(
                        value, ci_dialog_attributes.get(cmdb_type).get(cmdb_at))

            at_type = at_types.get(cmdb_at)
            if cmdb_at != None:
                cat = categorie_attributes.get(cmdb_at)
                if cat not in body["params"]["categories"]:
                    body["params"]["categories"][cat] = [{}]
                if at_type == "text" or at_type == "text_area" or at_type == "date" or at_type == "date_time" or at_type == "json":
                    body["params"]["categories"][cat][0][str(
                        cmdb_at)] = str(value)
                elif at_type == "int":
                    try:
                        body["params"]["categories"][cat][0][str(
                            cmdb_at)] = int(value)
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to int.")
                elif at_type == "float" or at_type == "double":
                    try:
                        body["params"]["categories"][cat][0][str(
                            cmdb_at)] = float(value)
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to float.")

        print()
        print(body)

        s = requests.Session()
        create_ci_request = s.post(cmdb_url, json=body, headers=headers)
        create_ci = create_ci_request.json()
        if "error" in create_ci:
            print(red + "\n>>> " + reset +
                  "Error creating the configuration item.")
        if "result" in create_ci:
            success = create_ci.get("result").get("success")
            if success == True:
                print(green + ">>> " + reset +
                      "Object of type " + str(cmdb_type) + " created successfully in the CMDB.")
                cmdb_id = create_ci.get("result").get("id")

    return cmdb_id


def create_idoit_relationship(rel_type, rel_attrs, rules_rel_types, rules_rel_attributes, ci_ids, source, target, rel_attributes_data_types, rel_dialog_attributes):
    """
    Creates a relationship into the CMDB.

    Parameters
    ----------
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

    source : string
        The source configuration item involved in the relationship.

    target : string
        The target configuration item involved in the relationship.

    rel_attributes_data_types : dict
        The data types of the attributes in the CMDB.

    rel_dialog_attributes : dict
        The values of the dialog attributes in the CMDB.

    Returns
    -------
    string
        Returns the identifier of the relationship in the CMDB.
    """

    cmdb_id = None
    cmdb_type = rules_rel_types.get(rel_type)

    body = {}
    body["version"] = "2.0"
    body["method"] = "cmdb.object.create"
    body["params"] = {}
    body["params"]["apikey"] = apikey
    body["params"]["language"] = "en"
    body["id"] = 1

    if cmdb_type != None:
        body["params"]["type"] = "C__OBJTYPE__RELATION"
        body["params"]["title"] = cmdb_type
        body["params"]["categories"] = {}
        body["params"]["categories"]["C__CATG__RELATION"] = [{}]
        body["params"]["categories"]["C__CATG__RELATION"][0]["relation_type"] = cmdb_type

        if ci_ids.get(source) != None and ci_ids.get(target) != None:
            body["params"]["categories"]["C__CATG__RELATION"][0]["object1"] = int(
                ci_ids.get(source))
            body["params"]["categories"]["C__CATG__RELATION"][0]["object2"] = int(
                ci_ids.get(target))

            at_types = rel_attributes_data_types.get(cmdb_type)
            attrs = [rules_rel_attributes.get(
                rel_type).get(at) for at in rel_attrs]

            categorie_attributes = define_attribute_categories(
                cmdb_type, attrs)

            for at in rel_attrs:
                cmdb_at = rules_rel_attributes.get(rel_type).get(at)
                value = rel_attrs.get(at).strip("\"")

                if cmdb_type in rel_dialog_attributes:
                    if cmdb_at in rel_dialog_attributes.get(cmdb_type):
                        value = calculate_value_from_dialog(
                            value, rel_dialog_attributes.get(cmdb_type).get(cmdb_at))

                at_type = at_types.get(cmdb_at)
                if cmdb_at != None:
                    cat = categorie_attributes.get(cmdb_at)
                    if cat not in body["params"]["categories"]:
                        body["params"]["categories"][cat] = [{}]
                    if at_type == "text" or at_type == "text_area" or at_type == "date" or at_type == "date_time" or at_type == "json":
                        body["params"]["categories"][cat][0][str(
                            cmdb_at)] = str(value)
                    elif at_type == "int":
                        try:
                            body["params"]["categories"][cat][0][str(
                                cmdb_at)] = int(value)
                        except ValueError:
                            print(red + "\n>>> " + reset +
                                  "Error converting string '" + str(value) + "' to int.")
                    elif at_type == "float" or at_type == "double":
                        try:
                            body["params"]["categories"][cat][0][str(
                                cmdb_at)] = float(value)
                        except ValueError:
                            print(red + "\n>>> " + reset +
                                  "Error converting string '" + str(value) + "' to float.")

            body["params"]["categories"]["C__CATG__RELATION"][0]["weighting"] = 5

            print()
            print(body)

            s = requests.Session()
            create_rel_request = s.post(cmdb_url, json=body, headers=headers)
            create_rel = create_rel_request.json()

            if "error" in create_rel:
                print(red + "\n>>> " + reset +
                      "Error creating the relationship.")

            if "result" in create_rel:
                success = create_rel.get("result").get("success")
                if success == True:
                    print(green + ">>> " + reset +
                          "Object of type " + str(cmdb_type) + " created successfully in the CMDB.")
                    cmdb_id = create_rel.get("result").get("id")

    return cmdb_id


def logout():
    """
    Closes the current session.

    Returns
    -------
    boolean
        Returns true if the disconnection was successfull, and false otherwise.
    """
    body = json.loads(
        "{\"version\": \"2.0\",\"method\": \"idoit.logout\",\"params\": {\"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 3}")
    try:
        s = requests.Session()
        logout_request = s.post(cmdb_url, json=body, headers=headers)
        logout = logout_request.json()
        if "error" in logout:
            print(red + "\n>>> " + reset +
                  "Unable to disconnect to the API.")
            return False
        else:
            print(green + "\n>>> " + reset + "Successfully disconnected.")
            return True
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to disconnect to the API.")
        return False


def run_idoit_population(cmdb_info, cmdb_data_model, rules, cis_types, rels_types, cis_attributes, rels_attributes, sources, targets):
    """
    Executes the population in the i-doit CMDB.

    Parameters
    ----------
    cmdb_info : dict
        The API information (server address, username, password and API key).

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
    idoit_specification(cmdb_info)
    ids = {}
    ci_attributes_data_types = cmdb_data_model.get("ci_attributes_data_types")
    rel_attributes_data_types = cmdb_data_model.get(
        "rel_attributes_data_types")
    ci_dialog_attributes = cmdb_data_model.get("ci_dialog_attributes")
    rel_dialog_attributes = cmdb_data_model.get("rel_dialog_attributes")

    print(blue + "\n>>> " + reset +
          "Creating the configuration items...")
    for ci in cis_types:
        id_ci = create_idoit_ci(cis_types.get(ci), cis_attributes.get(
            ci), rules.get("ci_types"), rules.get("ci_attributes"), ci_attributes_data_types, ci_dialog_attributes)
        if id_ci != None:
            ids[ci] = id_ci

    print(blue + "\n>>> " + reset +
          "Creating the relationships...")
    for rel in rels_types:
        rel_id = create_idoit_relationship(rels_types.get(
            rel), rels_attributes.get(rel), rules.get("rel_types"), rules.get("rel_attributes"), ids, sources.get(rel), targets.get(rel), rel_attributes_data_types, rel_dialog_attributes)

    out = logout()

    return out
