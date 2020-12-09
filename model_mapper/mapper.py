# -*- coding: utf-8 -*-

import os
from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
from tabulate import tabulate
import operator

from cmdb_processor import cmdb_data_model
from db_processor import db_data_model
from .transformation_rules import rules
from similarity import similarity

os.environ["SPACY_WARNING_IGNORE"] = "W008"

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


class NumberValidator(Validator):
    def validate(self, document):
        char = regex.search(r'[^\d\.]', document.text)
        if char:
            raise ValidationError(
                message='Please enter a number between 0 and 1.',
                cursor_position=len(document.text))  # Move cursor to end
        else:
            ok = regex.match(
                r'\d(\.\d+)?', document.text)
            if ok:
                s = regex.search(r'\d([,\.]\d+)?', document.text)
                value = float(s.group(0))
                if value < 0 or value > 1:
                    raise ValidationError(
                        message='Please enter a number between 0 and 1.',
                        cursor_position=len(document.text))  # Move cursor to end
            else:
                raise ValidationError(
                    message='Please enter a number between 0 and 1.',
                    cursor_position=len(document.text))  # Move cursor to end


def calc_similars(cmdb, db):
    """
    Calculates the similarity between the terms from the CMDB and the database.

    Parameters
    ----------
    cmdb : dict
        The CMDB terms.

    db : dict
        The database terms.

    Returns
    -------
    dict
        Returns the similarity values between all the values.
    """
    res = {}
    for c1 in cmdb:
        l = {}
        for c2 in db:
            l[db.get(c2)] = similarity.calculate_similarity(c1, c2)
        l_sort = {k: v for k, v in sorted(
            l.items(), key=lambda item: item[1], reverse=True)}
        res[cmdb.get(c1)] = l_sort
    return res


def calculate_class_similarity(cmdb_types, db_types):
    """
    Calculates the similarity between the terms from the CMDB and the database.

    Parameters
    ----------
    cmdb_types : dict
        The CMDB terms.

    db_types : dict
        The database terms.

    Returns
    -------
    dict
        Returns the similarity values between all the values.
    """
    cmdb_tp = {cmdb_types.get(x): x for x in cmdb_types}
    db_tp = {db_types.get(y): y for y in db_types}
    class_similarity = calc_similars(cmdb_tp, db_tp)
    return class_similarity


def select_option(option1, option2, choice):
    """
    Asks the user what option he thinks is more similar with the term being compared.

    Parameters
    ----------
    option1 : string
        One option.

    option2 : string
        The other option.

    choice : string
        The term being compared with the options.

    Returns
    -------
    string
        The option selected by the user.
    """
    question = [
        {
            'type': 'list',
            'message': 'The similarities between \'' + choice + '\' with \'' + option1 + '\' and \'' + option2 + '\' are equal. Choose the one to consider.',
            'name': 'option',
            'choices': [{'name': option1}, {'name': option2}]
        }
    ]

    answer = prompt(question, style=style)
    return answer.get("option")


def select_option_2(options, choice):
    choices = []
    txt = ""
    last = len(options) - 1
    for opt in options:
        if options.index(opt) == 0:
            txt += " " + str(opt)
        elif options.index(opt) == last:
            txt += " and " + str(opt) + " "
        else:
            txt += " ," + str(opt)
        choices.append({'name': opt})

    question = [
        {
            'type': 'list',
            'message': 'The similarities between \'' + choice + '\' with \'' + txt + '\' are equal. Choose the one to consider.',
            'name': 'option',
            'choices': choices
        }
    ]

    answer = prompt(question, style=style)
    return answer.get("option")


def check_if_already_has_most_similar(key, option, value, selected_values):
    existing_value = -1
    existing_key = ""
    for k in selected_values:
        if option in selected_values.get(k):
            existing_value = selected_values.get(k).get(option)
            existing_key = k
    if existing_value == -1:
        return key
    else:
        if existing_value <= value:
            return False
        else:
            return True


