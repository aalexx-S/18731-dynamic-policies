# A helper program to send a http request to the policy server to simulate 
# a device update.

import sys
import urllib.request

if len(sys.argv) != 4:
    print('Usage: set_status.py <device> <status name> <status value>')
    exit()

device = sys.argv[1]
sname = sys.argv[2]
svalue = sys.argv[3]

query = {
    'device': device,
    'status_name': sname,
    'status_value':svalue
}

rurl = 'http://127.0.0.1:8080/?%s' %(urllib.parse.urlencode(query))
print(rurl)
contents = urllib.request.urlopen(rurl)

print(contents)