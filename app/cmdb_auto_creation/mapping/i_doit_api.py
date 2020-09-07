#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json


def api_constants():
    constants_body = json.loads("{\"version\": \"2.0\",\"method\": \"idoit.constants\",\"params\": {\"apikey\": \"" +
                                apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    constants_request = s.post(api_url, json=constants_body, headers=headers)
    constants = constants_request.json()
    return constants


def api_category_info(category):
    attributes = []
    cat_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.category_info\",\"params\": {\"category\": \"" +
                          category + "\", \"apikey\": \"" + apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    cat_request = s.post(api_url, json=cat_body, headers=headers)
    if cat_request.text != "":
        if "result" in cat_request.json():
            for attr in cat_request.json()["result"]:
                new_atr = {}
                new_atr[cat_request.json()["result"][attr]["title"]] = attr
                attributes.append(new_atr)

    return attributes


def api_obj_types():
    obj_body = json.loads("{\"version\": \"2.0\",\"method\": \"cmdb.object_types\",\"params\": {\"apikey\": \"" +
                          apikey + "\",\"language\": \"en\"},\"id\": 1}")
    s = requests.Session()
    obj_request = s.post(api_url, json=obj_body, headers=headers)
    obj_types = {}
    for obj in obj_request.json()["result"]:
        obj_types[obj["const"]] = obj["id"]
    return obj_types


def get_object_attributes(id, category_attributes):
    object_attributes = []
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
                        object_attributes.extend(category_attributes[cat])
            if "cats" in obj_categories_request.json()["result"]:
                for cat_s in obj_categories_request.json()["result"]["cats"]:
                    cat = cat_s["const"]
                    if cat in category_attributes:
                        object_attributes.extend(category_attributes[cat])
    return object_attributes


def main(url, username, password, api_key):
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
    for cat in {**categories_g, **categories_s}:
        category_attributes[cat] = api_category_info(cat)

    # {"C__OBJTYPE__SERVICE": "1"}
    object_types_ids = api_obj_types()

    # {"C__OBJTYPE__PERSON": [{"Service": "connected_object"}, {"SYSID": "sysid"}]}
    obj_type_attributes = {}
    for obj_name in object_types_ids:
        obj_id = object_types_ids[obj_name]
        obj_type_attributes[obj_name] = get_object_attributes(
            obj_id, category_attributes)


main("192.168.1.72", "admin", "admin", "b6b2rwwtsfksokgw")
