#!/usr/bin/python3

from __future__ import print_function
import os
import re
from time import sleep

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
			print("Something went wrong!")
	except:
		print("No 'oom' error message found in syslog")

def netstat():
	msg = "Listening services"
	print("="*40, msg, "="*40)
	try:
		use_netstat_comand = "netstat -tlpn | awk '{print $7}'"
		if os.system(use_netstat_comand) != 0:
			print("Something went wrong!")
	except:
		print("Netstat returned nothing!")

def list_of_domains_on_server():
	print("="*40, "List of Domains", "="*40)
	try:
		domains = ("cat /etc/virtual/domains")
		if os.system(domains) != 0:
			print("Something went wrong!")
	except:
		print("There is no domains on this server")

def check_cron_for_all_users():
	print("="*40, "Checking crons for all users", "="*35)
	try:
		check_each_user_crontab = "grep -Rinw /var/spool/cron/crontabs/ -e 'memory_limit'"
		if os.system(check_each_user_crontab) != 0:
			print("Something went wrong!")
	except:
		print("There is no crons set with memory_limit")

def chech_sql_configuration_file():
    print("="*40, "Verfing SQL configuration file", "="*35)

    path_to_my_conf_file = "/etc/my.cnf"
    alternative_path = "/etc/mysql/my.cnf"
    is_file_existing = os.path.isfile(path_to_my_conf_file)
    is_file_existing_alter = os.path.isfile(alternative_path)
    if is_file_existing == True:
        key_buffer_pattern = re.compile('key_buffer_size')
        buffer_pool_pattern = re.compile('innodb_buffer_pool_size')
        for line in open("/etc/my.cnf"):
            for match in re.finditer(key_buffer_pattern, line):
                print(line)
            for match in re.compile(buffer_pool_pattern, line):
                print(line)
    elif is_file_existing_alter == True:
        for line in open("/etc/mysql/my.cnf"):
            for match in re.finditer(key_buffer_pattern, line):
                print(line)
            for match in re.compile(buffer_pool_pattern, line):
                print(line)
    else:
        print("Configuration file not found")    

def verify_elasticsearch_conf_file():
    print("="*40, "Memory settings for elasticsearch", "="*35)

    path_to_jvm_options_file = "/etc/elasticsearch/jvm.options"
    is_file_existing = os.path.isfile(path_to_jvm_options_file)
    if is_file_existing == True:
        pattern_to_match_heapsize_min = re.compile('Xms')
        pattern_to_match_heapsize_max = re.compile('Xmx')
        for line in open("/etc/elasticsearch/jvm.options"):
            for match in re.finditer(pattern_to_match_heapsize_min, line):
                print(line)
            for match in re.finditer(pattern_to_match_heapsize_max, line):
                print(line)
    else:
        print("Configuration file not found")

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
		use_access_log_command = "cat /var/log/php-fpm/access.log | awk '{print $1}' | sort -n | uniq -c | sort -rn | head -5"
		if os.system(use_access_log_command) !=0:
			print("Something went wrong!")
	except:
		print("Access log is empty!")

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
	print("\n")

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