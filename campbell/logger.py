
import logging
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import requests 
import enum


class CrLogger():
    """
    Class to access a campbell scientific logger over http
    Oliver Archner 
    2020-09-08
    """

    iso_timestamp = '%Y-%m-%dT%H:%M:%S.%f'
    iso_date = '%Y-%m-%d'

    symbol_table = 6
    symbol_array = 7
    symbol_scalar = 8

    url = None
    auth = None
    
    def __init__(self,url,user="anonymous",password=""):
        self.url = url
        self.auth=(user, password)
            
    def getClock(self):
        """Returns the current logger time as date without timezoen"""
        r = requests.get(self.url,"?command=ClockCheck&format=json",auth=self.auth)
        return datetime.strptime(str(r.json()['time']),self.iso_timestamp)

    def getSymbols(self):
        """Get all symbol details from logger"""
        r = requests.get(self.url,"?command=BrowseSymbols&format=json",auth=self.auth)
        return r.json()

    def getTableUris(self):
        return [item['uri'] for item in self.getSymbols()['symbols'] if item['type'] == self.symbol_table]  

    def dataMostRecent(self,uri,records):
        """Returns the data from the most recent number of records. The number of records is specified by records."""
        r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}".format(uri,"most-recent",records),auth=self.auth)
        return r.json()

    def dataSinceTime(self,uri,date):
        """Returns all the data since a certain time. The time is specified by date."""
        since = datetime.strftime(date,self.iso_timestamp) 
        r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}".format(uri,"since-time",since),auth=self.auth)
        return r.json()
       
    def dataSinceRecord(self,uri,record):
        """Returns all the records since a certain record number (inclusive). The record number is specified using record"""
        r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}".format(uri,"since-record",record),auth=self.auth)
        return r.json()

    def dataRange(self, uri, startTime, endTime):
        range = (datetime.strftime(startTime,self.iso_timestamp),datetime.strftime(endTime,self.iso_timestamp)) 
        """Returns the data in a certain date range. The date range is specified using startTime and endTime"""
        r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}&p2={}".format(uri,"data-range",range[0],range[1]),auth=self.auth)
        return r.json()

    def dataBackfill(self,uri, seconds):
        """Returns the all data since a specific time interval defined in seconds, e.g. 3600 would be 1 hour"""
        r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}".format(uri,"Backfill",seconds),auth=self.auth)
        return r.json()