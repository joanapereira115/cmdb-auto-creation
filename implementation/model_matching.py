#!/usr/bin/env python3

import difflib

cim_model_classes = {
	"managed element" : ["caption", "description", "element name", "instance id", "generation"],
	"managed system element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status"],
	"logical element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status"],
	"enabled logical element" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states"],
	"filesystem" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "creation class name", "name", "root", "block size", "filesystem size", "available space", "read only", "encryption method", "compression method", "case sensitive", "case preserved", "codeset", "max file name length", "cluster size", "filesystem type", "persistence type", "other persistence type", "number of files", "is fixed size"],
	"operating system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "creation class name", "name", "os type", "other type description", "version", "last boot up time", "local datetime", "current timezone", "number of licensed users", "number of users", "number of processes", "max number of processes", "total swap space size", "total virtual memory size", "free virtual memory", "free physical memory", "total visible memory size", "size stored in paging files", "free space in paging files", "max process memory size", "distributed", "max processes per user", "manufacturer", "family", "os classification"],
	"alocated logical system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate"],
	"system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate", "creation class name", "name", "name format", "primary owner name",  "primary owner contact", "roles", "other identifying info", "identifying descriptions"],
	"computer system" : ["caption", "description", "element name", "instance id", "generation", "install date", "name", "operational status", "health state", "primary status", "detailed status", "operating status", "communication status", "enabled state", "other enabled state", "requested state", "enabled default", "time of last state change", "transitioning to state", "available requested states", "allocationstate", "creation class name", "name", "name format", "primary owner name",  "primary owner contact", "roles", "other identifying info", "identifying descriptions", "name format", "dedicated", "other dedicated descriptions", "reset capability", "system id"],
}

cim_model_relationships = {}

idoit_model_classes = {
	"Operating system" : ["Title", "Category", "Purpose", "Condition", "CMDB status", "Object ID", "Object type", "SYSID", "Creation date", "Date of change", "Tags", "Description", "Specification", "Manufacturer", "Installation", "Registration key", "Install path"]
}

idoit_model_relationships = {}

strong_mapping = {}
weak_mapping = {}

for x in idoit_model_classes:
	rate = 0
	idoit = x
	cim = None
	for y in cim_model_classes:
		seq = difflib.SequenceMatcher(None,idoit.lower(),y.lower())
		r = seq.ratio()*100
		if r > rate:
			cim = y
			rate = r
	if rate >= 75:
		strong_mapping[idoit] = cim
	elif rate >= 50:
		weak_mapping[idoit] = cim
print("STRONG: " + str(strong_mapping))
print("WEAK: " + str(weak_mapping))

attr = {}

for z in strong_mapping:
	cim = strong_mapping[z]
	idoit = z
	atrate = 0
	atrcim = None
	for a in idoit_model_classes[idoit]:
		atr = a
		for k in cim_model_classes[cim]:
			seq = difflib.SequenceMatcher(None,atr.lower(),k.lower())
			r2 = seq.ratio()*100
			if r2 > atrate:
				atrcim = k
				atrate = r2
		if atrate >= 75:
			attr[atr] = atrcim
print("ATTR: " + str(attr))
			


