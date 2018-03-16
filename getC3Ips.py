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
cliqr_key = str('713EA2E8A097883C')


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
        s += '    {"Name": "' + i['deploymentInfo']['deploymentName'] + '", "App": "' + i['appName'] + '", "Status": "' + i['deploymentInfo']['deploymentStatus'] + '"},\n'
    s = s[:-2] + '\n'
    s += "]}\n"

    return s 

#######################

if __name__ == '__main__':
   s = get_deployed_apps()
   print (s)
