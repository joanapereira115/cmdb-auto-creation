# -*- coding: utf-8 -*-

import re
import string
from stringcase import sentencecase
from nltk.corpus import stopwords

acronyms_db = {
    'os': 'operating system',
    'ip': 'internet protocol',
    'mac': 'media access control',
    'tcp': 'transmission control protocol',
    'itil': 'information technology infrastructure library',
    'cmdb': 'configuration management database',
    'ci': 'configuration item',
    'iso': 'international organization for standardization',
    'icmp': 'internet control message protocol',
    'snmp': 'simple network management protocol',
    'lan': 'local area network',
    'wan': 'wide area netwok',
    'vpn': 'virtual private network',
    'fdb': 'forwarding database',
    'arp': 'address resolution protocol',
    'lldp': 'link layer discovery protocol',
    'mib': 'management information base',
    'udp': 'user datagram protocol',
    'stp': 'spanning tree protocol',
    'span': 'switched port analyzer',
    'rdp': 'remote desktop protocol',
    'api': 'application programming interface',
    'rest': 'representational state transfer',
    'ti': 'tecnologias da informação',
    'itsm': 'it service management',
    'osi': 'open system interconnection',
    'ssh': 'secure shell',
    'wmi': 'windows management instrumentation',
    'winrm': 'windows remote management',
    'cdp': 'cisco discovery protocol',
    'jmx': 'java management extensions',
    'sql': 'structured query language',
    'dns': 'domain name system',
    'nfs': 'network file system',
    'ldap': 'lightweight directory access protocol',
    'taddm': 'tivoli application dependency discovery manager',
    'ssd': 'solid-state drive',
    'das': 'direct attached storage',
    'nas': 'network attached storage',
    'san': 'storage area network',
    'cpu': 'central processing unit',
    'bios': 'basic input/output system',
    'json': 'javascript object notation',
    'http': 'hypertext transfer protocol',
    'https': 'hypertext transfer protocol secure',
    'xml': 'extensible markup language',
    'cim': 'common information model',
    'svs': 'service value system',
    'dmtf': 'distributed management task force',
    'uml': 'unified modeling language',
    'rpc': 'remote procedure call',
    'cms': 'configuration management system',
    'cidr': 'classless inter-domain routing',
    'ttl': 'time to live',
    'csv': 'comma-separated values',
    'php': 'hypertext preprocessor',
    'xdp': 'express data path',
    'fdp': 'foundry discovery protocol',
    'ospf': 'open shortest path first',
    'bgp': 'border gateway protocol',
    'ndp': 'neighbor discovery protocol',
    'ups': 'uninterruptible power source',
    'man': 'metropolitan area network',
    'ban': 'body area network',
    'pan': 'personal area network',
    'ap': 'access point',
    'hdd': 'hard disk drive',
    'sgbd': 'sistemas de gestão de base de dados',
    'bd': 'bases de dados',
    'html': 'hypertext markup language',
    'url': 'uniform resource locator',
    'ssl': 'secure sockets layer',
    'vlan': 'virtual local area network',
    'ucs': 'unified computing system',
    'aci': 'application centric infrastructure',
    'sdn': 'software defined network',
    'ipmi': 'intelligent platform management interface',
    'bmc': 'baseboard management controller',
    'sccm': 'system center configuration manager',
    'ftp': 'file transfer protocol',
    'uuid': 'universally unique identifier',
    'cdm': 'common data model',
    'tpl': 'template file',
    'is-is': 'intermediate system-intermediate system',
    'rip': 'routing information protocol'
}


def remove_spaces(text):
    """
    Removes multiple spaces and spaces at the beginning and at the end of the text.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    # remove spaces at the begin
    text = re.sub(r"^\s+", "", text)
    # remove spaces at the end
    text = re.sub(r"\s+$", "", text)
    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text


def remove_style_case(text):
    """
    Checks if a text has words in snake, kebab, pascal or camel case, and removes the formatting.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    words = text.split()
    new_words = []
    for w in words:
        snake_case = re.search("_", w)
        if snake_case != None:
            w = sentencecase(w)
        kebab_case = re.search("-", w)
        if kebab_case != None:
            w = sentencecase(w)
        camelOrPascalCase = re.search(r"[a-z][A-Z]", w)
        if camelOrPascalCase != None:
            w = sentencecase(w)
        new_words.append(w)
    res = " ".join(new_words)
    return res

# TODO: não remover : quando é um endereço ipv6


def remove_punctuation(text):
    """
    Removes punctuation from text.

    Does not remove '.' and ':' if they are separating numbers (e.g.: 10.1.1.1).

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.

    """
    words = text.split()
    new_words = []
    for w in words:
        numbers = re.search(r"\d\.\d", w) or re.search(r"\d\:\d", w)
        if numbers:
            w = ''.join([c for c in w if c not in string.punctuation.replace(
                '.', '').replace(':', '')])
        else:
            w = ''.join([c for c in w if c not in string.punctuation])
        new_words.append(w)
    res = " ".join(new_words)
    return res


def remove_stop_words(text):
    sw = stopwords.words("english")
    text = ' '.join([word for word in text.split() if word not in sw])
    return text


def acronym(text):
    return ' '.join([acronyms_db.get(i, i) for i in text.split()])


def clean_text(text):
    text = remove_style_case(text)
    text = remove_spaces(text)
    text = remove_punctuation(text)
    text = text.lower()
    text = acronym(text)
    text = remove_stop_words(text)
    return text


"""
separate numbers from units
    text = re.sub(r"([0-9]+\.?|,?[0-9]+?)([a-zA-Z]+)[^:]",
                  r"\1 \2", text, re.DOTALL)
"""
