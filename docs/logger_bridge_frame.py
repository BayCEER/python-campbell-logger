# Sample to read a campbell logger table and push the data to a BayEOS Gateway
# Oliver Archner
# 2020-09-09

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
import tempfile
from os import path
from campbell.logger import FrameLogger
from pytz import timezone
import pytz 
from datetime import datetime

# Please adapt the following variables
GATEWAY_URL = 'http://debian/gateway/frame/saveFlat'
LOGGER_URL = "http://cr3000"
LOGGER_TABLE = "avg_control"
LOGGER_TIMEZONE = 'Etc/GMT-1'
LOGGER_NAME = "CR3000"
BACKFILL_SECS = 3600
SLEEP_SECS = 5


# Gateway Client
path = path.join(tempfile.gettempdir(),"{}-data".format(LOGGER_NAME)) 
writer = BayEOSWriter(path)
writer.save_msg('Writer started.')
sender = BayEOSSender(path, "{}/{}".format(LOGGER_NAME,LOGGER_TABLE), GATEWAY_URL)
sender.start()

# Cambell logger 
logger = FrameLogger(LOGGER_URL,timeZone=LOGGER_TIMEZONE)
lastRec = None
timeZone = timezone(LOGGER_TIMEZONE)

while True:
    if lastRec is None:
        print("Initial import")
        df = logger.frameBackfill("dl:{}".format(LOGGER_TABLE),BACKFILL_SECS)
    else:
        print("Delta import")
        df = logger.frameSinceRecord("dl:{}".format(LOGGER_TABLE),lastRec)
    n = 0
    for ts, row in df.iterrows():       
        values = {}
        for col, value in row.items():
            values[col[0]] = value
        writer.save(values=values,value_type=0x61,timestamp=ts.timestamp()) 
        lastRec=int(values['RECORD'])
        n = n + 1
    print("{} records fetched. Last record:{}".format(n, lastRec))
    writer.flush()
    print("Going to sleep")
    sleep(SLEEP_SECS)
    