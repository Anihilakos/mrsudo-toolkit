import os
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python script.py [target system]")
    sys.exit()

target = sys.argv[1]

# Global dictionary to store the results
results = {}

# Command to gather the ports of the system
os.system(f"nmap {target} -p- -oG -  | awk '/Up$/{print $2}' > ports.txt")

# Read the open ports from the file and store them in the global dictionary
results['ports'] = {}
ports = {"state:":"","service":""}

with open("ports.txt") as f:
    for line in f:
        port, state = re.search(r'(\d+)/(\w+)', line.strip()).groups()
        results['ports'][port][state]= state

# Command to gather information on the services running on these ports
os.system(f"nmap -sV -sC -p {','.join(results['ports'].keys())} {target} -oA services")

# Read the services from the file and store them in the global dictionary
with open("services.nmap") as f:
    port = None
    for line in f:
        if 'PORT' in line:
            port = re.search(r'(\d+)/', line.strip()).group(1)
        elif 'http' in line:
            results['ports'][port][service] = 'http'

# Check if any of the services are HTTP-based
http_services = [port for port, service in results['services'].items() if service == 'http']

if http_services:
    # Run gobuster directory browsing on HTTP-based services
    for service in http_services:
        os.system(f"gobuster dir -u http://{target}:{service} -w /usr/share/wordlists/dirb/medium.txt -o gobuster_{target}_{service}.txt")
else:
    print("No HTTP-based services found.")
