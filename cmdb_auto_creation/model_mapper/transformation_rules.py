# -*- coding: utf-8 -*-

"""
    Saves information about the transformation rules.
"""
rules = {
    # {"DB CI type": "CMDB CI type", ...}
    "ci_types": {},

    # {"DB relationship type": "CMDB relationship type", ...}
    "rel_types": {},

    # {"DB CI type": {"DB attribute": "CMDB attribute", ...}, ...}
    "ci_attributes": {},

    # {"DB relationship type": {"DB attribute": "CMDB attribute", ...}, ...}
    "rel_attributes": {}
}
