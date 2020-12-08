# -*- coding: utf-8 -*-

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
    int
        The value, between 0 and 1, that represents the syntatic similarity between the two terms.

    """
    if text1 != "" and text2 != "" and text1 != None and text2 != None:
        t1 = normalization.parse_text_to_compare(text1)
        t2 = normalization.parse_text_to_compare(text2)
        if t1 != "" and t2 != "":
            text = [t1, t2]
            try:
                vectorizer = CountVectorizer().fit_transform(text)
                vectors = vectorizer.toarray()
                csims = cosine_similarity(vectors)
                csim = csims[0][1]
                return csim
            except:
                return 0
    return 0
