# -*- coding: utf-8 -*-

from syntatic_matching import syntatic_matching
from semantic_matching import semantic_matching
import numpy


def calculate_similarity(text1, text2):
    """
    Calculates the similarity of two terms.

    It calculates the syntatic similarity between the two terms.
    If it's equal to 1, returns that value.
    If not, calculates the semantic similarity between the two terms and returns the biggest value between the semantic and syntatic similarity.

    Parameters
    ----------
    text1 : string
        The first term we want to compare.

    text2 : string
        The second term which we want to compare the first one with.

    Returns
    -------
    int
        The value, between 0 and 1, that represents the similarity between the two terms.
    """
    if text1 != "" and text2 != "" and text1 != None and text2 != None:
        syn_value = syntatic_matching.syntatic_coeficient(text1, text2)
        if syn_value == 1:
            return numpy.clip(syn_value, 0, 1)
        else:
            sem_value = semantic_matching.semantic_coeficient(text1, text2)
            if sem_value > syn_value:
                return numpy.clip(sem_value, 0, 1)
            else:
                return numpy.clip(syn_value, 0, 1)
    else:
        return 0
