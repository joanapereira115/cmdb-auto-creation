#!/usr/bin/env python3

import difflib
import spacy
import operator

nlp = spacy.load('en_core_web_lg')

cim_classes = ["filesystem", "operating system"]
cim_atrs = {
    "filesystem": ["caption", "description", "element name"],
    "operating system": ["caption", "description", "operational status"]
}

cmdb_classes = ['catg computing resources list', "filesystem type"]

cmdb_atrs = {
    'catg computing resources list':
        ['catg computing resources list property', 'catg computing resources list status',
            'catg computing resources list description'],
    'filesystem type':
        ['filesystem type title', 'filesystem type description']
}

# TODO: fazer verificações para existência de elementos!

# utilizar lexical database do domínio das TI para melhores resultados


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

# considerar também o tipo de dados dos atributos


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
    # inverter a ordem dos valores CMDB:CIM
    # possível verificação dos valores
    res = {}
    for k in similars:
        res[k] = list(similars.get(k).keys())[0]
    return res


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


print(final(cmdb_classes, cmdb_atrs, cim_classes, cim_atrs))
