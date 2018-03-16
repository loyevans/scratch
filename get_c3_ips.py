#!/usr/bin/python

import requests
#import anydbm
#import jinja2
import json
import os
import time
import re
import sys
import logging

cliqr_ccm = 'bds-ccc.auslab.cisco.com'
cliqr_user = 'loyevans_e'
cliqr_key = ''


deployment = sys.argv[1]

#######################

def get_deployed_apps():

    r2 = 'curl -s -k -H "Accept:application/json" -H "Content-Type:application/json" -u ' + cliqr_user + ':' + cliqr_key +  ' -X GET https://' + cliqr_ccm + '/v1/jobs/'
    f = os.popen(r2)
    result = f.read()
    f.close()
    formed = json.loads(result)

    s = '{"deployed" : [\n'
    for i in formed['jobs']:
        if i['deploymentInfo'] == None:
            continue
        print (i)
        print ("=====================================")
        print (i['deploymentInfo'])
        s += '    {"Name": "' + i['deploymentInfo']['deploymentName'] + '", "App": "' + i['appName'] + '", "Status": "' + i['deploymentInfo']['deploymentStatus'] + '"},\n'
    s = s[:-2] + '\n'
    s += "]}\n"

    return s 

def get_deployed_app_ips(deployment):

    r2 = 'curl -s -k -H "Accept:application/json" -H "Content-Type:application/json" -u ' + cliqr_user + ':' + cliqr_key +  ' -X GET https://' + cliqr_ccm + '/v1/jobs/'
    f = os.popen(r2)
    result = f.read()
    f.close()
    formed = json.loads(result)

    s = '{"deployed" : [\n'
    for i in formed['jobs']:
        if i['deploymentInfo'] == None:
            continue
        if i['deploymentInfo']['deploymentName'] == deployment:
            r3 = 'curl -s -k -H "Accept:application/json" -H "Content-Type:application/json" -u ' + cliqr_user + ':' + cliqr_key +  ' -X GET ' + i['resource']
            f2 = os.popen(r3)
            result = f2.read()
            f2.close()
            formed = json.loads(result)
            #print json.dumps(formed, indent=4)
            for j in formed['jobs']:
                for v in j['virtualMachines']:
                    #print json.dumps(v, indent=4)
                    hn = v['hostName']
                    nis = ""
                    for ni in v['nodeNetworkInterfaces']:
                        nis = nis +  ',' + ni['publicIPAddress']
                    res = hn + nis
                    print (res) 


        #print i
        #print "====================================="
        #print i['deploymentInfo']
        #s += '    {"Name": "' + i['deploymentInfo']['deploymentName'] + '", "App": "' + i['appName'] + '", "Status": "' + i['deploymentInfo']['deploymentStatus'] + '"},\n'
    #s = s[:-2] + '\n'
    #s += "]}\n"

    #return s 

#######################

if __name__ == '__main__':
   get_deployed_app_ips(deployment)
