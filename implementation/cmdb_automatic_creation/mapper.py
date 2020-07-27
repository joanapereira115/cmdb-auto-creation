#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import spacy
import difflib
from colored import fg, bg, attr

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

cim = {
    'cim_tables': {"filesystem": "filesystem", "operating system": "operatingsystem"},
    'cim_tables_atrs': {"filesystem": {"caption": "caption", "description": "description", "element name": "elementname"}, "operatingsystem": {"caption": "caption", "description": "description", "operational status": "operationalstatus"}},
    'cim_proc': {"filesystem": ["caption", "description", "element name"], "operating system": ["caption", "description", "operational status"]}
}

"""
cmdb = {
    'cmdb_tables': {
        'ac air quantity unit': 'isys_ac_air_quantity_unit',
        'ac refrigerating capacity unit': 'isys_ac_refrigerating_capacity_unit',
        'ac type': 'isys_ac_type',
        'access type': 'isys_access_type',
        'account': 'isys_account',
        'agent': 'isys_agent',
        'application manufacturer': 'isys_application_manufacturer'
    },
    'cmdb_proc': {
        'ac air quantity unit': ['ac air quantity unit id', 'ac air quantity unit const', 'ac air quantity unit title', 'ac air quantity unit description', 'ac air quantity unit property', 'ac air quantity unit sort', 'ac air quantity unit status'],
        'ac refrigerating capacity unit': ['ac refrigerating capacity unit id', 'ac refrigerating capacity unit const', 'ac refrigerating capacity unit factor', 'ac refrigerating capacity unit title', 'ac refrigerating capacity unit description', 'ac refrigerating capacity unit property', 'ac refrigerating capacity unit sort', 'ac refrigerating capacity unit status'],
        'ac type': ['ac type id', 'ac type title', 'ac type description', 'ac type const', 'ac type property', 'ac type sort', 'ac type status'],
        'access type': ['access type id', 'access type title', 'access type description', 'access type const', 'access type sort', 'access type status', 'access type property'],
        'account': ['account id', 'account title', 'account description', 'account property', 'account status', 'account const', 'account sort'],
        'agent': ['agent id', 'agent title', 'agent status', 'agent const', 'agent sort', 'agent description'],
        'application manufacturer': ['application manufacturer id', 'application manufacturer title', 'application manufacturer description', 'application manufacturer sort', 'application manufacturer const', 'application manufacturer status', 'application manufacturer property']
    },
    'cmdb_tables_atrs': {
        'isys_ac_air_quantity_unit': {'ac air quantity unit id': 'isys_ac_air_quantity_unit__id', 'ac air quantity unit const': 'isys_ac_air_quantity_unit__const', 'ac air quantity unit title': 'isys_ac_air_quantity_unit__title', 'ac air quantity unit description': 'isys_ac_air_quantity_unit__description', 'ac air quantity unit property': 'isys_ac_air_quantity_unit__property', 'ac air quantity unit sort': 'isys_ac_air_quantity_unit__sort', 'ac air quantity unit status': 'isys_ac_air_quantity_unit__status'},
        'isys_ac_refrigerating_capacity_unit': {'ac refrigerating capacity unit id': 'isys_ac_refrigerating_capacity_unit__id', 'ac refrigerating capacity unit const': 'isys_ac_refrigerating_capacity_unit__const', 'ac refrigerating capacity unit factor': 'isys_ac_refrigerating_capacity_unit__factor', 'ac refrigerating capacity unit title': 'isys_ac_refrigerating_capacity_unit__title', 'ac refrigerating capacity unit description': 'isys_ac_refrigerating_capacity_unit__description', 'ac refrigerating capacity unit property': 'isys_ac_refrigerating_capacity_unit__property', 'ac refrigerating capacity unit sort': 'isys_ac_refrigerating_capacity_unit__sort', 'ac refrigerating capacity unit status': 'isys_ac_refrigerating_capacity_unit__status'},
        'isys_ac_type': {'ac type id': 'isys_ac_type__id', 'ac type title': 'isys_ac_type__title', 'ac type description': 'isys_ac_type__description', 'ac type const': 'isys_ac_type__const', 'ac type property': 'isys_ac_type__property', 'ac type sort': 'isys_ac_type__sort', 'ac type status': 'isys_ac_type__status'},
        'isys_access_type': {'access type id': 'isys_access_type__id', 'access type title': 'isys_access_type__title', 'access type description': 'isys_access_type__description', 'access type const': 'isys_access_type__const', 'access type sort': 'isys_access_type__sort', 'access type status': 'isys_access_type__status', 'access type property': 'isys_access_type__property'},
        'isys_account': {'account id': 'isys_account__id', 'account title': 'isys_account__title', 'account description': 'isys_account__description', 'account property': 'isys_account__property', 'account status': 'isys_account__status', 'account const': 'isys_account__const', 'account sort': 'isys_account__sort'},
        'isys_agent': {'agent id': 'isys_agent__id', 'agent title': 'isys_agent__title', 'agent status': 'isys_agent__status', 'agent const': 'isys_agent__const', 'agent sort': 'isys_agent__sort', 'agent description': 'isys_agent__description'},
        'isys_application_manufacturer': {'application manufacturer id': 'isys_application_manufacturer__id', 'application manufacturer title': 'isys_application_manufacturer__title', 'application manufacturer description': 'isys_application_manufacturer__description', 'application manufacturer sort': 'isys_application_manufacturer__sort', 'application manufacturer const': 'isys_application_manufacturer__const', 'application manufacturer status': 'isys_application_manufacturer__status', 'application manufacturer property': 'isys_application_manufacturer__property'}
    }
}
"""

