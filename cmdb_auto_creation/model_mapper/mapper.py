# -*- coding: utf-8 -*-

import os
from colored import fg, bg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex

from cmdb_processor import cmdb_data_model
from db_processor import db_data_model
from .mapping import calc_similars, select_most_similar
from .transformation_rules import rules

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


def calculate_attribute_similarity(similars, cmdb_attributes, db_attributes):
    attr_similarity = {}
    for db_t in similars:
        cmdb_t = list(similars[db_t].keys())[0]
        # {'Vendor': 'vendor', 'uuid': 'uuid', 'serial_number': 'serial number', 'name': 'name', 'description': 'description', 'status': 'status', 'mac_address': 'mac address', 'has_ipv4': 'ipv4', 'has_ipv6': 'ipv6'}
        db_attrs = db_attributes.get(db_t)
        cmdb_attrs = cmdb_attributes.get(cmdb_t)
        if db_attrs != None and cmdb_attrs != None:
            attr_similarity[cmdb_t] = calculate_class_similarity(
                db_attrs, cmdb_attrs)
        else:
            attr_similarity[cmdb_t] = {}
    return attr_similarity


def calculate_class_similarity(cmdb_types, app_types):
    cmdb_tp = {cmdb_types.get(x): x for x in cmdb_types}
    app_tp = {app_types.get(y): y for y in app_types}
    class_similarity = calc_similars(cmdb_tp, app_tp)
    return class_similarity


def present_map(cmdb_ci_types, db_ci_types, cmdb_rel_types, db_rel_types, cmdb_ci_attributes, db_ci_attributes, cmdb_rel_attributes, db_rel_attributes, similar_ci, similar_rel, similar_attr_ci, similar_attr_rel):
    print("\n===============================================================================================================================================================================")
    print("Configuration Item Types Mapping")
    for db_ci in similar_ci:
        print("==============================================================================================================================================================================")
        cmdb_ci = list(similar_ci[db_ci].keys())[0]
        sim = similar_ci.get(db_ci).get(cmdb_ci)
        print("|| " + green + cmdb_ci + reset + " \t || \t " + green + cmdb_ci_types.get(cmdb_ci) + reset +
              " \t || \t " + blue + db_ci + reset + " \t || \t " + blue + db_ci_types.get(db_ci) + reset + " \t || \t " + red + str(sim) + reset + " ||")
        atrs = similar_attr_ci.get(cmdb_ci)
        print("******************************************************************************************************************************************************************************")
        for cmdb_at in atrs:
            db_at = list(atrs.get(cmdb_at).keys())[0]
            sim = atrs.get(cmdb_at).get(db_at)
            print("|| " + green + cmdb_at + reset + " \t || \t " + green + cmdb_ci_attributes.get(cmdb_ci).get(cmdb_at) + reset +
                  " \t || \t " + blue + db_at + reset + " \t || \t " + blue + db_ci_attributes.get(db_ci).get(db_at) + reset + " \t || \t " + red + str(sim) + reset + " ||")
            print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    print("===============================================================================================================================================================================")
    print("Relationship Types Mapping")
    for db_rel in similar_rel:
        print("===============================================================================================================================================================================")
        cmdb_rel = list(similar_rel[db_rel].keys())[0]
        sim = similar_rel.get(db_rel).get(cmdb_rel)
        print("|| " + green + cmdb_rel + reset + " \t || \t " + green + cmdb_rel_types.get(cmdb_rel) + reset +
              " \t || \t " + blue + db_rel + reset + " \t || \t " + blue + db_rel_types.get(db_rel) + reset + " \t || \t " + red + str(sim) + reset + " ||")
        atrs = similar_attr_rel.get(cmdb_rel)
        print("*******************************************************************************************************************************************************************************")
        for cmdb_at in atrs:
            db_at = list(atrs.get(cmdb_at).keys())[0]
            sim = atrs.get(cmdb_at).get(db_at)
            cmdb_at_desc = cmdb_rel_attributes.get(cmdb_rel)
            if cmdb_at_desc != None:
                cmdb_at_desc = cmdb_at_desc.get(cmdb_at)
            db_at_desc = db_rel_attributes.get(db_rel)
            if db_at_desc != None:
                db_at_desc = db_at_desc.get(db_at)
            print("|| " + green + cmdb_at + reset + " \t || \t " + green + str(cmdb_at_desc) + reset + " \t || \t " +
                  blue + db_at + reset + " \t || \t " + blue + str(db_at_desc) + reset + " \t || \t " + red + str(sim) + reset + " ||")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    print(green + "** Green text represents terms associated with the CMDB **")
    print(blue + "** Blue text represents terms associated with the database **")
    print(red + "** Red text represents the similarity coeficient calculated **\n" + reset)


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


