#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

from .cmdb_data_model import data_model


def api_constants():
    constants_body = json.loads("{\"version\": \"2.0\",\"method\": \"idoit.constants\",\"params\": {\"apikey\": \"" +
                                apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    constants_request = s.post(api_url, json=constants_body, headers=headers)
    constants = constants_request.json()
    return constants


def api_category_info(category):
    res = {}
    attributes = []
    types = {}
    cat_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.category_info\",\"params\": {\"category\": \"" +
                          category + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    cat_request = s.post(api_url, json=cat_body, headers=headers)
    if cat_request.text != "":
        if "result" in cat_request.json():
            for attr in cat_request.json()["result"]:
                new_atr = {}
                new_atr[cat_request.json()["result"][attr]["title"]] = attr
                types[cat_request.json()["result"][attr]["title"]] = cat_request.json()[
                    "result"][attr]["data"]["type"]
                attributes.append(new_atr)

    res["attributes"] = attributes
    res["types"] = types
    return res


def api_obj_types():
    obj_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.object_types\",\"params\": {\"apikey\": \"" +
                          apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    obj_request = s.post(api_url, json=obj_body, headers=headers)
    obj_types = {}
    for obj in obj_request.json()["result"]:
        obj_types[obj["const"]] = obj["id"]
    return obj_types

# TODO: C__CATG__RELATION para obter os atributos dos relacionamentos


def get_object_attributes(id, category_attributes, category_attr_types):
    res = {}
    object_attributes = {}
    attributes_types = {}
    obj_categories_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.object_type_categories.read\",\"params\": {\"id\": \"" +
                                     id + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    obj_categories_request = s.post(
        api_url, json=obj_categories_body, headers=headers)

    if obj_categories_request.text != "":
        if "result" in obj_categories_request.json():
            if "catg" in obj_categories_request.json()["result"]:
                for cat_g in obj_categories_request.json()["result"]["catg"]:
                    cat = cat_g["const"]
                    if cat in category_attributes:
                        ats = category_attr_types.get(cat)
                        for at in category_attributes[cat]:
                            at_key = list(at.keys())[0]
                            attributes_types[at_key] = ats.get(at_key)
                            object_attributes.update(at)

            if "cats" in obj_categories_request.json()["result"]:
                for cat_s in obj_categories_request.json()["result"]["cats"]:
                    cat = cat_s["const"]
                    if cat in category_attributes:
                        ats = category_attr_types.get(cat)
                        for at in category_attributes[cat]:
                            at_key = list(at.keys())[0]
                            attributes_types[at_key] = ats.get(at_key)
                            object_attributes.update(at)
                            # object_attributes.extend(category_attributes[cat])

    res["attributes_types"] = attributes_types
    res["object_attributes"] = object_attributes
    return res


def get_relation_attributes(category_attributes):
    rel_attributes = {}
    rel_categories_body = json.loads(
        "{\"version\": \"2.0\",\"method\": \"cmdb.object_type_categories.read\",\"params\": {\"type\": \"C__OBJTYPE__RELATION\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    rel_category_request = s.post(
        api_url, json=rel_categories_body, headers=headers)

    if rel_category_request.text != "":
        if "result" in rel_category_request.json():
            if "catg" in rel_category_request.json()["result"]:
                for cat_g in rel_category_request.json()["result"]["catg"]:
                    cat = cat_g["const"]
                    if cat in category_attributes:
                        for at in category_attributes[cat]:
                            rel_attributes.update(at)
            if "cats" in rel_category_request.json()["result"]:
                for cat_s in rel_category_request.json()["result"]["cats"]:
                    cat = cat_s["const"]
                    if cat in category_attributes:
                        for at in category_attributes[cat]:
                            rel_attributes.update(at)
    return rel_attributes


def process_idoit(url, username, password, api_key):
    global api_url
    api_url = "http://" + url + "/i-doit/src/jsonrpc.php"

    global headers
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["X-RPC-Auth-Username"] = username
    headers["X-RPC-Auth-Password"] = password

    global apikey
    apikey = api_key

    constants = api_constants()

    # {"C__OBJTYPE__SERVER": "Server"}
    objectTypes = constants["result"]["objectTypes"]
    # {"C__RELATION_TYPE__SOFTWARE": "Software assignment"}
    relationTypes = constants["result"]["relationTypes"]
    # {"C__CATG__GLOBAL": "General"}
    categories_g = constants["result"]["categories"]["g"]
    # {"C__CATS__CLIENT": "Desktop"}
    categories_s = constants["result"]["categories"]["s"]

    # {"Server": "C__OBJTYPE__SERVER"}
    ci_types = {y: x for x, y in objectTypes.items()}
    # {"Software assignment": "C__RELATION_TYPE__SOFTWARE"}
    rel_types = {y: x for x, y in relationTypes.items()}

    # {"C__CATG__GLOBAL": [{"ID": "id"}]}
    category_attributes = {}
    # {'C__CATG__GLOBAL': {'ID': 'int', 'Title': 'text', 'Condition': 'int', 'Creation date': 'text'}}
    category_attr_types = {}
    for cat in {**categories_g, **categories_s}:
        category_info = api_category_info(cat)
        category_attributes[cat] = category_info.get("attributes")
        category_attr_types[cat] = category_info.get("types")

    # {"C__OBJTYPE__SERVICE": "1"}
    object_types_ids = api_obj_types()

    # {"C__OBJTYPE__PERSON": [{"Service": "connected_object"}, {"SYSID": "sysid"}]}
    obj_type_attributes = {}
    #
    attribute_types = {}
    for obj_name in object_types_ids:
        obj_id = object_types_ids[obj_name]
        attrs = get_object_attributes(
            obj_id, category_attributes, category_attr_types)
        obj_type_attributes[obj_name] = attrs["object_attributes"]
        attribute_types[obj_name] = attrs["attributes_types"]

    rel_attributes = get_relation_attributes(category_attributes)

    data_model["ci_types"] = ci_types
    data_model["rel_types"] = rel_types
    data_model["ci_types_attributes"] = obj_type_attributes
    data_model["rel_attributes"] = rel_attributes
    data_model["attribute_types"] = attribute_types

    f = open("cmdb_data_model.txt", "w")
    f.write(str(data_model))
    f.write("\n")

    return data_model
