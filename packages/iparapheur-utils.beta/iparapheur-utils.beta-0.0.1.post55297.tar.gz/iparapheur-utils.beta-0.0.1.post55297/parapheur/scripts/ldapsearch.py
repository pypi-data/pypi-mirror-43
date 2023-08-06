#!/usr/bin/env python
# coding=utf-8
from parapheur.parapheur import config
import os

authentication_url = ""
authentication_active = ""
synchronization_security_principal = ""
synchonization_security_credentials = ""
synchronization_groupSearchBase = ""
synchronization_personDifferentialQuery = ""
query = ""


def clean(str):
    str = str.replace('\n', '')
    str = str.replace('\r', '')
    str = str.split("=", 1)
    return str[1]


def getConf():
    print("----------- Récupération des sources")
    try:
        conf = config.get("Ldapsearch", "conf_file")
    except:
        print("Fichier de conf requis: ph-init ldapsearch")

    try:
        file = open(conf, "r")
        print("OK")
    except:
        print("ERREUR : Le fichier de conf " + conf + " n'existe pas")
        exit(0)

    for line in file:
        if line.startswith("ldap.authentication.active"):
            authentication_active = clean(line)
        if line.startswith("ldap.authentication.java.naming.provider.url"):
            authentication_url = clean(line)
        if line.startswith("ldap.synchronization.java.naming.security.principal"):
            synchronization_security_principal = clean(line)
        if line.startswith("ldap.synchronization.java.naming.security.credentials"):
            synchonization_security_credentials = clean(line)
        if line.startswith("ldap.synchronization.groupSearchBase"):
            synchronization_groupSearchBase = clean(line)
        if line.startswith("ldap.synchronization.personDifferentialQuery"):
            synchronization_personDifferentialQuery = clean(line)

    file.close()


def isSynchoEnable(authentication_active):
    print("- Synchronisation demandée ?")

    if authentication_active == "true":
        print("Synchronisation activée")
    else:
        print("ERREUR : Synchronisation désactivée")


def accessUrl(authentication_url):
    print("- URL accessible ?")
    # response = os.system("ping -c 1 " + authentication_url)
    url1 = authentication_url.split("//")
    url2 = url1[1].split(":")
    try:
        response = os.system("ping -c 1 " + url2[0] + " -p " + url2[1])
    except:
        response = os.system("ping -c 1 " + url2[0])

    if response == 0:
        print('Le serveur LDAP est accessible')
    else:
        print('ERREUR : Le serveur LDAP  n\'est pas accessible', authentication_url)


def ldapRequest(authentication_url, synchronization_security_principal, synchonization_security_credentials,
                synchronization_groupSearchBase, synchronization_personDifferentialQuery):
    print("- Requête LDAP")
    query = "ldapsearch -LLL -H " + authentication_url + " -x -D " + synchronization_security_principal + " -w '" + synchonization_security_credentials + "' -b '" + synchronization_groupSearchBase + "' '" + synchronization_personDifferentialQuery + "' | grep displayName "
    print(query)


def ldapSearchGrepDisplayname(query):
    print("- Liste des utilisateurs")
    os.system(query)


getConf()
isSynchoEnable(authentication_active)
accessUrl(authentication_url)
ldapRequest(authentication_url, synchronization_security_principal, synchonization_security_credentials,
            synchronization_groupSearchBase, synchronization_personDifferentialQuery)
ldapSearchGrepDisplayname(query)
