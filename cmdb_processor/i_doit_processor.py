# -*- coding: utf-8 -*-

import requests
import json
from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex

from .cmdb_data_model import cmdb_data_model

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
            r'(\d{1,3}\.){3}\d{1,3}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address.',
                cursor_position=len(document.text))  # Move cursor to end


def api_specification():
    """
    Asks the user to enter the necessary information (server address, username, password and api key) to access the i-doit CMDB.

    Returns
    -------
    dict
        The CMDB information (server address, username, password and api key).
    """
    api_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the IP address of your CMDB server (use format yyx.yyx.yyx.yyx where \'y\' is optional):',
            'name': 'server',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter your CMDB username:',
            'name': 'username',
            'validate': NotEmpty
        },
        {
            'type': 'password',
            'message': 'Enter your CMDB password:',
            'name': 'password'
        },
        {
            'type': 'input',
            'message': 'Enter your API key:',
            'name': 'api_key',
            'validate': NotEmpty
        }
    ]
    api_specification_answer = prompt(api_specification_question, style=style)
    return api_specification_answer


def test_api_connection(server, username, password, api_key):
    """
    Tests the access to the CMDB.

    Parameters
    ----------
    server : string
        The IP address of the CMDB server.

    username : string
        The CMDB username.

    password : string
        The CMDB password.

    api_key: string
        The CMDB API key.

    Returns
    -------
    boolean
        Returns true if the connection was successful and false otherwise.
    """
    global api_url
    api_url = "http://" + server + "/i-doit/src/jsonrpc.php"

    global headers
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["X-RPC-Auth-Username"] = username
    headers["X-RPC-Auth-Password"] = password

    global apikey
    apikey = api_key

    print(blue + "\n>>> " + reset + "Checking API connection...")

    login_body = json.loads("{\"version\": \"2.0\",\"method\": \"idoit.login\",\"params\": {\"apikey\": \"" +
                            apikey + "\",\"language\": \"en\"},\"id\": 1}")

    try:
        s = requests.Session()
        login_request = s.post(api_url, json=login_body, headers=headers)
        login = login_request.json()
        if "error" in login:
            print(red + "\n>>> " + reset +
                  "Unable to connect to the API. Please verify the connection information.")
            return False
        else:
            print(green + "\n>>> " + reset + "Successfully connected.")
            return True
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.")
        return False


def api_constants():
    """
    Executes the method 'idoit.contants' of the i-doit API.
    Gets the configuration item types, relationship types, and categories present in the CMDB.

    Returns
    -------
    boolean
        Returns the result of the execution of the method.
    """
    constants_body = json.loads("{\"version\": \"2.0\",\"method\": \"idoit.constants\",\"params\": {\"apikey\": \"" +
                                apikey + "\",\"language\": \"en\"},\"id\": 1}")
    try:
        s = requests.Session()
        constants_request = s.post(
            api_url, json=constants_body, headers=headers)
        constants = constants_request.json()
        return constants.get("result")
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.\n")
        return None


def api_category_info(category):
    """
    Executes the method 'cmdb.category_info' of the i-doit API for a given category.
    Gets the attributes associated with a category, its data types and the available values of the dialog type attributes.

    Parameters
    ----------
    category : string
        The category name.

    Returns
    -------
    dict
        Returns the attributes, its data types and the available values of the dialog type attributes associated with the category.
    """
    res = {}
    attributes = []
    types = {}
    dialogs = {}
    cat_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.category_info\",\"params\": {\"category\": \"" +
                          category + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")

    try:
        s = requests.Session()
        cat_request = s.post(api_url, json=cat_body, headers=headers)
        if cat_request.text != "":
            if "result" in cat_request.json():
                for attr in cat_request.json()["result"]:
                    new_atr = {}
                    new_atr[cat_request.json()["result"][attr]["title"]] = attr
                    types[cat_request.json()["result"][attr]["title"]] = cat_request.json()[
                        "result"][attr]["data"]["type"]
                    dialog = cat_request.json()["result"][attr]["info"]["type"]
                    if dialog == "dialog":
                        d = {}
                        dialog_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.dialog.read\",\"params\": {\"category\": \"" +
                                                 category + "\", \"property\": \"" + attr + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
                        s = requests.Session()
                        dialog_request = s.post(
                            api_url, json=dialog_body, headers=headers)
                        if dialog_request.text != "":
                            values = dialog_request.json().get("result")
                            if values != None:
                                if len(values) == 1:
                                    values = values[0]
                                if values != None:
                                    for a in values:
                                        if type(a) is dict:
                                            value = a.get("id")
                                            name = a.get("title")
                                            d[value] = name
                        if len(d) > 0:
                            dialogs[attr] = d
                    attributes.append(new_atr)
        res["attributes"] = attributes
        res["types"] = types
        res["dialogs"] = dialogs
        return res
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.\n")
        return None