def select_most_similar(calculated_matches, selected_values, selected):
    for key in calculated_matches:
        if key not in selected_values:
            key_values = calculated_matches.get(key)
            values = list(key_values.values())
            fst = None
            if len(values) > 0:
                if values.count(values[0]) > 1:
                    same = [x for x in key_values if key_values[x] == values[0]]
                    for s in same:
                        if check_if_already_has_most_similar(key, s, values[0], selected_values) == True:
                            same.remove(s)
                            calculated_matches.get(key).pop(s, None)
                    if len(same) > 1:
                        fst = select_option_2(same, key)
                    elif len(same) == 1:
                        fst = same[0]
                if fst == None:
                    while fst == None:
                        key_values = calculated_matches.get(key)
                        if len(key_values) > 0:
                            if check_if_already_has_most_similar(key, list(key_values.keys())[0], key_values.get(list(key_values.keys())[0]), selected_values) == True:
                                calculated_matches.get(key).pop(
                                    list(key_values.keys())[0], None)
                            else:
                                fst = list(key_values.keys())[0]
                if fst != None:
                    if fst not in selected:
                        selected.append(fst)
                        selected_values[key] = {
                            fst: calculated_matches.get(key).get(fst)}
                        return select_most_similar(calculated_matches, selected_values, selected)

                    else:
                        for k in selected_values:
                            if fst in selected_values.get(k):
                                existing_key = k
                                existing_value = selected_values.get(
                                    k).get(fst)

                        if existing_value == calculated_matches.get(key).get(fst):
                            sel = select_option_2([existing_key, key], fst)
                            if sel == key:
                                del selected_values[existing_key]
                                del calculated_matches[existing_key][fst]
                                selected_values[key] = {
                                    fst: calculated_matches.get(key).get(fst)}
                                return select_most_similar(calculated_matches, selected_values, selected)
                            else:
                                del calculated_matches[key][fst]
                                return select_most_similar(calculated_matches, selected_values, selected)
                        else:
                            del selected_values[existing_key]
                            del calculated_matches[existing_key][fst]
                            selected_values[key] = {
                                fst: calculated_matches.get(key).get(fst)}
                            return select_most_similar(calculated_matches, selected_values, selected)
                else:
                    selected_values[key] = {}
            else:
                selected_values[key] = {}
    return selected_values


"""
def select_most_similar(calculated_matches, v, m):
"""
"""
    Selects the most similar terms between the similarity values calculated from the CMDB and the database terms.

    Parameters
    ----------
    calculated_matches : dict
        The similarity values calculated.

    v : dict
        The most similar selected and the correspondent value.

    m : list
        The most similar selected.

    Returns
    -------
    dict
        Returns the most similar terms correspondence.
    """
"""
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
                    # TODO: e não estiver no v o que está a ser comparado com um valor superior
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
"""


def calculate_attribute_similarity(similars, cmdb_attributes, db_attributes):
    """
    Calculates the similarity between the attributes from the CMDB and the database.

    Parameters
    ----------
    similars : dict
        The most similar classes calculated between the CMDB and the database.

    cmdb_attributes : dict
        The attributes of the CMDB classes.

    db_attributes : dict
        The attributes of the database classes.

    Returns
    -------
    dict
        Returns the similarity values between all the attributes.
    """
    attr_similarity = {}
    for db_t in similars:
        cmdb_t = list(similars[db_t].keys())[0]
        db_attrs = db_attributes.get(db_t)
        cmdb_attrs = cmdb_attributes.get(cmdb_t)
        if db_attrs != None and cmdb_attrs != None:
            attr_similarity[cmdb_t] = calculate_class_similarity(
                db_attrs, cmdb_attrs)
        else:
            attr_similarity[cmdb_t] = {}
    return attr_similarity


