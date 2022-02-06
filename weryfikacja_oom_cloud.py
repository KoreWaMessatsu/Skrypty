#!/usr/bin/python3

from __future__ import print_function
import re
import os
import subprocess
from time import sleep

# TODO 
# 2. TOP 10 procesów - uniklanych 

def spec_info():
    check_system_info = "hostnamectl | grep -iE 'hostname|Operating System|Kernel'"
    print("="*40, "System Info", "="*40)
    os.system(check_system_info)

    total_memory, used_memory, free_memory = map(int, os.popen('free -t --mega').readlines()[-1].split()[1:])
    print("="*40, "RAM Info", "="*40)
    print("Total memory: %d" % total_memory,"\n""Used: %u" % used_memory,"\n""Free: %g" % free_memory)

    cpu_usage=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
    cpu_count = os.cpu_count()
    cpu_load = ("uptime | awk '{print $9, $10, $11, $12, $13 }'")
    print("="*40, "CPU Info", "="*40)
    print("CPU Usage: " + cpu_usage + "%")
    print("Number of cores: %d" % cpu_count)
    os.system(cpu_load)

def check_syslog_for_oom():
    print("="*40, "Checking syslog", "="*40)
    try:
        check_log_for_oom = "cat /var/log/syslog | grep -i 'oom'  | grep -wv -i cron | grep -wv -i chef"
        if os.system(check_log_for_oom) != 0:
            raise Exception("Something went wrong")
    except:
        print("No 'oom' error message found in syslog")

def netstat():
    msg = "Listening services"
    print("="*40, msg, "="*40)
    try:
        use_netstat_comand = "netstat -tlpn | awk '{print $7}'"
        os.system(use_netstat_comand)
    except:
        print("Something went wrong!")

def list_of_domains_on_server():
    print("="*40, "List of Domains", "="*40)
    try:
        domains = os.listdir("/etc/virtual/domains/")
        print(domains)
    except:
        print("There is no domains to list on this server")

def check_cron_for_all_users():
    print("="*40, "Checking crons for all users", "="*35)
    try:
        check_each_user_crontab = "grep -Rinw /var/spool/cron/crontabs/ -e 'memory_limit'"
        os.system(check_each_user_crontab)
    except:
        print("There is no crons set with memory_limit")

def chech_sql_configuration_file():
    print("="*40, "Verfing SQL configuration file", "="*35)

    path_to_my_conf_file = "/etc/my.cnf"
    is_file_existing = os.path.isfile(path_to_my_conf_file)
    if is_file_existing == True:
        key_buffer_string = 'key_buffer_size'
        buffer_pool_string = 'innodb_buffer_pool_size'

        open_sql_conf_file = open("/etc/my.cnf", "r")
        flag_string_1 = 0
        flag_string_2 = 0
        index_string_1 = 0
        index_string_2 = 0

        for line in open_sql_conf_file:  
            index_string_1 += 1
            index_string_2 += 1 
    
            if key_buffer_string in line:
                flag_string_1 = 1
            elif buffer_pool_string in line:
                flag_string_2 = 1

        if flag_string_1 == 0: 
            print(key_buffer_string , '> not set') 
        else: 
            print('Found: ', key_buffer_string)
        if flag_string_2 == 0:
            print(buffer_pool_string , '> not set')
        else:
            print('Found: ', buffer_pool_string)    
        open_sql_conf_file.close() 
    else:
        print("SQL is not installed")    

def verify_elasticsearch_conf_file():
    print("="*40, "Memory settings for elasticsearch", "="*35)
    path_to_jvm_options = "/etc/elasticsearch/jvm.options"
    is_file_existing = os.path.isfile(path_to_jvm_options)
    if is_file_existing == True:
        string_to_match_heapsize_min = 'service.heapsize.min'
        string_to_match_heapsize_max = 'service.heapsize.max'

        open_jvm_options_file = open("/etc/elasticsearch/jvm.options", "r")
        count_lines_for_heapsize_min = 0
        count_lines_for_heapsize_max = 0
        heapsize_min_string_match = 0    
        heapsize_max_string_match = 0

        for line in open_jvm_options_file:
            heapsize_min_string_match += 1
            heapsize_max_string_match += 1

            if string_to_match_heapsize_min in line:
                count_lines_for_heapsize_min = 1
            elif string_to_match_heapsize_max in line:
                count_lines_for_heapsize_max = 1

        if count_lines_for_heapsize_min == 0:
            print(string_to_match_heapsize_min , '> not set') 
        else: 
            print('Found: ', string_to_match_heapsize_min)
        if count_lines_for_heapsize_max == 0: 
            print(string_to_match_heapsize_max , '> not set') 
        else: 
            print('Found: ', string_to_match_heapsize_max)
        open_jvm_options_file.close()
    else:
        print("Elasticsearch is not installed")

def verify_reddis_memory_settings():
    print("="*40, "Memory settings for Reddis", "="*35)
    try:
        use_redis_comand = 'redis-cli info memory | grep "maxmemory_human"'
        if os.system(use_redis_comand) != 0:
            print("Reddis is not installed")
    except:
        print("No memory set for Reddis")


def check_acces_log():
    print("="*40, "Access Log", "="*40)
    try:
        subprocess.run(["cat /var/log/php-fpm/access.log | awk '{print $1}' | sort -n | uniq -c | sort -rn | head -5"], check = True)
    except:
        print("There is no access log on this server")

def install_atop_if_not_existing():
    print("="*40, "Checking for ATOP", "="*40)
    path_to_atop = '/var/log/atop/'
    
    isPath = os.path.exists(path_to_atop) 
    if isPath == True:
        print("Atop is already installed")
    else:
        print("Installing ATOP")
        os.system("apt install atop")
        sleep(30)
        if isPath == True:
            print("Done")
        else:
            print("I was unable to install ATOP")

spec_info()
check_syslog_for_oom()
netstat()
list_of_domains_on_server()
check_cron_for_all_users()
chech_sql_configuration_file()
verify_elasticsearch_conf_file()
verify_reddis_memory_settings()
check_acces_log()
install_atop_if_not_existing()