def ask_for_threshold():
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

    print(rules)


def run_mapper():
    print(blue + "\n>>> " + reset + "Executing the model mapper...\n")

    # {"CI type": "description", ...}
    cmdb_ci_types = cmdb_data_model.cmdb_data_model.get("ci_types")
    # {"relationship type": "description", ...}
    cmdb_rel_types = cmdb_data_model.cmdb_data_model.get("rel_types")
    # {"CI type": {"attribute": "description", ...}, ...}
    cmdb_ci_attributes = cmdb_data_model.cmdb_data_model.get("ci_attributes")
    # {"relationship type": {"attribute": "description", ...}, ...}
    cmdb_rel_attributes = cmdb_data_model.cmdb_data_model.get("rel_attributes")

    # {"CI type": "description", ...}
    db_ci_types = db_data_model.db_data_model.get("ci_types")
    # {"relationship type": "description", ...}
    db_rel_types = db_data_model.db_data_model.get("rel_types")
    # {"CI type": {"attribute": "description", ...}, ...}
    db_ci_attributes = db_data_model.db_data_model.get("ci_attributes")
    # {"relationship type": {"attribute": "description", ...}, ...}
    db_rel_attributes = db_data_model.db_data_model.get("rel_attributes")

    print(blue + "\n>>> " + reset +
          "Calculating configuration item types similarity...")
    ci_similarity = calculate_class_similarity(cmdb_ci_types, db_ci_types)

    print(blue + "\n>>> " + reset + "Calculating relationship types similarity...")
    rel_similarity = calculate_class_similarity(cmdb_rel_types, db_rel_types)

    # {'Portable Computer': {'C__OBJTYPE__SERVER': 0.8181818181818182}, 'Router': {'C__OBJTYPE__ROUTER': 1.0}}
    similar_ci = select_most_similar(ci_similarity)
    # {'Network connection': {'C__RELATION_TYPE__NET_CONNECTIONS': 0.954378751269652}}
    similar_rel = select_most_similar(rel_similarity)

    print(blue + "\n>>> " + reset +
          "Calculating configuration item attributes similarity...")
    attr_ci_similarity = calculate_attribute_similarity(
        similar_ci, cmdb_ci_attributes, db_ci_attributes)

    print(blue + "\n>>> " + reset +
          "Calculating relationship attributes similarity...")
    attr_rel_similarity = calculate_attribute_similarity(
        similar_rel, cmdb_rel_attributes, db_rel_attributes)

    similar_attr_ci = {x: select_most_similar(
        attr_ci_similarity.get(x)) for x in attr_ci_similarity}
    # {'C__RELATION_TYPE__NET_CONNECTIONS': {'changes': {'Speed': 0.875}}}
    similar_attr_rel = {y: select_most_similar(
        attr_rel_similarity.get(y)) for y in attr_rel_similarity}

    present_map(cmdb_ci_types, db_ci_types, cmdb_rel_types, db_rel_types, cmdb_ci_attributes, db_ci_attributes, cmdb_rel_attributes, db_rel_attributes, similar_ci, similar_rel,
                similar_attr_ci, similar_attr_rel)

    threshold = ask_for_threshold()

    define_rules(float(threshold), similar_ci, similar_rel,
                 similar_attr_ci, similar_attr_rel)
