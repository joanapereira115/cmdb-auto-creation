# -*- coding: utf-8 -*-

import operator
import os

from similarity import similarity

from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import getpass
import regex
import pyfiglet

from cmdb_processor import i_doit_processor
from db_processor import db_processor

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

style = style_from_dict({
    Token.QuestionMark: '#B54653 bold',
    Token.Selected: '#86DEB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


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


def select_option(option1, option2, choice):
    question = [
        {
            'type': 'list',
            'message': 'The similarities between \'' + choice + '\' with \'' + option1 + '\' and \'' + option2 + '\' are equal. Choose the one to consider.',
            'name': 'option',
            'choices': [{'name': option1}, {'name': option2}]
        }
    ]

    answer = prompt(question, style=style)
    return answer["option"]


def select_most_similar(calculated_matches, v, m):
    existing_keys = []
    for k in v:
        existing_keys.append(list(v.get(k).keys())[0])
    for key in calculated_matches:
        if key not in existing_keys:
            values = calculated_matches.get(key)
            if len(values) > 0:
                fst = list(values.keys())[0]
                l = len(list(values.keys()))
                i = 1
                while i < l:
                    # todo: e não estiver no v o que está a ser comparado com um valor superior
                    other = list(values.keys())[i]
                    if values.get(fst) == values.get(other):
                        selected = select_option(fst, other, key)
                        fst = selected
                        if selected == other:
                            calculated_matches[key][fst], calculated_matches[key][
                                other] = calculated_matches[key][other], calculated_matches[key][fst]
                        i += 1
                    else:
                        i = l

                if fst not in m:
                    m.append(fst)
                    v[fst] = {key: values.get(fst)}
                else:
                    prev = v.get(fst).get(list(v.get(fst).keys())[0])

                    if values.get(fst) == prev:
                        last = list(v.get(fst).keys())[0]
                        print()
                        selected = select_option(key, last, fst)
                        if selected == key:
                            del calculated_matches[last][fst]
                            v[fst] = {key: values.get(fst)}
                            return select_most_similar(calculated_matches, v, m)
                        else:
                            del calculated_matches[key][fst]
                            return select_most_similar(calculated_matches, v, m)

                    if values.get(fst) > prev:
                        last = list(v.get(fst).keys())[0]
                        del calculated_matches[last][fst]
                        v[fst] = {key: values.get(fst)}
                        return select_most_similar(calculated_matches, v, m)
    return v



