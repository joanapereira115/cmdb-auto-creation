# -*- coding: utf-8 -*-

import difflib
from normalization import normalization
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def syntatic_coeficient(text1, text2):
    """
    Calculates the syntatic similarity of two terms using cosine similarity.

    Parameters
    ----------
    text1 : string
        The first term we want to compare.

    text2 : string
        The second term which we want to compare with the first one.

    Returns
    -------
    string
        The value, between 0 and 1, that represents the syntatic similarity between the two terms.

    """
    t1 = normalization.clean_text(text1)
    t2 = normalization.clean_text(text2)
    text = [t1, t2]
    vectorizer = CountVectorizer().fit_transform(text)
    vectors = vectorizer.toarray()
    csims = cosine_similarity(vectors)
    csim = csims[0][1]
    return csim