nlp = spacy.load('en_core_web_lg')

# TODO: considerar a existência de hierarquias
# TODO: utilizar lexical database do domínio das TI para melhores resultados
# TODO: deve ser restringido o valor de similaridade (ou seja, só aceitar acima de determinado valor? ou pedir confirmação abaixo de determinado valor?)
# TODO: considerar também o tipo de dados dos atributos


def semantic_similarity(word1, word2):
    w1 = word1.lower()
    w2 = word2.lower()
    s = nlp(w1).similarity(nlp(w2))
    return s


def syntatic_similarity(word1, word2):
    w1 = word1.lower()
    w2 = word2.lower()
    seq = difflib.SequenceMatcher(None, w1, w2)
    d = seq.ratio()
    return d


def calc_similarity(sem, syn):
    r = sem*0.7 + syn*0.3
    return r


def calc_similars(cmdb, cim):
    res = {}
    for c1 in cmdb:
        l = {}
        for c2 in cim:
            l[c2] = calc_similarity(semantic_similarity(
                c1, c2), syntatic_similarity(c1, c2))
        l_sort = dict(
            sorted(l.items(), key=operator.itemgetter(1), reverse=True))
        res[c1] = l_sort
    return res


def calc_atr_similarity(matches, cmdb_atr, cim_atr):
    res = {}
    for cmdb_elm in matches:
        values = matches[cmdb_elm]
        atrs = {}
        for cim_elm in values:
            cmdb_atrs = cmdb_atr[cmdb_elm]
            cim_atrs = cim_atr[cim_elm]
            matching = calc_similars(cmdb_atrs, cim_atrs)
            atrs[cim_elm] = matching
        res[cmdb_elm] = atrs
    return res


def select_most_similar(calculated_matches):
    m = []
    v = {}
    for key in calculated_matches:
        values = calculated_matches.get(key)
        if len(values) > 0:
            fst = list(values.keys())[0]
            if fst not in m:
                m.append(fst)
                v[fst] = {key: values.get(fst)}
            else:
                prev = v.get(fst).get(list(v.get(fst).keys())[0])
                if values.get(fst) > prev:
                    k = calculated_matches.get(list(v.get(fst).keys())[0])
                    ky = str(list(k.keys())[0])
                    del k[ky]
                    return select_most_similar(calculated_matches)
    return v


def calculate_average(similars):
    total = 0
    count = 0
    for k in similars:
        count += 1
        total += similars.get(k).get(list(similars.get(k).keys())[0])
    return total/float(count)


def calculate_atr_weight(elvalue, atrvalue):
    res = elvalue * 0.7 + atrvalue * 0.3
    return res


def select_matches(similars):
    res = {}
    for k in similars:
        res[k] = list(similars.get(k).keys())[0]
    return res


def to_original(matches, cmdb, cim):
    res = {}

    cmdb_tables = cmdb['cmdb_tables']
    cmdb_tables_atrs = cmdb['cmdb_tables_atrs']
    cim_tables = cim['cim_tables']
    cim_tables_atrs = cim['cim_tables_atrs']

    for cim_elm in matches:
        r = {}
        new_cim_elm = cim_tables[cim_elm]
        cmdb_elm = list(matches[cim_elm].keys())[0]
        new_cmdb_elm = cmdb_tables[cmdb_elm]
        atrs = matches[cim_elm][cmdb_elm]
        new_atrs = {}
        for a in atrs:
            cim_atr = a
            cmdb_atr = atrs[a]
            new_cim_atr = cim_tables_atrs[new_cim_elm][cim_atr]
            new_cmdb_atr = cmdb_tables_atrs[new_cmdb_elm][cmdb_atr]
            new_atrs[new_cim_atr] = new_cmdb_atr
        r[new_cmdb_elm] = new_atrs
        res[new_cim_elm] = r
    return res


def final(cmdb):
    result = {}
    similars = {}

    cmdb_tables_proc = [x for x in cmdb['cmdb_tables']]
    cim_tables_proc = [x for x in cim['cim_tables']]

    print(blue + "\n>>> " + reset + "Calculating table names similarity...")
    similar_classes = calc_similars(cmdb_tables_proc, cim_tables_proc)

    print(blue + ">>> " + reset + "Calculating field names similarity...")
    similar_atrs = calc_atr_similarity(
        similar_classes, cmdb['cmdb_proc'], cim['cim_proc'])

    for cmdb_elm in similar_atrs:
        atrs = {}
        for cim_elm in similar_atrs[cmdb_elm]:
            atrs[cim_elm] = select_most_similar(
                similar_atrs[cmdb_elm][cim_elm])
            avg = calculate_average(atrs[cim_elm])
            tot = calculate_atr_weight(similar_classes[cmdb_elm][cim_elm], avg)
            similar_classes[cmdb_elm][cim_elm] = tot
        similars[cmdb_elm] = atrs

    print(blue + ">>> " + reset + "Defining similar table names...")
    classes_similars = select_most_similar(similar_classes)
    map_classes = select_matches(classes_similars)

    print(blue + ">>> " + reset + "Defining similar field names...")
    for cim_elm in map_classes:
        temp = {}
        cmdb_elm = map_classes[cim_elm]
        map_atrs = select_matches(similars[cmdb_elm][cim_elm])
        temp[cmdb_elm] = map_atrs
        result[cim_elm] = temp

    print(blue + ">>> " + reset + "Determining original names...")
    final_res = to_original(result, cmdb, cim)

    print(green + "\n>>> " + reset + "Mapping of models completed successfully.")
    return final_res
