import time
import urllib.parse
import urllib.request
import json
import os
import sys

sys.argv[1] = sys.argv[1].replace('\'','"')
param = json.loads(sys.argv[1])

configPath = os.path.dirname(__file__)


url = 'https://eliezerodjao.com/Dosie/notifications.php'
values = param
data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
    the_page = response.read()
the_page = str(the_page)
the_page = the_page[2:-1]
try:
    the_page = json.loads(the_page)
    notification = True
except:
    notification = False
if notification:
    with open(configPath+'/access/notifications.txt','r') as nt:
        nt = json.loads(nt.read())
    nt.append(the_page)
    with open(configPath+'/access/notifications.txt','w+') as nt2:
        nt2.write(json.dumps(nt))
else:
    pass