def present_map(cmdb_ci_types, db_ci_types, cmdb_rel_types, db_rel_types, cmdb_ci_attributes, db_ci_attributes, cmdb_rel_attributes, db_rel_attributes, similar_ci, similar_rel, similar_attr_ci, similar_attr_rel):
    """
    Presents the most similar values calculated from the comparasions between the items from the CMDB and the database.

    Parameters
    ----------
    cmdb_ci_types : dict
        The CMDB configuration item types.

    db_ci_types : dict
        The database configuration item types.

    cmdb_rel_types : dict
        The CMDB relationship types.

    db_rel_types : dict
        The database relationship types.

    cmdb_ci_attributes : dict
        The CMDB configuration item attributes.

    db_ci_attributes : dict
        The database configuration item attributes.

    cmdb_rel_attributes : dict
        The CMDB relationship attributes.

    db_rel_attributes : dict
        The database relationship attributes.

    similar_ci : dict
        The most similars configuration item types.

    similar_rel : dict
        The most similars relationship types.

    similar_attr_ci : dict
        The most similars configuration item attributes.

    similar_attr_rel : dict
        The most similars relationship attributes.
    """
    print("\n===============================================================================================================================================================================")
    print(blue + "CONFIGURATION ITEMS MAPPING" + reset)
    print("===============================================================================================================================================================================")
    print()
    data = []
    for db_ci in similar_ci:
        cmdb_ci = list(similar_ci[db_ci].keys())[0]
        sim = similar_ci.get(db_ci).get(cmdb_ci)
        row = [cmdb_ci, cmdb_ci_types.get(
            cmdb_ci), db_ci, db_ci_types.get(db_ci), sim]
        data.append(row)
    print(tabulate(data, headers=[
        "CI in CMDB", "Description", "CI in DB", "Description", "Similarity Coeficient"]))
    print()

    for db_ci in similar_ci:
        data = []
        cmdb_ci = list(similar_ci[db_ci].keys())[0]
        print("**************************************************************************************************")
        print(
            green + str(cmdb_ci) + " Attributes Mapping" + reset)
        print("**************************************************************************************************")
        print()
        atrs = similar_attr_ci.get(cmdb_ci)
        for cmdb_at in atrs:
            db_at = list(atrs.get(cmdb_at).keys())[0]
            sim = atrs.get(cmdb_at).get(db_at)
            row = [cmdb_at, cmdb_ci_attributes.get(
                cmdb_ci).get(cmdb_at), db_at, db_ci_attributes.get(db_ci).get(db_at), sim]
            data.append(row)
        print(tabulate(data, headers=["Attribute in CMDB", "Description",
                                      "Attribute in DB", "Description", "Similarity Coeficient"]))
        print()
    print()

    print("===============================================================================================================================================================================")
    print(blue + "RELATIONSHIPS MAPPING" + reset)
    print("===============================================================================================================================================================================")
    print()

    data = []
    for db_rel in similar_rel:
        cmdb_rel = list(similar_rel[db_rel].keys())[0]
        sim = similar_rel.get(db_rel).get(cmdb_rel)
        row = [cmdb_rel, cmdb_rel_types.get(
            cmdb_rel), db_rel, db_rel_types.get(db_rel), sim]
        data.append(row)
        atrs = similar_attr_rel.get(cmdb_rel)
    print(tabulate(data, headers=[
        "Relationship in CMDB", "Description", "Relationship in DB", "Description", "Similarity Coeficient"]))
    print()

    for db_rel in similar_rel:
        data = []
        cmdb_rel = list(similar_rel[db_rel].keys())[0]
        print("**************************************************************************************************")
        print(green + str(cmdb_rel) + " Attributes Mapping" + reset)
        print("**************************************************************************************************")
        print()
        for cmdb_at in atrs:
            db_at = list(atrs.get(cmdb_at).keys())[0]
            sim = atrs.get(cmdb_at).get(db_at)
            cmdb_at_desc = cmdb_rel_attributes.get(cmdb_rel)
            if cmdb_at_desc != None:
                cmdb_at_desc = cmdb_at_desc.get(cmdb_at)
            db_at_desc = db_rel_attributes.get(db_rel)
            if db_at_desc != None:
                db_at_desc = db_at_desc.get(db_at)
            row = [cmdb_at, cmdb_at_desc, db_at,
                   db_at_desc, sim]
            data.append(row)
        print(tabulate(data, headers=["Attribute in CMDB", "Description",
                                      "Attribute in DB", "Description", "Similarity Coeficient"]))
        print
    print()


def ask_for_threshold():
    """
    Asks the user the threshold value that he wants to consider.

    Returns
    -------
    string
        The threshold value selected by the user.
    """
    threshold_question = [
        {
            'type': 'input',
            'message': 'Enter the threshold value that you want to consider (similarities below that value will not be considered):',
            'name': 'threshold',
            'validate': NumberValidator
        }
    ]
    threshold_answer = prompt(threshold_question, style=style)
    return threshold_answer.get("threshold")


