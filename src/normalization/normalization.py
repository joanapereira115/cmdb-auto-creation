# -*- coding: utf-8 -*-

import re
import string
from nltk.corpus import stopwords
from unit_converter.converter import convert, converts

acronyms_db = {
    'aci': 'application centric infrastructure',
    'ack': 'acknowledgement',
    'acl': 'access control list',
    'adsl': 'asymmetric digital subscriber line',
    'aes': 'advanced encryption standard',
    'ap': 'access point',
    'api': 'application programming interface',
    'arp': 'address resolution protocol',
    'atm': 'asynchronous transfer mode',
    'ban': 'body area network',
    'bgp': 'border gateway protocol',
    'bios': 'basic input/output system',
    'bmc': 'baseboard management controller',
    'bss': 'basic service set',
    'cd': 'compact disc',
    'cd-rom': 'compact disc read-only memory',
    'cdm': 'common data model',
    'chap': 'challenge-handshake authentication protocol',
    'ci': 'configuration item',
    'cidr': 'classless inter-domain routing',
    'cim': 'common information model',
    'cdp': 'cisco discovery protocol',
    'cli': 'command line interpreter',
    'cmdb': 'configuration management database',
    'cms': 'configuration management system',
    'cpe': 'customer premises equipment',
    'cpu': 'central processing unit',
    'crc': 'cyclic redundancy check',
    'csma/ca': 'carrier sense multiple access / collision avoidance',
    'csma/cd': 'carrier sense multiple access / collision detection',
    'csu/dsu': 'channel service unit / data service unit',
    'csv': 'comma-separated values',
    'das': 'direct attached storage',
    'db': 'database',
    'dnms': 'database management system',
    'dce': 'data communications equipment',
    'dec': 'digital equipment corporation',
    'des': 'data encryption standard',
    'dhcp': 'dynamic host configuration protocol',
    'dimm': 'dual in-line memory module',
    'dmtf': 'distributed management task force',
    'dns': 'domain name system',
    'dram': 'dynamic random-access memory',
    'dsl': 'digital subscriber line',
    'dte': 'data terminal equipment',
    'dmi': 'desktop management interface',
    'eha': 'ethernet hardware address ',
    'eigrp': 'enhanced interior gateway routing protocol',
    'eof': 'end of file',
    'ess': 'extended service set',
    'fdb': 'forwarding database',
    'fdp': 'foundry discovery protocol',
    'fcc': 'federal communications commission',
    'fcs': 'frame check sequence',
    'fddi': 'fiber distributed data interface',
    'ftp': 'file transfer protocol',
    'hdd': 'hard disk drive',
    'hdlc': 'high-level data link control',
    'html': 'hypertext markup language',
    'http': 'hypertext transfer protocol',
    'https': 'hypertext transfer protocol secure',
    'icmp': 'internet control message protocol',
    'idf': 'intermediate distribution frame',
    'ids': 'intrusion detection system',
    'ieee': 'institute for electrical and electronic engineers',
    'ietf': 'internet engineering task force',
    'imap': 'internet message access protocol',
    'ip': 'internet protocol',
    'ipv4': 'internet protocol version 4',
    'ipv6': 'internet protocol version 6',
    'ipmi': 'intelligent platform management interface',
    'ips': 'intrusion prevention system',
    'is-is': 'intermediate system-intermediate system',
    'iso': 'international organization for standardization',
    'it': 'information technology',
    'itil': 'information technology infrastructure library',
    'itsm': 'information technology service management',
    'isdn': 'integrated services digital network',
    'isp': 'internet service provider',
    'jmx': 'java management extensions',
    'json': 'javascript object notation',
    'lacp': 'link aggregation control protocol',
    'lan': 'local area network',
    'lapf': 'link-access procedure for frame relay',
    'ldap': 'lightweight directory access protocol',
    'llc': 'logical link control',
    'lldp': 'link layer discovery protocol',
    'mac': 'media access control',
    'mam': 'media access management',
    'man': 'metropolitan area network',
    'mdf': 'main distribution frame',
    'mib': 'management information base',
    'mpls': 'multiprotocol label switching',
    'mtu': 'maximum Transmission Unit',
    'nac': 'network access control',
    'nas': 'network attached storage',
    'nat': 'network address translation',
    'ndp': 'neighbor discovery protocol',
    'nfs': 'network file system',
    'nic': 'network interface card',
    'os': 'operating system',
    'osi': 'open system interconnection',
    'ospf': 'open shortest path first',
    'pan': 'personal area network',
    'pap': 'password authentication protocol',
    'pat': 'port address translation',
    'pc': 'personal computer',
    'pdu': 'protocol data unit',
    'php': 'hypertext preprocessor',
    'ppp': 'point-to-point protocol',
    'ram': 'random access memory',
    'rarp': 'reverse address resolution protocol',
    'rdp': 'remote desktop protocol',
    'rest': 'representational state transfer',
    'rip': 'routing information protocol',
    'rom': 'read-only memory',
    'rpc': 'remote procedure call',
    'rstp': 'rapid spanning tree protocol',
    'rtp': 'real-time transport protocol',
    'san': 'storage area network',
    'sccm': 'system center configuration manager',
    'sdlc': 'synchronous data link control',
    'sdn': 'software defined network',
    'smtp': 'simple mail transfer protocol',
    'sna': 'systems network architecture',
    'snmp': 'simple network management protocol',
    'sram': 'static random access memory',
    'span': 'switched port analyzer',
    'sql': 'structured query language',
    'ssd': 'solid-state drive',
    'ssh': 'secure shell',
    'ssid': 'service set identifier',
    'ssl': 'secure sockets layer',
    'stp': 'spanning tree protocol',
    'svs': 'service value system',
    'syn': 'synchronization',
    'taddm': 'tivoli application dependency discovery manager',
    'tcp': 'transmission control protocol',
    'tpl': 'template file',
    'ttl': 'time to live',
    'udp': 'user datagram protocol',
    'ucs': 'unified computing system',
    'uml': 'unified modeling language',
    'ups': 'uninterruptible power source',
    'url': 'uniform resource locator',
    'usb': 'universal serial bus',
    'utp': 'unshielded twisted pair',
    'uuid': 'universally unique identifier',
    'vlan': 'virtual local area network',
    'vpn': 'virtual private network',
    'wan': 'wide area netwok',
    'winrm': 'windows remote management',
    'wmi': 'windows management instrumentation',
    'wpa': 'wi-fi protected access',
    'www': 'world wide web',
    'xdp': 'express data path',
    'xml': 'extensible markup language',
    'vrrp': 'virtual router redundancy protocol',
    'net': 'network',
    'gpu': 'graphics processing unit',
    'sd': 'secure digital'
}


