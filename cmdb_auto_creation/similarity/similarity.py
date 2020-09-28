# -*- coding: utf-8 -*-

from syntatic_matching import syntatic_matching
from semantic_matching import semantic_matching


def calculate_similarity(text1, text2):
    """
    Calculates the similarity of two terms.

    It calculates the syntatic similarity between the two terms.
    If it's more than 0.99, returns that value.
    If not, calculates the semantic similarity between the two terms and returns that value.

    Parameters
    ----------
    text1 : string
        The first term we want to compare.

    text2 : string
        The second term which we want to compare the first one with.

    Returns
    -------
    string
        The value, between 0 and 1, that represents the similarity between the two terms.

    """
    syn_value = syntatic_matching.syntatic_coeficient(text1, text2)
    if syn_value > 0.99:
        return syn_value
    else:
        sem_value = semantic_matching.semantic_coeficient(text1, text2)
        if sem_value > syn_value:
            return sem_value
        else:
            return syn_value
