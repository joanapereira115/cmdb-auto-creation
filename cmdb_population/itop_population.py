# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
import json
import stringcase

from similarity import similarity

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
            r'(\d{1,3}\.){3}\d{1,3}(/.*)*', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address.',
                cursor_position=len(document.text))  # Move cursor to end


def api_specification():
    """
    Asks the user to enter the necessary information (server address, username and password) to access the iTop CMDB.

    Returns
    -------
    dict
        The CMDB information (server address, username and password).

    """
    print()
    api_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the url of your iTop CMDB server:',
            'name': 'url',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter your iTop username:',
            'name': 'username',
            'validate': NotEmpty
        },
        {
            'type': 'password',
            'message': 'Enter your iTop password:',
            'name': 'password'
        }
    ]
    api_specification_answer = prompt(api_specification_question, style=style)
    return api_specification_answer


def itop_specification(cmdb_info):
    cmdb_url = "http://" + str(cmdb_info.get("url")) + \
        "/webservices/rest.php?version=1.3"

    user = str(cmdb_info.get("username"))
    pwd = str(cmdb_info.get("password"))

    json_req = {'operation': "core/check_credentials"}
    json_req["user"] = user
    json_req["password"] = pwd
    json_data = json.dumps(json_req)
    payload = dict(json_data=json_data,)

    test = requests.post(cmdb_url, data=payload, auth=(
        user, pwd), verify=False)

    auth = False
    try:
        auth = test.json().get("authorized")
    except:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.\n")
    if auth == True:
        print(green + "\n>>> " + reset + "Successfully connected.\n")

    return cmdb_url


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


def create_itop_ci(cmdb_info, cmdb_url, ci_type, ci_attrs, rules_ci_types, rules_ci_attributes, ci_attributes_data_types, ci_dialog_attributes):
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
        json_req["class"] = stringcase.capitalcase(cmdb_type)

        at_types = ci_attributes_data_types.get(cmdb_type)
        fields = {}
        fields["org_id"] = 'SELECT Organization WHERE name = \"My Company/Department\"'

        for at in ci_attrs:
            cmdb_at = rules_ci_attributes.get(ci_type).get(at)
            value = ci_attrs.get(at)

            if cmdb_type in ci_dialog_attributes:
                if cmdb_at in ci_dialog_attributes.get(cmdb_type):
                    value = calculate_value_from_dialog(
                        value, ci_dialog_attributes.get(cmdb_type).get(cmdb_at))

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
            fields["name"] = ci_type

        if cmdb_type == "person":
            if ('first_name' in fields) == False:
                fields["first_name"] = ci_type

        json_req["fields"] = fields
        json_data = json.dumps(json_req)
        payload = dict(json_data=json_data,)
        create_ci = requests.post(cmdb_url, data=payload, auth=(
            user, pwd), verify=False)
        try:
            cmdb_id = create_ci.json().get("objects").get(
                list(create_ci.json().get("objects").keys())[0]).get("key")
        except:
            print(red + "\n>>> " + reset +
                  "Error creating the configuration item of type " + str(cmdb_type) + ": " + str(create_ci.json().get("message")))
    if cmdb_id != None:
        print(green + "\n>>> " + reset + "Object of type " +
              str(cmdb_type) + " created successfully in the CMDB.")
    return cmdb_id, cmdb_type


"""
"lnkphysicalinterfacetovlan": {
        "physicalinterface_id": "physicalinterface",
        "vlan_id": "vlan"
    },
"""


def create_itop_relationship(cmdb_info, cmdb_url, rel_type, rel_attrs, rules_rel_types, rules_rel_attributes, ci_ids, ci_types, source, target, rel_attributes_data_types, rel_dialog_attributes, rel_restrictions):
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
        json_req["class"] = stringcase.capitalcase(cmdb_type)

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
                    json_data = json.dumps(json_req)
                    print("json_data: " + str(json_data))
                    print()
                    payload = dict(json_data=json_data,)
                    create_ci = requests.post(cmdb_url, data=payload, auth=(
                        user, pwd), verify=False)
                    try:
                        cmdb_id = create_ci.json().get("objects").get(
                            list(create_ci.json().get("objects").keys())[0]).get("key")
                    except:
                        print(red + "\n>>> " + reset +
                              "Error creating the configuration item of type " + str(cmdb_type) + ": " + str(create_ci.json().get("message")))

                if cmdb_id != None:
                    print(green + "\n>>> " + reset + "Object of type " +
                          str(cmdb_type) + " created successfully in the CMDB.")

    return cmdb_id


def run_itop_population(cmdb_data_model, rules, cis_types, rels_types, cis_attributes, rels_attributes, sources, targets):
    cmdb_info = api_specification()
    cmdb_url = itop_specification(cmdb_info)

    ids = {}  # id bd : id cmdb
    types = {}  # id bd : id cmdb
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
        id_ci, type_ci = create_itop_ci(cmdb_info, cmdb_url, cis_types.get(ci), cis_attributes.get(
            ci), rules.get("ci_types"), rules.get("ci_attributes"), ci_attributes_data_types, ci_dialog_attributes)
        if id_ci != None:
            ids[ci] = id_ci
        if type_ci != None:
            types[ci] = type_ci

    print(blue + "\n>>> " + reset +
          "Creating the relationships...")
    for rel in rels_types:
        rel_id = create_itop_relationship(cmdb_info, cmdb_url, rels_types.get(
            rel), rels_attributes.get(rel), rules.get("rel_types"), rules.get("rel_attributes"), ids, types, sources.get(rel), targets.get(rel), rel_attributes_data_types, rel_dialog_attributes, rel_restrictions)

    return True
