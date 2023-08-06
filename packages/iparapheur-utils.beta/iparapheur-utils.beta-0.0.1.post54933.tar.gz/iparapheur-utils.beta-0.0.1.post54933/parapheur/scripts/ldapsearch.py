#!/usr/bin/env python
# coding=utf-8
from parapheur.parapheur import config
import os

print("- Récupération des sources")
# import_dir = config.get("Ldapsearch", "conf_file")
conf = "/home/spatau/Téléchargements/___LDAP/PROD_ldap-ad-authentication.properties"
try:
    file = open(conf, "r")
    print("OK")
except:
    print("ERREUR : Le fichier de conf " + conf + " n'existe pas")
    exit(0)


def clean(str):
    str = str.replace('\n', '')
    str = str.replace('\r', '')
    str = str.split("=", 1)
    return str[1]


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

# print(authentication_active)
# print(authentication_url)
# print(synchronization_security_principal)
# print(synchonization_security_credentials)
# print(synchronization_groupSearchBase)
# print(synchronization_personDifferentialQuery)

file.close()

print("- Synchronisation demandée ?")

if authentication_active == "true":
    print("Synchronisation activée")
else:
    print("ERREUR : Synchronisation désactivée")

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

print("- Requête LDAP")
query = "ldapsearch -LLL -H " + authentication_url + " -x -D " + synchronization_security_principal + " -w '" + synchonization_security_credentials + "' -b '" + synchronization_groupSearchBase + "' '" + synchronization_personDifferentialQuery + "' | grep displayName "
print(query)

print("- Liste des utilisateurs")
os.system(query)
