# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
from colored import fg, bg, attr
import regex
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
    cmdb_id = None
    cmdb_type = rules_rel_types.get(rel_type)
    if cmdb_type != None:
        cmdb_type_text = "\"type\": \"" + cmdb_type + "\", "

        if source != None and target != None:
            cmdb_source_target_text = "\"object1\": \"" + \
                str(ci_ids.get(source)) + "\", \"object2\": \"" + \
                str(ci_ids.get(target)) + "\", "
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
                    """ + cmdb_type_text + cmdb_weight_text + cmdb_source_target_text + cmdb_at_text + """
                    \"apikey\": \"""" + apikey + """\",
                    \"language\": \"en\"
                },
                \"id\": 1
            }""")

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
                    print(green + "\n>>> " + reset +
                          "Object of type " + str(cmdb_type) + " created successfully in the CMDB.")
                    cmdb_id = create_rel.get("result").get("id")

    return cmdb_id


def run_idoit_population(cmdb_info, cmdb_data_model, rules, cis_types, rels_types, cis_attributes, rels_attributes, sources, targets):
    idoit_specification(cmdb_info)
    ids = {}  # id bd : id cmdb
    # {"CI type": {"attribute": "data type", ...}, ...}
    ci_attributes_data_types = cmdb_data_model.get("ci_attributes_data_types")
    # {"relationship type": {"attribute": "data type", ...}, ...}
    rel_attributes_data_types = cmdb_data_model.get(
        "rel_attributes_data_types")
    # {"relationship type": [{"source CI attribute": "CI type", "target CI attribute": "CI type"}, ...], ...}
    rel_restrictions = cmdb_data_model.get("rel_restrictions")
    # {"CI type": {"attribute": {"value", "description", ...}, ...}, ...}
    ci_dialog_attributes = cmdb_data_model.get("ci_dialog_attributes")
    # {"relationship type": {"attribute": {"value", "description", ...}, ...}, ...}
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

    return True

    # TODO: devo fazer o logout?
