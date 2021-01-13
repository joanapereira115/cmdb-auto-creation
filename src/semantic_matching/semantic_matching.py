# -*- coding: utf-8 -*-

from normalization import normalization

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import spacy
from stringcase import snakecase
from stringcase import sentencecase
import os

os.environ["SPACY_WARNING_IGNORE"] = "W008"

nlp = spacy.load("en_core_web_lg")


def semantic_coeficient(text1, text2):
    """
    Calculates the semantic similarity of two terms.

    It calculates the maximum similarity using the Wu-Palmer similarity, that returns a score denoting how similar two word senses are, 
    based on the depth of the two senses in the taxonomy and that of their Least Common Subsumer (most specific ancestor node). 
    Then calculates the similarity between the two terms using the spacy module.
    It returns the biggest value between the two.

    Parameters
    ----------
    text1 : string
        The first term we want to compare.

    text2 : string
        The second term which we want to compare with the first one.

    Returns
    -------
    int
        The value, between 0 and 1, that represents the biggest value of semantic similarity calculated between the two terms.
    """
    if text1 != None and text2 != None:
        t1 = snakecase(normalization.parse_text_to_compare(text1))
        t2 = snakecase(normalization.parse_text_to_compare(text2))
        maxi = 0
        syn1 = wn.synsets(t1)
        syn2 = wn.synsets(t2)
        for s1 in syn1:
            for s2 in syn2:
                new = wn.wup_similarity(s1, s2)
                if new != None:
                    if new > maxi:
                        maxi = new
        new_spacy = nlp(text1).similarity(nlp(text2))
        if new_spacy > maxi:
            maxi = new_spacy
        return maxi
    else:
        return 0