def category_attributes_types(categories):
    """
    Gets the attributes its data types and the available values of the dialog type attributes associated with all the categories in the CMDB.

    Parameters
    ----------
    categories : list
        The category names.

    Returns
    -------
    dict
        Returns the attributes, its data types and the available values of the dialog type attributes associated with all the categories.
    """
    attributes = {}
    for cat in categories:
        attributes[cat] = {}
        category_info = api_category_info(cat)

        attr = {}
        for a in category_info.get("attributes"):
            for key in a:
                attr[key] = a[key]

        attributes[cat]["attributes"] = {k: d for d, k in attr.items()}

        types = category_info.get("types")
        attributes[cat]["types"] = {
            attr.get(a): types.get(a) for a in types}

        attributes[cat]["dialogs"] = category_info.get("dialogs")

    return attributes


def get_object_attributes(ci, cat_attr_types):
    """
    Executes the method 'cmdb.object_type_categories.read' of the i-doit API for a given object type.
    Gets the categories associated with an object type.
    Computes the attributes, its data types and the available values of the dialog type attributes of the object type, based on the categories associated with that type.

    Parameters
    ----------
    ci : string
        The object name.

    cat_attr_types : dict
        The attributes, its data types and the available values of the dialog type attributes, associated with every category, .

    Returns
    -------
    dict
        Returns the attributes, its data types and the available values of the dialog type attributes associated with the object type.
    """
    res = {}
    object_attributes = {}
    attributes_types = {}
    dialogs = {}
    obj_categories_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.object_type_categories.read\",\"params\": {\"type\": \"" +
                                     ci + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
    try:
        s = requests.Session()
        obj_categories_request = s.post(
            api_url, json=obj_categories_body, headers=headers)

        if obj_categories_request.text != "":
            if "result" in obj_categories_request.json():
                if "catg" in obj_categories_request.json()["result"]:
                    for cat_g in obj_categories_request.json()["result"]["catg"]:
                        cat = cat_g["const"]
                        if cat in cat_attr_types:
                            dialogs.update(
                                cat_attr_types.get(cat).get("dialogs"))
                            attrs = cat_attr_types.get(cat).get("attributes")
                            types = cat_attr_types.get(cat).get("types")
                            object_attributes.update(attrs)
                            attributes_types.update(types)
                if "cats" in obj_categories_request.json()["result"]:
                    for cat_s in obj_categories_request.json()["result"]["cats"]:
                        cat = cat_s["const"]
                        if cat in cat_attr_types:
                            dialogs.update(
                                cat_attr_types.get(cat).get("dialogs"))
                            attrs = cat_attr_types.get(cat).get("attributes")
                            types = cat_attr_types.get(cat).get("types")
                            object_attributes.update(attrs)
                            attributes_types.update(types)
        res["dialogs"] = dialogs
        res["attributes"] = object_attributes
        res["types"] = attributes_types
        return res
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to the API. Please verify the connection information.\n")
        return None


def process_i_doit():
    """
    Processes the i-doit CMDB data model, obtaining information about configuration item types, 
    relationship types, configuration items and relationship attributes, restrictions between relationships, 
    data types of attributes, and values for dialog type attributes.

    Returns
    -------
    dict
        Returns the CMDB information (server address, username, password and api key).
    """
    print(blue + "\n>>> " + reset + "Make sure that i-doit is running.")
    api_info = api_specification()

    server = api_info.get("server")
    username = api_info.get("username")
    password = api_info.get("password")
    api_key = api_info.get("api_key")

    connection = test_api_connection(server, username, password, api_key)
    if connection == False:
        return process_i_doit()
    else:
        print(blue + "\n>>> " + reset + "Processing i-doit CMDB data model...")
        constants = api_constants()

        if constants == None:
            process_i_doit()
        else:
            ci_types = constants.get("objectTypes")
            cmdb_data_model["ci_types"] = ci_types
            rel_types = constants.get("relationTypes")
            cmdb_data_model["rel_types"] = rel_types

            categories = [c for c in {
                **constants.get("categories").get("g"), **constants.get("categories").get("s")}]
            cat_attr_types = category_attributes_types(categories)

            ci_attributes_types = {}

            for ci in ci_types:
                attrs = get_object_attributes(ci, cat_attr_types)
                if attrs == None:
                    process_i_doit()
                else:
                    ci_attributes_types[ci] = attrs

            rel_attributes_types = {}

            attrs = get_object_attributes(
                "C__OBJTYPE__RELATION", cat_attr_types)

            if attrs == None:
                process_i_doit()
            else:
                for rel in rel_types:
                    rel_attributes_types[rel] = attrs

            cmdb_data_model["ci_attributes"] = {
                ci: ci_attributes_types[ci]["attributes"] for ci in ci_attributes_types}

            cmdb_data_model["ci_attributes_data_types"] = {
                ci: ci_attributes_types[ci]["types"] for ci in ci_attributes_types}

            cmdb_data_model["ci_dialog_attributes"] = {
                ci: ci_attributes_types[ci]["dialogs"] for ci in ci_attributes_types}

            cmdb_data_model["rel_attributes"] = {
                rel: rel_attributes_types[rel]["attributes"] for rel in rel_attributes_types}

            cmdb_data_model["rel_attributes_data_types"] = {
                rel: rel_attributes_types[rel]["types"] for rel in rel_attributes_types}

    return api_info
