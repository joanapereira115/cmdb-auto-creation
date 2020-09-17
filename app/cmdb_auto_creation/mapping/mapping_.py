import os
from .cmdb_data_model import data_model
from .app_data_model import app_data_model
from .mapper import calc_similars, select_most_similar, filter_most_similar

from colored import fg, bg, attr
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


os.environ["SPACY_WARNING_IGNORE"] = "W008"


def calculate_class_similarity(cmdb_types, app_types):
    result = {}
    cmdb_tp = [x for x in cmdb_types]
    app_tp = [y for y in app_types]
    # {'System Service': {'Service': 0.7958800017463593, 'Operating System': 0.6879912871822835, 'media access control': 0.5440860997165468}}
    class_similarity = calc_similars(cmdb_tp, app_tp)
    return class_similarity


def map_():
    res = {}
    # {'System Service': 'C__OBJTYPE__SERVICE', 'Application': 'C__OBJTYPE__APPLICATION'}
    cmdb_ci_types = data_model["ci_types"]
    # {'Software assignment': 'C__RELATION_TYPE__SOFTWARE', 'Cluster service assignment': 'C__RELATION_TYPE__CLUSTER_SERVICE'}
    cmdb_rel_types = data_model["rel_types"]
    # {'C__OBJTYPE__PRINTER': {'Title': 'title', 'In-/Output': 'type', 'Wiring system': 'wiring_system', 'Interface': 'interface'}}
    cmdb_ci_types_attributes = data_model["ci_types_attributes"]
    # [{'Service': 'connected_object'}, {'SYSID': 'sysid'}, {'Object 1': 'object1'}, {'Object 2': 'object2'}]
    cmdb_rel_types_attributes = data_model["rel_attributes"]

    # {'ipv4': 'ipv4', 'Host': 'Host', 'media access control': 'media_access_control', 'Protocol': 'Protocol', 'Service': 'Service', 'Operating System': 'Operating_System'}
    app_ci_types = app_data_model["ci_types"]
    # {'has address': 'has_address', 'address of': 'address_of', 'has protocol': 'has_protocol', 'protocol of': 'protocol_of', 'has service': 'has_service', 'service of': 'service_of'}
    app_rel_types = app_data_model["rel_types"]
    # {'configuration item type': 'ci_type', 'name': 'name', 'value': 'value', 'status': 'status'}
    app_ci_types_attributes = app_data_model["ci_types_attributes"]
    # {'rel type': 'rel_type', 'source': 'source', 'target': 'target'}
    app_rel_types_attributes = app_data_model["rel_types_attributes"]

    ci_similarity = calculate_class_similarity(cmdb_ci_types, app_ci_types)
    rel_similarity = calculate_class_similarity(cmdb_rel_types, app_rel_types)

    ci_most_similars = filter_most_similar(select_most_similar(ci_similarity))
    rel_most_similars = filter_most_similar(
        select_most_similar(rel_similarity))

    different_attr = {}
    for ci in cmdb_ci_types_attributes:
        for at in cmdb_ci_types_attributes[ci]:
            if at not in different_attr:
                different_attr[at] = cmdb_ci_types_attributes[ci][at]

    ci_attr_similarity = calculate_class_similarity(
        different_attr, app_ci_types_attributes)

    ci_attr_similars = filter_most_similar(
        select_most_similar(ci_attr_similarity))

    rel_attr_similarity = calculate_class_similarity(
        cmdb_rel_types_attributes, app_rel_types_attributes)

    rel_attr_similars = filter_most_similar(
        select_most_similar(rel_attr_similarity))

    f = open("attrsimilars.txt", "w")
    f.write(str(ci_most_similars))
    f.write("\n")
    f.write(str(rel_most_similars))
    f.write("\n")
    f.write(str(ci_attr_similars))
    f.write("\n")
    f.write(str(rel_attr_similars))
    f.close()

    res["ci_most_similars"] = ci_most_similars
    res["rel_most_similars"] = rel_most_similars
    res["ci_attr_similars"] = ci_attr_similars
    res["rel_attr_similars"] = rel_attr_similars

    return res


"""
def final(cmdbcl, cmdbat, cimcl, cimat):
    result = {}
    similar_classes = calc_similars(cmdbcl, cimcl)
    similar_atrs = calc_atr_similarity(similar_classes, cmdbat, cimat)
    similars = {}
    for cmdb_elm in similar_atrs:
        atrs = {}
        for cim_elm in similar_atrs[cmdb_elm]:
            atrs[cim_elm] = select_most_similar(
                similar_atrs[cmdb_elm][cim_elm])
            avg = calculate_average(atrs[cim_elm])
            tot = calculate_atr_weight(similar_classes[cmdb_elm][cim_elm], avg)
            similar_classes[cmdb_elm][cim_elm] = tot
        similars[cmdb_elm] = atrs
    classes_similars = select_most_similar(similar_classes)
    map_classes = select_matches(classes_similars)
    for cim_elm in map_classes:
        temp = {}
        cmdb_elm = map_classes[cim_elm]
        map_atrs = select_matches(similars[cmdb_elm][cim_elm])
        temp[cim_elm] = map_atrs
        result[cmdb_elm] = temp
    return result
"""
