# -*- coding: utf-8 -*-

import re
import string
from stringcase import sentencecase
from nltk.corpus import stopwords


def remove_spaces(text):
    """
    Removes multiple spaces and spaces at the beginning and at the end of the text.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    # remove spaces at the begin
    text = re.sub(r"^\s+", "", text)
    # remove spaces at the end
    text = re.sub(r"\s+$", "", text)
    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text


def remove_style_case(text):
    """
    Checks if a text has words in snake, kebab, pascal or camel case, and removes the formatting.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    words = text.split()
    new_words = []
    for w in words:
        snake_case = re.search("_", w)
        if snake_case != None:
            w = sentencecase(w)
        kebab_case = re.search("-", w)
        if kebab_case != None:
            w = sentencecase(w)
        camelOrPascalCase = re.search(r"[a-z][A-Z]", w)
        if camelOrPascalCase != None:
            w = sentencecase(w)
        new_words.append(w)
    res = " ".join(new_words)
    return res


def remove_punctuation(text):
    """
    Removes punctuation from text.

    Does not remove '.' and ':' if they are separating numbers (e.g.: 10.1.1.1).

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    words = text.split()
    new_words = []
    for w in words:
        numbers = re.search(r"\d\.\d", w) or re.search(r"\d\:\d", w)
        if numbers:
            w = ''.join([c for c in w if c not in string.punctuation.replace(
                '.', '').replace(':', '')])
        else:
            w = ''.join([c for c in w if c not in string.punctuation])
        new_words.append(w)
    res = " ".join(new_words)
    return res


def remove_stop_words(text):
    sw = stopwords.words("english")
    text = ' '.join([word for word in text.split() if word not in sw])
    return text


def clean_text(text):
    text = remove_style_case(text)
    text = remove_spaces(text)
    text = remove_punctuation(text)
    text = text.lower()
    text = remove_stop_words(text)
    return text


"""
separate numbers from units
    text = re.sub(r"([0-9]+\.?|,?[0-9]+?)([a-zA-Z]+)[^:]",
                  r"\1 \2", text, re.DOTALL)
"""
