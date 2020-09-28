import spacy
import difflib
from colored import fg, bg, attr
import os

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

nlp = spacy.load('en_core_web_lg')


def semantic_similarity(word1, word2):
    w1 = word1.lower()
    w2 = word2.lower()
    s = nlp(w1).similarity(nlp(w2))
    return s


def syntatic_similarity(word1, word2):
    w1 = word1.lower()
    w2 = word2.lower()
    seq1 = difflib.SequenceMatcher(None, w1, w2)
    seq2 = difflib.SequenceMatcher(None, w1, w2)
    d1 = seq1.ratio()
    d2 = seq2.ratio()
    if d1 > d2:
        return d1
    else:
        return d2


def calc_similarity(sem, syn):
    r = sem*0.7 + syn*0.3
    return r


def similarity_degree(word1, word2):
    sem = semantic_similarity(word1, word2)
    syn = syntatic_similarity(word1, word2)
    result = calc_similarity(sem, syn)
    return result
