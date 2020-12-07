#!/bin/sh
PYTHON_APPS="python3 python3-pip python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev portaudio19-dev libperl-dev gcc libsnmp-dev"
SNMP_APPS="snmp snmp-mibs-downloader snmpd"
LIST_OF_APPS="iputils-ping software-properties-common nmap wireshark"

sudo apt update
sudo apt install $SNMP_APPS
sudo apt install lldpad
lldpad -d

for i in `ls /sys/class/net/ | grep 'eth\|ens\|eno'` ; do echo "enabling lldp for interface: $i" ; lldptool set-lldp -i $i adminStatus=rxtx ; lldptool -T -i $i -V sysName enableTx=yes; lldptool -T -i $i -V portDesc enableTx=yes ; lldptool -T -i $i -V sysDesc enableTx=yes; lldptool -T -i $i -V sysCap enableTx=yes; lldptool -T -i $i -V mngAddr enableTx=yes; done

sudo apt install -y $PYTHON_APPS
sudo add-apt-repository universe
pip3 install --upgrade pip
sudo apt install -y $LIST_OF_APPS
pip3 install -r requirements.txt

python3 -m spacy download en_core_web_lg
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader wordnet