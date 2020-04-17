#!/usr/bin/env python3

import difflib
import spacy 
import operator

#Levenshtein distance
#import nltk
#print(nltk.edit_distance("Operating system", "operating system"))

#from sematch.semantic.similarity import WordNetSimilarity
#wns = WordNetSimilarity()
#s = wns.word_similarity(w1, w2, 'li')

nlp = spacy.load('en_core_web_lg')

cim_model_classes = [
	#"managed element", 
    #"managed system element",
    #"logical element",
    #"enabled logical element",
    "filesystem",
    "operating system"#,
    #"alocated logical system",
    #"system",
    #"computer system"
]

cim_model_atr = {
	#"managed element" : ["caption", "description", "element name", "instance id", "generation"],
	#"managed system element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status"],
	#"logical element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status"],
	#"enabled logical element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states"],
	"filesystem" : ["caption", "description", "element name"],#, "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "creation class name", "name", "root", "block size", "filesystem size", "available space", "read only", "encryption method", "compression method", "case sensitive", "case preserved", "codeset", "max file name length", "cluster size", "filesystem type", "persistence type", "other persistence type", "number of files", "is fixed size"],
	"operating system" : 
        ["caption", "description", 
        #"element name", "instance id", "generation", "install date", "name", 
        "operational status"#, "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "creation class name", "name", "os type", "other type description", "version", "last boot up time", "local datetime", "current timezone", "number of licensed users", "number of users", "number of processes", "max number of processes", "total swap space size", "total virtual memory size", "free virtual memory", "free physical memory", "total visible memory size", "size stored in paging files", "free space in paging files", "max process memory size", "distributed", "max processes per user", "manufacturer", "family", "os classification"
        ]#,
	#"alocated logical system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate"],
	#"system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate", "creation class name", "name", "name format", "primary owner name",  "primary owner contact", "roles", "other identifying info", "identifying descriptions"],
	#"computer system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate", "creation class name", "name", "name format", "primary owner name",  "primary owner contact", "roles", "other identifying info", "identifying descriptions", "name format", "dedicated", "other dedicated descriptions", "reset capability", "system id"],
}

idoit_model_classes = [
    #"Air Condition System", "Appliance", "Application", "Building", "Client", "Host", "Server", "Workplace"
	"Operating system", "File"
]

idoit_model_atr = {
	"Operating system" : 
        ["Title", 
        "Category", 
        #"Purpose", "Condition", 
        "CMDB status"],
        #, "Object ID", "Object type", "SYSID", "Creation date", "Date of change", "Tags", "Description", "Specification", "Manufacturer", "Installation", "Registration key", "Install path"]
    "File" : ["Title", "CMDB status", "Description"]
}

def semantic_similarity(word1,word2):
    w1 = word1.lower()
    w2 = word2.lower()
    s = nlp(w1).similarity(nlp(w2))
    return s

def syntatic_similarity(word1,word2):
    w1 = word1.lower()
    w2 = word2.lower()
    seq = difflib.SequenceMatcher(None,w1,w2)
    d = seq.ratio()
    return d

def calc_similarity(sem, syn):
    r = sem*0.7 + syn*0.3
    return r

def calc_classes_similarity(cmdb, cim):
    res = {}
    for c1 in cmdb:
        l = {}
        for c2 in cim:
            l[c2] = calc_similarity(semantic_similarity(c1,c2), syntatic_similarity(c1,c2))
        l_sort = dict(sorted(l.items(), key=operator.itemgetter(1), reverse=True))
        res[c1] = l_sort
    return res

def select_most_similar(calculated_matches):
    m = []
    v = {}
    for key in calculated_matches:
        values = calculated_matches.get(key)
        fst = list(values.keys())[0]
        if fst not in m:
            m.append(fst)
            v[fst] = {key: values.get(fst)}
        else:
            prev = v.get(fst).get(list(v.get(fst).keys())[0])
            if values.get(fst) > prev:
                k = calculated_matches.get(list(v.get(fst).keys())[0])
                ky = str(list(k.keys())[0])
                del k[ky]
                return select_most_similar(calculated_matches)
    return v

def select_matches(similars):
    #possível verificação dos valores
    res = {}
    for k in similars:
        res[k] = list(similars.get(k).keys())[0]
    return res

def calculate_average(similars):
    total = 0
    count = 0
    for k in similars:
        count += 1
        total += similars.get(k).get(list(similars.get(k).keys())[0])
    return total/float(count)

def calculate_atr_weight(elvalue, atrvalue):
    res = elvalue * 0.7 + atrvalue * 0.3
    return res

def calc_atr_similarity(matches, cmdb_atr, cim_atr):
    res = {}
    for cmdb_elm in matches:
        values = matches[cmdb_elm]
        for cim_elm in values:
            cmdb_atrs = cmdb_atr[cmdb_elm]
            cim_atrs = cim_atr[cim_elm]
            matching = calc_classes_similarity(cmdb_atrs, cim_atrs)
            similars = select_most_similar(matching)
            print(similars)
            #maps = select_matches(similars)
            avg = calculate_average(similars)
            tot = calculate_atr_weight(values[cim_elm], avg)
            values[cim_elm] = tot
    print(select_matches(matches))

calc_atr_similarity(calc_classes_similarity(idoit_model_classes, cim_model_classes), idoit_model_atr, cim_model_atr)