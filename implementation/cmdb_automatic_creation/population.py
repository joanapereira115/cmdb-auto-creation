#!/usr/bin/env python3

rules = {
    'isys_catg_computing_resources_list': {'operatingsystem': {
        'caption': 'isys_catg_computing_resources_list__property',
        'operationalstatus': 'isys_catg_computing_resources_list__status',
        'description': 'isys_catg_computing_resources_list__description'}},
    'isys_filesystem_type': {'filesystem': {
        'elementname': 'isys_filesystem_type__title',
        'description': 'isys_filesystem_type__description'}}
}

send_format = {
    "jsonrpc": "2.0",
    "method": "cmdb.object.create",
    "params": {
        "type": "C__OBJTYPE__SERVER",
        "title": "My little server",
        "apikey": "c1ia5q"
    },
    "id": 1
}

cmdb_header = "Content-Type: application/json"

cmdb_api = 'https://demo.i-doit.com/src/jsonrpc.php'

cim_api = 'http://localhost:3000'


def run_population():
    print("\n*******************************************")
    print("Population Phase")
    print("*******************************************\n")
