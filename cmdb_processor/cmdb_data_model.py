# -*- coding: utf-8 -*-

"""
    Saves information about the data model of the chosen CMDB, holding information about configuration item types, 
    relationship types, configuration items, and relationship attributes, restrictions between relationships, 
    data types of attributes, and values for dialog type attributes.
"""
cmdb_data_model = {
    # {"CI type": "description", ...}
    "ci_types": {},

    # {"relationship type": "description", ...}
    "rel_types": {},

    # {"CI type": {"attribute": "description", ...}, ...}
    "ci_attributes": {},

    # {"relationship type": {"attribute": "description", ...}, ...}
    "rel_attributes": {},

    # {"CI type": {"attribute": "data type", ...}, ...}
    "ci_attributes_data_types": {},

    # {"relationship type": {"attribute": "data type", ...}, ...}
    "rel_attributes_data_types": {},

    # {"relationship type": [{"source CI attribute": "CI type", "target CI attribute": "CI type"}, ...], ...}
    "rel_restrictions": {},

    # {"CI type": {"attribute": {"value", "description", ...}, ...}, ...}
    "ci_dialog_attributes": {},

    # {"relationship type": {"attribute": {"value", "description", ...}, ...}, ...}
    "rel_dialog_attributes": {}

}
