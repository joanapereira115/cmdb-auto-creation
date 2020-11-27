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
    if cmdb_type != None:
        cmdb_type_text = "\"type\": \"" + cmdb_type + "\", "
        cmdb_at_text = ""
        has_title = False
        at_types = ci_attributes_data_types.get(cmdb_type)

        for at in ci_attrs:
            cmdb_at = rules_ci_attributes.get(ci_type).get(at)
            value = ci_attrs.get(at)

            if cmdb_type in ci_dialog_attributes:
                if cmdb_at in ci_dialog_attributes.get(cmdb_type):
                    value = calculate_value_from_dialog(
                        value, ci_dialog_attributes.get(cmdb_type).get(cmdb_at))

            at_type = at_types.get(cmdb_at)
            if cmdb_at != None:
                if cmdb_at == "title":
                    has_title = True
                if at_type == "text" or at_type == "text_area" or at_type == "date" or at_type == "date_time" or at_type == "json":
                    cmdb_at_text += "\"" + cmdb_at + "\": \"" + value + "\","
                elif at_type == "int":
                    try:
                        cmdb_at_text += "\"" + str(cmdb_at) + \
                            "\": " + str(int(value)) + ","
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to int.")
                elif at_type == "float" or at_type == "double":
                    try:
                        cmdb_at_text += "\"" + str(cmdb_at) + \
                            "\": " + str(float(value)) + ","
                    except ValueError:
                        print(red + "\n>>> " + reset +
                              "Error converting string '" + str(value) + "' to float.")
            else:
                cmdb_at_text += ""

        if has_title == False:
            cmdb_at_text += "\"title\": \"" + ci_type + "\","
        body = json.loads("""{"version\": \"2.0\",
            \"method\": \"cmdb.object.create\",
            \"params\": {
                """ + cmdb_type_text + cmdb_at_text + """
                \"apikey\": \"""" + apikey + """\",
                \"language\": \"en\"
            },
            \"id\": 1
        }""")

        s = requests.Session()
        create_ci_request = s.post(cmdb_url, json=body, headers=headers)
        create_ci = create_ci_request.json()
        if "error" in create_ci:
            print(red + "\n>>> " + reset +
                  "Error creating the configuration item.")
        if "result" in create_ci:
            success = create_ci.get("result").get("success")
            if success == True:
                print(green + "\n>>> " + reset +
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
    if cmdb_type != None:
        cmdb_type_text = "\"type\": \"C__OBJTYPE__RELATION\", \"relation_type\": \"" + \
            cmdb_type + "\", "

        if ci_ids.get(source) != None and ci_ids.get(target) != None:
            cmdb_source_target_text = "\"object1\": " + \
                str(ci_ids.get(source)) + ", \"object2\": " + \
                str(ci_ids.get(target)) + ", "
            cmdb_at_text = ""

            has_title = False
            at_types = rel_attributes_data_types.get(cmdb_type)

            for at in rel_attrs:
                cmdb_at = rules_rel_attributes.get(rel_type).get(at)
                value = rel_attrs.get(at)

                if cmdb_type in rel_dialog_attributes:
                    if cmdb_at in rel_dialog_attributes.get(cmdb_type):
                        value = calculate_value_from_dialog(
                            value, rel_dialog_attributes.get(cmdb_type).get(cmdb_at))

                at_type = at_types.get(cmdb_at)
                if cmdb_at != None:
                    if cmdb_at == "title":
                        has_title = True
                    if at_type == "text" or at_type == "text_area" or at_type == "date" or at_type == "date_time" or at_type == "json":
                        cmdb_at_text += "\"" + cmdb_at + "\": \"" + value + "\","
                    elif at_type == "int":
                        try:
                            cmdb_at_text += "\"" + str(cmdb_at) + \
                                "\": " + str(int(value)) + ","
                        except ValueError:
                            print(red + "\n>>> " + reset +
                                  "Error converting string '" + str(value) + "' to int.")
                    elif at_type == "float" or at_type == "double":
                        try:
                            cmdb_at_text += "\"" + str(cmdb_at) + \
                                "\": " + str(float(value)) + ","
                        except ValueError:
                            print(red + "\n>>> " + reset +
                                  "Error converting string '" + str(value) + "' to float.")
                else:
                    cmdb_at_text += ""

            if has_title == False:
                cmdb_at_text += "\"title\": \"" + rel_type + "\","

            cmdb_weight_text = "\"weighting\": " + str(5) + ","

            body = json.loads("""{"version\": \"2.0\",
                \"method\": \"cmdb.object.create\",
                \"params\": {
                    """ + str(cmdb_type_text) + str(cmdb_weight_text) + str(cmdb_source_target_text) + str(cmdb_at_text) + """
                    \"apikey\": \"""" + apikey + """\",
                    \"language\": \"en\"
                },
                \"id\": 1
            }""")

            s = requests.Session()
            create_rel_request = s.post(cmdb_url, json=body, headers=headers)
            create_rel = create_rel_request.json()

            if "error" in create_rel:
                print(red + "\n>>> " + reset +
                      "Error creating the relationship.")

            if "result" in create_rel:
                success = create_rel.get("result").get("success")
                if success == True:
                    print(green + "\n>>> " + reset +
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