def define_rules(threshold, similar_ci, similar_rel, similar_attr_ci, similar_attr_rel):
    """
    Defines the mapping rules based on the threshold choosed by the user and the most similar values calculated between the terms of the CMDB and the database.

    Parameters
    ----------
    threshold : string
        The threshold value selected by the user.

    similar_ci : dict
        The most similars configuration item types.

    similar_rel : dict
        The most similars relationship types.

    similar_attr_ci : dict
        The most similars configuration item attributes.

    similar_attr_rel : dict
        The most similars relationship attributes.
    """
    rules["ci_types"] = {db_ci: list(similar_ci.get(db_ci).keys())[
        0] for db_ci in similar_ci if float(similar_ci.get(db_ci).get(list(similar_ci.get(db_ci).keys())[
            0])) > threshold}

    rules["rel_types"] = {db_rel: list(similar_rel.get(db_rel).keys())[
        0] for db_rel in similar_rel if float(similar_rel.get(db_rel).get(list(similar_rel.get(db_rel).keys())[
            0])) > threshold}

    inverse_cis = {x: y for y, x in rules["ci_types"].items()}
    inverse_rels = {x: y for y, x in rules["rel_types"].items()}

    for cmdb_ci, atrs in similar_attr_ci.items():
        db_ci = inverse_cis.get(cmdb_ci)
        if db_ci in rules["ci_types"]:
            attr = {}
            for cmdb_at in atrs:
                db_at = list(atrs.get(cmdb_at).keys())[0]
                if float(atrs.get(cmdb_at).get(db_at)) > threshold:
                    attr[db_at] = cmdb_at
            rules["ci_attributes"][db_ci] = attr

    for cmdb_rel, atrs in similar_attr_rel.items():
        db_rel = inverse_rels.get(cmdb_rel)
        if db_rel in rules["rel_types"]:
            attr = {}
            for cmdb_at in atrs:
                db_at = list(atrs.get(cmdb_at).keys())[0]
                if float(atrs.get(cmdb_at).get(db_at)) > threshold:
                    attr[db_at] = cmdb_at
            rules["rel_attributes"][db_rel] = attr


def run_mapper():
    """
    Defines the mapping rules between the two models, calculating the similarity between the terms of the CMDB and the database.
    """
    print(blue + "\n>>> " + reset + "Executing the model mapper...")

    cmdb_ci_types = cmdb_data_model.cmdb_data_model.get("ci_types")
    cmdb_rel_types = cmdb_data_model.cmdb_data_model.get("rel_types")
    cmdb_ci_attributes = cmdb_data_model.cmdb_data_model.get("ci_attributes")
    cmdb_rel_attributes = cmdb_data_model.cmdb_data_model.get("rel_attributes")

    db_ci_types = db_data_model.db_data_model.get("ci_types")
    db_rel_types = db_data_model.db_data_model.get("rel_types")
    db_ci_attributes = db_data_model.db_data_model.get("ci_attributes")
    db_rel_attributes = db_data_model.db_data_model.get("rel_attributes")

    print(blue + "\n>>> " + reset +
          "Calculating configuration item types similarity...")
    ci_similarity = calculate_class_similarity(cmdb_ci_types, db_ci_types)
    print()
    print("Similaridade dos CIs")
    print(ci_similarity)
    similar_ci = select_most_similar(ci_similarity, {}, [])

    print(blue + "\n>>> " + reset + "Calculating relationship types similarity...")
    rel_similarity = calculate_class_similarity(cmdb_rel_types, db_rel_types)
    print()
    print("Similaridade dos Rels")
    print(rel_similarity)
    similar_rel = select_most_similar(rel_similarity, {}, [])

    print(blue + "\n>>> " + reset +
          "Calculating configuration item attributes similarity...")
    attr_ci_similarity = calculate_attribute_similarity(
        similar_ci, cmdb_ci_attributes, db_ci_attributes)

    print(blue + "\n>>> " + reset +
          "Calculating relationship attributes similarity...")
    attr_rel_similarity = calculate_attribute_similarity(
        similar_rel, cmdb_rel_attributes, db_rel_attributes)

    similar_attr_ci = {x: select_most_similar(
        attr_ci_similarity.get(x), {}, []) for x in attr_ci_similarity}

    similar_attr_rel = {y: select_most_similar(
        attr_rel_similarity.get(y), {}, []) for y in attr_rel_similarity}

    present_map(cmdb_ci_types, db_ci_types, cmdb_rel_types, db_rel_types, cmdb_ci_attributes, db_ci_attributes, cmdb_rel_attributes, db_rel_attributes, similar_ci, similar_rel,
                similar_attr_ci, similar_attr_rel)

    threshold = ask_for_threshold()

    define_rules(float(threshold), similar_ci, similar_rel,
                 similar_attr_ci, similar_attr_rel)
