# -*- coding: utf-8 -*-

import re
import string
from stringcase import sentencecase
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
    'vrrp': 'virtual router redundancy protocol'
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
        if snake_case != None:
            w = sentencecase(w)
        kebab_case = re.search("-", w)
        if kebab_case != None:
            w = sentencecase(w)
        camelOrPascalCase = re.search(r"[a-z][A-Z]", w)
        if camelOrPascalCase != None:
            text = re.sub(r'([a-z])([A-Z])', r'\1 \2', str(text))
            text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', str(text))
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
    return ' '.join([acronyms_db.get(i, i) for i in str(text).split()])


def parse_text_to_store(text):
    """
    Cleans the text without removing any of its content for storing.

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
    text = text.lower()
    text = acronym(text)
    return text


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


def unit_formatter(text):
    """
    Transforms the units names to its abbreviations.

    Parameters
    ----------
    text : string
        The text that we want to parse.

    Returns
    -------
    string
        Returns the text parsed.
    """
    # TODO: add more units
    text = str(text)
    # time
    text = re.sub("yoctosecond(s)?", "ys", text)
    text = re.sub("zeptosecond(s)?", "zs", text)
    text = re.sub("attosecond(s)?", "as", text)
    text = re.sub("femtosecond(s)?", "fs", text)
    text = re.sub("picosecond(s)?", "ps", text)
    text = re.sub("nanosecond(s)?", "ns", text)
    text = re.sub("microsecond(s)?", "µs", text)
    text = re.sub("millisecond(s)?", "ms", text)
    text = re.sub("second(s)?", "s", text)
    text = re.sub("minute(s)?", "min", text)
    text = re.sub("hour(s)?", "h", text)
    # measurement
    text = re.sub("yoctometer(s)?", "ym", text)
    text = re.sub("zeptometer(s)?", "zm", text)
    text = re.sub("attometer(s)?", "am", text)
    text = re.sub("femtometer(s)?", "fm", text)
    text = re.sub("picometer(s)?", "pm", text)
    text = re.sub("nanometer(s)?", "nm", text)
    text = re.sub("micrometer(s)?", "µm", text)
    text = re.sub("millimeter(s)?", "mm", text)
    text = re.sub("centimeter(s)?", "cm", text)
    text = re.sub("decimeter(s)?", "dm", text)
    text = re.sub("decameter(s)?", "dam", text)
    text = re.sub("hectometer(s)?", "hm", text)
    text = re.sub("kilometer(s)?", "km", text)
    text = re.sub("megameter(s)?", "Mm", text)
    text = re.sub("gigameter(s)?", "Gm", text)
    text = re.sub("terameter(s)?", "Tm", text)
    text = re.sub("petameter(s)?", "Pm", text)
    text = re.sub("exameter(s)?", "Em", text)
    text = re.sub("zettameter(s)?", "Zm", text)
    text = re.sub("yottameter(s)?", "Ym", text)
    text = re.sub(" th$", "thou", text)
    text = re.sub(" in$", "inch", text)
    text = re.sub(" ft$", "foot", text)
    text = re.sub(" yd$", "yard", text)
    text = re.sub(" ch$", "chain", text)
    text = re.sub(" fur$", "furlong", text)
    text = re.sub(" ml$", "mile", text)
    text = re.sub(" lea$", "league", text)
    text = re.sub("meter(s)?", "m", text)
    # mass
    text = re.sub("yoctogram(s)?", "yg", text)
    text = re.sub("zeptogram(s)?", "zg", text)
    text = re.sub("attogram(s)?", "ag", text)
    text = re.sub("femtogram(s)?", "fg", text)
    text = re.sub("picogram(s)?", "pg", text)
    text = re.sub("nanogram(s)?", "ng", text)
    text = re.sub("microgram(s)?", "µg", text)
    text = re.sub("milligram(s)?", "mg", text)
    text = re.sub("centigram(s)?", "cg", text)
    text = re.sub("decigram(s)?", "dg", text)
    text = re.sub("decagram(s)?", "dag", text)
    text = re.sub("hectogram(s)?", "hg", text)
    text = re.sub("kilogram(s)?", "kg", text)
    text = re.sub("megagram(s)?", "Mg", text)
    text = re.sub("gigagram(s)?", "Gg", text)
    text = re.sub("teragram(s)?", "Tg", text)
    text = re.sub("petagram(s)?", "Pg", text)
    text = re.sub("exagram(s)?", "Eg", text)
    text = re.sub("zettagram(s)?", "Zg", text)
    text = re.sub("yottagram(s)?", "Yg", text)
    text = re.sub("gram(s)?", "g", text)
    # speed
    text = re.sub("yoctohertz(s)?", "yHz", text)
    text = re.sub("zeptohertz(s)?", "zHz", text)
    text = re.sub("attohertz(s)?", "aHz", text)
    text = re.sub("femtohertz(s)?", "fHz", text)
    text = re.sub("picohertz(s)?", "pHz", text)
    text = re.sub("nanohertz(s)?", "nHz", text)
    text = re.sub("microhertz(s)?", "µHz", text)
    text = re.sub("millihertz(s)?", "mHz", text)
    text = re.sub("centihertz(s)?", "cHz", text)
    text = re.sub("decihertz(s)?", "dHz", text)
    text = re.sub("decahertz(s)?", "daHz", text)
    text = re.sub("hectohertz(s)?", "hHz", text)
    text = re.sub("kilohertz(s)?", "kHz", text)
    text = re.sub("megahertz(s)?", "MHz", text)
    text = re.sub("gigahertz(s)?", "GHz", text)
    text = re.sub("terahertz(s)?", "THz", text)
    text = re.sub("petahertz(s)?", "PHz", text)
    text = re.sub("exahertz(s)?", "EHz", text)
    text = re.sub("zettahertz(s)?", "ZHz", text)
    text = re.sub("yottahertz(s)?", "YHz", text)
    text = re.sub("hertz(s)?", "Hz", text)
    # thermodynamic temperature
    text = re.sub("kelvin(s)?", "K", text)
    text = re.sub("celsius(s)?", "°C", text)
    text = re.sub("fahrenheit(s)?", "°F", text)
    # other
    text = re.sub("milliampere(s)?", "mA", text)
    text = re.sub("centiampere(s)?", "cA", text)
    text = re.sub("deciampere(s)?", "dA", text)
    text = re.sub("decampere(s)?", "daA", text)
    text = re.sub("hectoampere(s)?", "hA", text)
    text = re.sub("kiloampere(s)?", "kA", text)
    text = re.sub("megampere(s)?", "MA", text)
    text = re.sub("gigampere(s)?", "GA", text)
    text = re.sub("ampere(s)?", "A", text)

    text = re.sub(" us$", " µs", text)

    return text


def conversion(text):
    """
    Converts unit values.

    Parameters
    ----------
    text : string
        The text that we want to convert.

    Returns
    -------
    string
        Returns the text converted.
    """
    # TODO: convert more units
    text = re.sub(r"([0-9]+\.?|,?[0-9]+?)([a-zA-Z]+)[^:]",
                  r"\1 \2", text, re.DOTALL)
    text = unit_formatter(text)

    measurement = re.search(r"[0-9]+(.|,[0-9]+)? ym|[0-9]+(.|,[0-9]+)? zm|[0-9]+(.|,[0-9]+)? am|[0-9]+(.|,[0-9]+)? fm|[0-9]+(.|,[0-9]+)? pm|[0-9]+(.|,[0-9]+)? nm|[0-9]+(.|,[0-9]+)? µm|[0-9]+(.|,[0-9]+)? mm|[0-9]+(.|,[0-9]+)? cm|[0-9]+(.|,[0-9]+)? dm|[0-9]+(.|,[0-9]+)? m|[0-9]+(.|,[0-9]+)? dam|[0-9]+(.|,[0-9]+)? hm|[0-9]+(.|,[0-9]+)? km|[0-9]+(.|,[0-9]+)? Mm|[0-9]+(.|,[0-9]+)? µm|[0-9]+(.|,[0-9]+)? Gm|[0-9]+(.|,[0-9]+)? Tm|[0-9]+(.|,[0-9]+)? Pm|[0-9]+(.|,[0-9]+)? Em|[0-9]+(.|,[0-9]+)? Zm|[0-9]+(.|,[0-9]+)? Ym|[0-9]+(.|,[0-9]+)? thou|[0-9]+(.|,[0-9]+)? inch|[0-9]+(.|,[0-9]+)? foot|[0-9]+(.|,[0-9]+)? yard|[0-9]+(.|,[0-9]+)? chain|[0-9]+(.|,[0-9]+)? furlong|[0-9]+(.|,[0-9]+)? mile|[0-9]+(.|,[0-9]+)? league", text)

    temperature = re.search(
        r"[0-9]+(.|,[0-9]+)? K|[0-9]+(.|,[0-9]+)? °C|[0-9]+(.|,[0-9]+)? °F", text)

    time = re.search(r"[0-9]+(\.|,[0-9]+)?( )?(min|s|h|ms|µs|ns|ps)", text)

    speed = re.search(
        r"[0-9]+(\.|,[0-9]+)?( )?(yHz|zHz|aHz|fHz|pHz|nHz|µHz|mHz|cHz|dHz|Hz|daHz|hHz|kHz|MHz|GHz|THz|PHz|EHz|ZHz|YHz)", text)

    if measurement != None:
        return str(converts(measurement[0], 'm')) + ' m'

    elif temperature != None:
        return str(converts(temperature[0], 'K')) + ' K'

    elif time != None:
        return str(converts(time[0], 's')) + ' s'

    elif speed != None:
        return str(speed(time[0], 'Hz')) + ' Hz'

    return text
