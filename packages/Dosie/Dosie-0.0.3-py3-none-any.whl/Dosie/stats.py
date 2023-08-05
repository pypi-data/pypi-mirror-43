import urllib.parse
import urllib.request
import os
import requests
import sys
import json
import logging

def my_handler(exc_type, exc_value, exc_traceback):
    ff = 'error.log'
    if 'SystemExit'.lower() in str(exc_type).lower():
        return
    logging.basicConfig(filename=ff,level=logging.DEBUG)
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    logging.warning('And this, too')
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    with open(ff,'a+') as ff:
        ff.write('\nEND-------------------------------\n-------------------------------\n\n')

sys.excepthook = my_handler

configPath = os.path.dirname(__file__)


file = sys.argv[1]
sys.argv[2] = sys.argv[2].replace('\'','"')
param = json.loads(sys.argv[2])




url = 'https://eliezerodjao.com/Dosie/stats.php'
the_page = False
if file == True or file == 'True':
    if os.path.getsize(param['file']) > 0:
        with open(param['file'], 'rb') as f:
            try:
                the_page = requests.post(url, data=param, files={param['file']: f})
            except:
                the_page = False
        if the_page:
            with open(param['file'],'w+') as df:
                df.write('')
else:
    values = param
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data)
    try:
        with urllib.request.urlopen(req) as response:
            the_page = str(response.read())
    except:
        the_page = False

