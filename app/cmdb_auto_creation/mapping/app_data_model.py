# definir o modelo de dados com base nos objetos descobertos (aceder à BD)

import requests
from urllib.parse import quote
from discovery import normalization

prefix = 'prefix : <http://www.semanticweb.org/joana/ontologies/2020/cmdb#>'
db_url = 'http://192.168.1.72:7200/repositories/cmdb_creation'

app_data_model = {
    #
    "ci_types": {},
    #
    "rel_types": {},
    #
    "ci_types_attributes": {},
    "rel_types_attributes": {}
}


def execQuery(query):
    encoded = quote(prefix + "\n" + query)
    url = db_url + "?query=" + encoded

    s = requests.Session()
    response = s.get(url)
    return response


def get_ci_types():
    query_string = "select distinct ?o where {?s rdf:type :Element. ?s :ci_type ?o.}"
    r = execQuery(query_string)
    return r.text.split()[1:]


def get_relation_types():
    query_string = "select distinct ?o where {?s rdf:type :Relationship. ?s :rel_type ?o.}"
    r = execQuery(query_string)
    return r.text.split()[1:]


def get_ci_attributes():
    query_string = "select distinct ?s where {?s rdfs:domain :Element .}"
    r = execQuery(query_string)
    return r.text.split()[1:]


def get_rel_attributes():
    query_string = "select distinct ?s where {?s rdfs:domain :Relationship .}"
    r = execQuery(query_string)
    return r.text.split()[1:]


def process_data_model():
    ci_types = get_ci_types()
    rel_types = get_relation_types()
    ci_attributes = get_ci_attributes()
    rel_attributes = get_rel_attributes()

    new_ci_types = {}
    for x in ci_types:
        new = normalization.normalize(x)
        new_ci_types[new] = x

    new_rel_types = {}
    for y in rel_types:
        new = normalization.normalize(y)
        new_rel_types[new] = y

    new_ci_attributes = {}
    for w in ci_attributes:
        if w.startswith("http://www.semanticweb.org/joana/ontologies/2020/cmdb#"):
            w = w[len("http://www.semanticweb.org/joana/ontologies/2020/cmdb#"):]
        new = normalization.normalize(w)
        new_ci_attributes[new] = w

    new_rel_attributes = {}
    for z in rel_attributes:
        if z.startswith("http://www.semanticweb.org/joana/ontologies/2020/cmdb#"):
            z = z[len("http://www.semanticweb.org/joana/ontologies/2020/cmdb#"):]
        new = normalization.normalize(z)
        new_rel_attributes[new] = z

    app_data_model["ci_types"] = new_ci_types
    app_data_model["rel_types"] = new_rel_types
    app_data_model["ci_types_attributes"] = new_ci_attributes
    app_data_model["rel_types_attributes"] = new_rel_attributes

    f = open("app_data_model.txt", "w")
    f.write(str(app_data_model))
    f.write("\n")

    return app_data_model
