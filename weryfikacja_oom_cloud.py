#!/usr/bin/python

from __future__ import print_function
import re
import os

# TODO
# 1. Weryfikacja sys logów pod kątem oom
# 2. Weryfikacja cronów pod kątem memory_limit=-1
# 3. Wyłączenie po potwierdzeniu clam'a

#Wywołanie polecnia netstat
def netstat():
    print("Priting netstat:")
    netstatcommand = "netstat -tulpn"
    try:
        os.system(netstatcommand)
    except:
        print("Wywołanie komendy nie powiodło się")
        print("\n")

#Listowanie listy domen na serwerze
def listofdomain():
    print("Printing list of domains on a server:")
    try:
        domains = os.listdir("/home/wojtek/Dokumenty/Vscode/Testy/")
        print(domains)
    except:
        print("Nie udało się wyświetlić listy domen na serwerze")
    print("\n")

#Sprawdzanie ustawień bazydanych
def mariadb():
    print("Memory settings for MariaDB my.conf file:")
    myconffile = open('/home/wojtek/Dokumenty/Vscode/Testy/testbackup/my.conf', 'r').readlines()
    try:
        for line in myconffile:
            if re.search(r"key_buffer_size", line) or re.search(r"innodb_buffer_pool_size", line):
                print(line, end='')
    except:
        print('Nie znaleziono ustwień')
    print("\n")

#Sprawdzanie ustawień elasticsearch
def elasticsearch():
    print("Memory settings for Elasticsearch jvm.option file:")
    jvmoptions = open('/home/wojtek/Dokumenty/Vscode/Testy/testbackup/jvm.options', 'r').readlines()
    try:
        for line in jvmoptions:
            if re.search(r"service.heapsize.min", line) or re.search(r"service.heapsize.max", line):
                print(line, end='')
    except:
        print("Nie znaleziono ustawień")
    print("\n")

#Sprawdzenie reddisa
def reddis():
    reddiccommand = "redis-cli info memory"
    print("Prining redis memory setting:")
    try:
        os.system(reddiccommand)
    except:
        print("Brak redisa na serwerze")
    print("\n")


netstat()
listofdomain()
mariadb()
elasticsearch()
reddis()
