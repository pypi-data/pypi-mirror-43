#!/usr/bin/env python
# v1.2    8/1/2019 First version 
# usage ./alteon2f5 <input file name> [partition]
import sys
import re
import time

def config_to_array (cfg):
    # Take a config string and converts it into a config array
    # Example 'if 5\r\n\tena\r\n\tipver v4\r\n\taddr 10.230.253.199\r\n\tmask 255.255.255.240\r\n\tbroad 10.230.253.207\r\n\tvlan 1199\r\n', '\tvlan 1199\r\n'
    config = {}
    configArray = cfg.split("\r\n")
    for line in configArray:
        if line == '':
            continue
        vars = line.split(' ')
        if len(vars) == 1:
            # No value available
            index,value = vars[0].lstrip(),True
        elif len(vars) == 2:
            # Index and value available
            index,value = vars[0].lstrip(),vars[1].rstrip().strip('\"')
            if index in config:
                # Already an index there
                #print "Type:" + type(config[index])
                if isinstance(config[index],basestring):
                    # Convert it to be a list
                    value = [config[index],value]
                elif isinstance(config[index],list):
                    # Append the value to the list
                    config[index].append(value)
                    continue
        else:
            # Multiple values so concatenate them all together
            index = vars[0].lstrip()
            value = ' '.join(vars[1:])
        config[index] = value
    return config
    
def convertmask (mask):
    return sum([bin(int(x)).count('1') for x in mask.split('.')])    
    
def array_add(a,d):
    # Function to safely add to an array
    #global a
    if not len(a):
        a = [ d ]
    else:
        a.append( d )
    return a
    

def is_ipv6(ip):
    if ':' in ip:
        return True
    else:
        return False

# Check there is an argument given
if not len(sys.argv) > 1:
    exit("Usage: " + sys.argv[0] + " <filename> [partition]")
if len(sys.argv) == 3:
    # Second command-line variable is the partition
    partition = "/" + sys.argv[2] + "/"
    print "Using partition " + partition
else:
    partition = "/Common/"
    
# Check input file
fh = open(sys.argv[1],"r")
if not fh:
    exit("Cannot open file " + argv[1])
rawfile = fh.read()
# Remove all comments from file
file = re.sub('\/c\/dump.+?^\/c','',rawfile)


config = {}