def remove_special_chars(text):
    """
    Removes multiple spaces, paragraphs and tabs and spaces, paragraphs and tabs at the beginning and at the end of the text.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    # remove characters at the begin
    text = re.sub(r"^\s+", "", text)
    text = re.sub(r"^\n+", "", text)
    text = re.sub(r"^\t+", "", text)
    # remove characters at the end
    text = re.sub(r"\s+$", "", text)
    text = re.sub(r"\n+$", "", text)
    text = re.sub(r"\t+$", "", text)
    # remove multiple characters
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\t+", " ", text)
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
    words = str(text).split()
    new_words = []
    for w in words:
        snake_case = re.search("_", w)
        kebab_case = re.search("-", w)
        camelOrPascalCase = re.search(r"[a-z][A-Z]", w)
        if snake_case != None:
            w = re.sub(r'_', r' ', str(w))
        elif kebab_case != None:
            w = re.sub(r'-', r' ', str(w))
        elif camelOrPascalCase != None:
            text = re.sub(r'([a-z])([A-Z])', r'\1 \2', str(w))
            w = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', str(text))
        new_words.append(w)
    res = " ".join(new_words)
    return res


def remove_punctuation(text):
    """
    Removes punctuation from text.
    Does not remove '.' and ':' from addresses (e.g.: 10.1.1.1).

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    words = str(text).split()
    new_words = []
    for w in words:
        ipv6 = re.search(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', w)
        ipv4 = re.search(
            r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])', w)
        mac = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', w)

        if ipv6 == None and ipv4 == None and mac == None:
            w = ''.join([c for c in w if c not in string.punctuation])
        new_words.append(w)

    res = " ".join(new_words)
    return res


def remove_stop_words(text):
    """
    Removes stop words of the text.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    sw = stopwords.words("english")
    text = ' '.join([word for word in str(text).split() if word not in sw])
    return text


def acronym(text):
    """
    Replaces the acronyms present in the text with its extended version.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    result = ' '.join([acronyms_db.get(i, i) for i in str(text).split()])
    if re.match(r"media access control operating system x", result, re.IGNORECASE):
        result = re.sub(
            "media access control operating system x", "mac os x", result)
    if re.match(r"media access control operating system", result, re.IGNORECASE):
        result = re.sub(
            "media access control operating system", "mac os", result)
    if re.match(r"operating system x", result, re.IGNORECASE):
        result = re.sub("operating system x", "os x", result)
    return result


def parse_text_to_compare(text):
    """
    Cleans the text for comparasions.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    text = str(text)
    text = remove_style_case(text)
    text = remove_special_chars(text)
    text = remove_punctuation(text)
    text = text.lower()
    text = acronym(text)
    text = remove_stop_words(text)
    return text
