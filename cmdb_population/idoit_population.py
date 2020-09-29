# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
from colored import fg, bg, attr
import regex
import json

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


def create_idoit_ci(ci_type, ci_attrs, rules_ci_types, rules_ci_attributes):
    cmdb_id = None

    cmdb_type = rules_ci_types.get(ci_type)
    if cmdb_type != None:
        cmdb_type_text = "\"type\": \"" + cmdb_type + "\", "
        cmdb_at_text = ""
        if "title" not in ci_attrs.values():
            cmdb_at_text += "\"title\": \"titulo\","
        for at in ci_attrs:
            cmdb_at = rules_ci_attributes.get(ci_type).get(at)
            value = ci_attrs.get(at)
            if cmdb_at != None:
                cmdb_at_text += "\"" + cmdb_at + "\": \"" + value + "\","
            else:
                cmdb_at_text = ""

        body = json.loads("""{
            \"version\": \"2.0\",
            \"method\": \"cmdb.object.create\",
            \"params\": { 
                """ + cmdb_type_text + cmdb_at_text + """
                \"apikey\": \"""" + apikey + """\",
                \"language\": \"en\"
            },
            \"id\": 1
        }""")

        print(body)

        s = requests.Session()
        create_ci_request = s.post(cmdb_url, json=body, headers=headers)
        create_ci = create_ci_request.json()
        print(create_ci)
        if "result" in create_ci:
            success = create_ci.get("result").get("success")
            if success == True:
                cmdb_id = create_ci.get("result").get("id")
    return cmdb_id


def create_idoit_relationship(rel_type, rel_attrs, rules_rel_types, rules_rel_attributes, ci_ids, source, target):
    cmdb_id = None
    cmdb_type = rules_rel_types.get(rel_type)
    if cmdb_type != None:
        cmdb_type_text = "\"type\": \"" + cmdb_type + "\", "

        if source != None and target != None:
            # TODO: ir buscar os atributos que representam a source e o target às rules
            cmdb_source_target_text = "\"object1\": \"" + \
                source + "\", \"object2\": \"" + target + "\", "
            cmdb_at_text = ""
            if "title" not in rel_attrs.values():
                cmdb_at_text += "\"title\": \"titulo\","
            for at in rel_attrs:
                cmdb_at = rules_rel_attributes.get(rel_type).get(at)
                value = rel_attrs.get(at)
                # TODO: verificar os tipos dos atributos!
                if cmdb_at != None:
                    cmdb_at_text += "\"" + cmdb_at + "\": \"" + value + "\","
                else:
                    cmdb_at_text = ""

            body = json.loads("""{
                \"version\": \"2.0\",
                \"method\": \"cmdb.object.create\",
                \"params\": { 
                    """ + cmdb_type_text + cmdb_source_target_text + cmdb_at_text + """
                    \"apikey\": \"""" + apikey + """\",
                    \"language\": \"en\"
                },
                \"id\": 1
            }""")

            s = requests.Session()
            create_ci_request = s.post(cmdb_url, json=body, headers=headers)
            create_ci = create_ci_request.json()
            print(create_ci)
            print()
            if "result" in create_ci:
                success = create_ci.get("result").get("success")
                if success == True:
                    cmdb_id = create_ci.get("result").get("id")
    return cmdb_id


def run_idoit_population(cmdb_info, rules, cis_types, rels_types, cis_attributes, rels_attributes, sources, targets):
    idoit_specification(cmdb_info)
    ids = {}  # id bd : id cmdb

    for ci in cis_types:
        id_ci = create_idoit_ci(cis_types.get(ci), cis_attributes.get(
            ci), rules.get("ci_types"), rules.get("ci_attributes"))
        if id_ci != None:
            ids[ci] = id_ci

    for rel in rels_types:
        rel_id = create_idoit_relationship(rels_types.get(
            rel), rels_attributes.get(rel), rules.get("rel_types"), rules.get("rel_attributes"), ids, sources.get(rel), targets.get(rel))

    return True

    # TODO: devo fazer o logout?
