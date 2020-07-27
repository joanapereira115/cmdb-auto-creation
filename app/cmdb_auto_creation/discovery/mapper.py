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

nlp = spacy.load('en_core_web_lg')

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
