# -*- coding: utf-8 -*-

import operator
import os

from similarity import similarity

os.environ["SPACY_WARNING_IGNORE"] = "W008"


def calc_similars(cmdb, db):
    res = {}
    for c1 in cmdb:
        l = {}
        for c2 in db:
            l[db.get(c2)] = similarity.calculate_similarity(c1, c2)
        l_sort = dict(
            sorted(l.items(), key=operator.itemgetter(1), reverse=True))
        res[cmdb.get(c1)] = l_sort
    return res


def select_most_similar(calculated_matches):
    m = []
    v = {}
    # {'System Service': {'Service': 0.7958800017463593, 'Operating System': 0.6879912871822835, 'media access control': 0.5440860997165468}}
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
