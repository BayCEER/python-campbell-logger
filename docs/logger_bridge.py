# Sample to read a campbell logger table 
# and push the data to a BayEOS Gateway
# Oliver Archner
# 2020-09-09

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
import tempfile
from os import path
from campbell.logger import CrLogger
from pytz import timezone
import pytz 
from datetime import datetime

# Please adapt the following variables
GATEWAY_URL = 'http://debian/gateway/frame/saveFlat'
LOGGER_URL = "http://cr3000"
LOGGER_TABLE = "avg_control_1min"
LOGGER_TIMEZONE = 'Etc/GMT-1'
LOGGER_NAME = "CR3000"
BACKFILL_SECS = 3600*24
SLEEP_SECS = 5

# Gateway Client
path = path.join(tempfile.gettempdir(),"{}-data".format(LOGGER_NAME)) 
writer = BayEOSWriter(path)
writer.save_msg('Writer started.')
sender = BayEOSSender(path, LOGGER_NAME, GATEWAY_URL)
sender.start()

# Cambell logger 
logger = CrLogger(LOGGER_URL)
lastRec = None
timeZone = timezone(LOGGER_TIMEZONE)

while True:
    if lastRec is None:
        print("Initial import")
        data = logger.dataBackfill("dl:{}".format(LOGGER_TABLE),BACKFILL_SECS)
    else:
        print("Delta import")
        data = logger.dataSinceRecord("dl:{}".format(LOGGER_TABLE),lastRec)
    labels = [field['name'] for field in data['head']['fields'] if field['type'] == 'xsd:float']
    n = 0
    for rec in data['data']: 
        values = {}
        for i, label in enumerate(labels):
            values[label] = rec['vals'][i]
        dt = timeZone.localize(datetime.strptime(rec['time'],'%Y-%m-%dT%H:%M:%S'))
        ts=(dt - datetime(1970,1,1,tzinfo=pytz.utc)).total_seconds()
        writer.save(values=values,value_type=0x61,timestamp=ts) 
        lastRec= rec['no']
        n = n + 1
    print("{} records fetched. Last record:{}".format(n, lastRec))
    writer.flush()
    print("Going to sleep")
    sleep(SLEEP_SECS)
    