##### Non-Floating Self-IPs ###########
config['self-ips'] = []
for line in re.finditer('\/c\/l3\/(if \d\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['self-ips'].append(cfg)
    
##### Floating Self-IPs ###########
config['self-ips-floating'] = []
for line in re.finditer('\/c\/l3\/vrrp\/(vr \d\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['self-ips-floating'].append(cfg)
    
##### Routes ###########
config['routes'] = []
for line in re.finditer('\/c\/l3\/(gw \d\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['routes'].append(cfg)   

##### SSL Certs ###########
config['ssl-certs'] = {}
for line in re.finditer('\/c\/slb\/ssl\/certs\/import (\S+) (\S+) text\r\n(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)',file,re.MULTILINE|re.DOTALL):
    type,name,text = line.group(1),line.group(2).strip('\"'),line.group(3)
    config['ssl-certs'][name] = {'type': type, 'text': text}

##### Nodes ###########
config['nodes'] = {}
for line in re.finditer('\/c\/slb\/(real \d+\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['nodes'][cfg['real']] = cfg     
    
##### Pools ###########
config['pools'] = {}
for line in re.finditer('\/c\/slb\/(group \d+\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['pools'][cfg['group']] = cfg
    
##### Monitors - HTTP ###########
config['monitors'] = {'http':{}}
for line in re.finditer('\/c\/slb\/(advhc/health (\S+) HTTP.+?\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    name = line.group(2)
    cfg = config_to_array(line.group(1))
    if name in config['monitors']['http']:
        config['monitors']['http'][name].update(cfg)
    else:
        config['monitors']['http'][name] = cfg    
 
##### Virtual Addresses ###########
config['virtual-addresses'] = {}
for line in re.finditer('\/c\/slb\/(virt \d+\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    cfg = config_to_array(line.group(1))
    config['virtual-addresses'][cfg['virt']] = cfg

##### Virtual Servers ###########
config['virtual-servers'] = {}
for line in re.finditer('\/c\/slb\/(virt (\d+)/service (\d+) (\S+)\r\n(\t.+?\r\n)+)',file,re.MULTILINE|re.DOTALL):
    virtId,port,type = line.group(2),line.group(3),line.group(4)
    cfg = config_to_array(line.group(1))
    cfg['type'] = type
    if virtId not in config['virtual-servers']:
        config['virtual-servers'][virtId] = {}
    config['virtual-servers'][virtId][port] = cfg


##########################################################################
#
# We have collected all of the relevant information. Now to print it out  
#
#
print ("# Configuration created on " + time.strftime("%c") )
print ("# Input filename: " + sys.argv[1] )
print ("# Partition: " + partition )
print ("\n\n")

# Stats
print("# -- Number of objects --")
print("# Type\t\t\tNumber")
print("# ----------------------------")
print("# SSL certs\t\t" + str(len(config['ssl-certs'])))
print("# Self-IPs\t\t" + str(len(config['self-ips'])))
print("# Floating Self-IPs\t" + str(len(config['self-ips-floating'])))
print("# Nodes\t\t\t" + str(len(config['nodes'])))
print("# Monitors - HTTP\t" + str(len(config['monitors']['http'])))
print("# Pools\t\t\t" + str(len(config['pools'])))
print("# Virtual Addresses\t" + str(len(config['virtual-addresses'])))
print("# Virtual Servers\t" + str(len(config['virtual-servers'])))


print("# ----------------------------\n\n")
##### SSL Certs ########
# Create SSL cert files
print("# -- Creating SSL certs --")
for cert in config['ssl-certs']:
        print ("# -- Writing SSL cert " + cert)
        with open(cert + ".crt",'w') as certFile:
            certFile.write(config['ssl-certs'][cert]['text'])
print("# -- Finished creating SSL certs --")
# Create load_certs.sh script to load the certs
with open("alteon_load_certs.sh",'w') as loadFile:
    loadFile.write("#!/bin/bash\n# Script to load SSL certs to F5\n")
    for cert in config['ssl-certs']:
        loadFile.write("tmsh install sys crypto cert " + partition + cert + ".crt from-local-file /var/tmp/" + cert + ".crt\n")
    print ("#!! Copy *.crt files to /var/tmp directory on BIG-IP and run load_certs.sh script !!")

    
print ("\n#-------------------------------------------------------")
print ("#----- Configuration below this line   -----------------\n")    



##### Non-Floating Self-IPs ########
for ip in config['self-ips']:
    print ("net self IP_" + ip['addr'] + " {")
    print ("\taddress " + ip['addr'] + "/" + str(convertmask(ip['mask'])))
    print ("\ttraffic-group traffic-group-local-only")
    print ("\tvlan VLAN-" + ip['vlan'])
    print ("\t}")

##### Floating Self-IPs ########
for ip in config['self-ips-floating']:
    if 'ena' not in ip:
        continue
    print ("net self IP_" + ip['addr'] + " {")
    print ("\taddress " + ip['addr'] + '/##INSERT MASK HERE##')
    print ("\ttraffic-group traffic-group-1")
    print ("\tvlan VLAN-" + '##INSERT VLAN ID HERE##')
    print ("\t}")


##### Nodes ##########
for nodeId in config['nodes']:
    n = config['nodes'][nodeId]
    print("ltm node " + partition + n['name'] + " {")
    print("\taddress " + n['rip'])
    print("}")

###### Monitors - HTTP/HTTPS ######
for monitor in config['monitors']['http']:
    m = config['monitors']['http'][monitor]
    if 'name' in m:
        monitorName = m['name']
    else:
        monitorName = monitor
    # Create this as an HTTP monitor if required    
    if 'ssl' in m and m['ssl'] == 'enabled':
        print ("ltm monitor https " + partition + monitorName + " {")
    else:
        print ("ltm monitor http " + partition + monitorName + " {")  
    if 'path' in m:
        print("\tsend " + m['path'])
    if 'response' in m:
        print("\trecv ^" + m['response'].replace('\"','').replace(' incl ','.*'))
    if 'dport' in m:
        print("\talias *:" + m['dport'])
    print ("}")
    
##### Pools ##########
for poolId in config['pools']:
    p = config['pools'][poolId]
    # Deal with the case of the pool not having a name
    if 'name' not in p:
        if 'group' in p:
            poolName = "GROUP-" + p['group']
        else:
            poolName = 'POOL_UNKNOWN'
    else:
        poolName = p['name']
            
    print("ltm pool " + partition + poolName + " {")
    if 'group' in p:
        print("\tdescription \"group " + p['group'] + "\"" )
    if 'health' in p:
        print("\tmonitor 1 of { " + partition + p['health'] + " }")
    # Manage pool members
    if 'add' in p:
        print("\tmembers {")
        for poolMember in p['add']:
            # Note that this is the nodeId, there is no port number
            # So we are going to add the node name and port 0 and leave the VS to sort it out
            print ("\t\t" + partition + config['nodes'][poolMember]['name'] + ":0")
        print("\t}")
    print("}")

##### Virtual Servers ###############
for vsId in config['virtual-servers']:
    for port in config['virtual-servers'][vsId]:
        vs = config['virtual-servers'][vsId][port]
        vsName = "VS_" + config['virtual-addresses'][vsId]['vname'].strip("\"").replace(" ","_") + "-" + port
        destination = config['virtual-addresses'][vsId]['vip'] + ":" + port
        #print "vsId: " + vsId + " port: " + str(port) + " VS: " + str(vs)

        print ("ltm virtual " + partition + vsName + " {")
        print("\tdestination " + destination)
        if 'group' in vs:
            # Specify the pool
            print("\tdescription \"group " + vs['group'] + "\"")
            if 'name' in config['pools'][vs['group']]:
                print("\tpool " + partition + config['pools'][vs['group']]['name'])
            else:
                print("\tpool " + partition + "GROUP-" + vs['group'])
        else:
            print("\t# WARNING! No pool assigned")
        # Manage profiles
        if 'type' in vs:
            print("\tprofiles {")
            if vs['type'] == 'basic-slb':
                # FastL4
                print("\t\tFastL4 {}")
            elif vs['type'] == 'http/http':
                # HTTP
                print("\t\ttcp {}\n\t\thttp {}")
            elif vs['type'] == 'https':
                # HTTP
                print("\t\ttcp {}\n\t\tclient-ssl {}")    
            elif vs['type'] == 'https/appshape':
                # HTTP with SSL and iRules
                print("\t\ttcp {}\n\t\thttp {}\n\t\tclient-ssl {}")
            elif vs['type'] == 'imap':
                # HTTP
                print("\t\ttcp {}\n\t\timap {}")
            elif vs['type'] == 'pop3':
                # HTTP
                print("\t\ttcp {}\n\t\tpop3 {}")
            else:
                print("WARNING: Unknown VS type: " + vs['type'])
                print("\t\tipother {}")
                
            print("\t}")
        print("}")
          