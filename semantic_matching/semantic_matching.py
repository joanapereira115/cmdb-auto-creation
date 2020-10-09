# -*- coding: utf-8 -*-

from normalization import normalization

import nltk
from nltk.corpus import stopwords
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
    string
        The value, between 0 and 1, that represents the biggest value of semantic similarity calculated between the two terms.

    """
    if text1 != None and text2 != None:
        t1 = snakecase(normalization.clean_text(text1))
        t2 = snakecase(normalization.clean_text(text2))
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


"""
def tokenization(text):
    text_doc = nlp(text)
    # token.idx, token.text_with_ws, token.is_alpha, token.is_punct, token.is_space, token.shape_, token.is_stop
    tokens = [token.text for token in text_doc if not token.is_stop]
    return tokens


def entity_detection(text):
    text_doc = nlp(text)
    entities = [e.text for e in text_doc.ents]
    return entities


def get_synonyms(word):
    word = snakecase(word)
    word.lower()
    res = []
    for ss in wn.synsets(word):
        syn = ss.lemma_names()
        for s in syn:
            if s not in res:
                res.append(s)
    new_res = []
    for r in res:
        new_res.append(sentencecase(r).lower())
    return new_res


def get_similars(word):
    res = []
    for ss in wn.synsets(word):
        syn = ss.similar_tos()
        for s in syn:
            if s not in res:
                res.append(s)
    return res


def get_antonyms(word):
    res = []
    for ss in wn.synsets(word):
        lemmas = ss.lemmas()
        for lemma in lemmas:
            lemma_antonyms = lemma.antonyms()
            for lemma_antonym in lemma_antonyms:
                antonyms = wn.lemma_from_key(
                    lemma_antonym.key()).synset().lemma_names()
                for antonym in antonyms:
                    if antonym not in res:
                        res.append(antonym)
    return res
"""
