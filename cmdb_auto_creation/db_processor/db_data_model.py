# -*- coding: utf-8 -*-

"""
    Saves information about the data model of the database, holding information about configuration item types, 
    relationship types, and configuration item and relationship attributes.
"""
db_data_model = {
    # {"CI type": "description", ...}
    "ci_types": {},

    # {"relationship type": "description", ...}
    "rel_types": {},

    # {"CI type": {"attribute": "description", ...}, ...}
    "ci_attributes": {},

    # {"relationship type": {"attribute": "description", ...}, ...}
    "rel_attributes": {}
}
