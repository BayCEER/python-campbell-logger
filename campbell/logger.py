
import logging
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import requests 
import pandas as pd
from io import StringIO

class Logger():
    """
    Campbell scientific logger access over http
    Oliver Archner 
    2020-09-08
    """

    iso_timestamp = '%Y-%m-%dT%H:%M:%S.%f'
    toa5_timestamp = '%Y-%m-%d %H:%M:%S'
    symbol_table = 6
    symbol_array = 7
    symbol_scalar = 8

      
    def __init__(self,url,user="anonymous",password=""):
        self.url = url
        self.auth=(user, password)
            
    def getClock(self):
        """
        Get Logger clock information
        @returns current logger time as date without timezone
        """
        r = requests.get(self.url,"?command=ClockCheck&format=json",auth=self.auth)
        return datetime.strptime(str(r.json()['time']),self.iso_timestamp)

    def getSymbols(self):
        """
        Get all symbol details from logger
        @returns list of symbols 
        """
        r = requests.get(self.url,"?command=BrowseSymbols&format=json",auth=self.auth)
        return r.json()['symbols']

    def getTableUris(self):
        """
        Get table uris 
        @returns uri list  
        """
        return [item['uri'] for item in self.getSymbols() if item['type'] == self.symbol_table]  

    def dataMostRecent(self,uri,records,format='json'):
        """Returns the data from the most recent number of records. 
        @param uri: table uri including prefix
        @param resords: number of records  
        @param format: response format html|json|toa5|tob1|xml
        """
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"most-recent",records),auth=self.auth)
        if format == 'json':
            return r.json()
        else:
            return r.text

    def dataSinceTime(self,uri,date,format='json'):
        """
        Returns all the data since a certain time.
        @param uri: table uri including prefix
        @param date: start date as date without tz 
        @param format: response format html|json|toa5|tob1|xml
        """
        since = datetime.strftime(date,self.iso_timestamp) 
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format, uri,"since-time",since),auth=self.auth)
        if format == 'json':
            return r.json()
        else:
            return r.text

       
    def dataSinceRecord(self,uri,record,format='json'):
        """
        Returns data since a certain record number (inclusive).
        @param uri: table uri including prefix
        @param record: record number 
        @param format: response format html|json|toa5|tob1|xml
        """
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"since-record",record),auth=self.auth)
        if format == 'json':
            return r.json()
        else:
            return r.text

    # TODO: Not working as expected 
    # def dataRange(self, uri, startTime, endTime):
    #     range = (datetime.strftime(startTime,self.iso_timestamp),datetime.strftime(endTime,self.iso_timestamp)) 
    #     """Returns the data in a certain date range. The date range is specified using startTime and endTime"""
    #     r = requests.get(self.url,"?command=dataquery&format=json&uri={}&mode={}&p1={}&p2={}".format(uri,"data-range",range[0],range[1]),auth=self.auth)
    #     return r.json()

    def dataBackfill(self,uri,seconds, format='json'):
        """
        Returns data that has been stored since a certain time interval
        @param uri: table uri including prefix
        @param seconds: interval in number of seconds 
        @param format: response format html|json|toa5|tob1|xml
        """
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"Backfill",seconds),auth=self.auth)
        if format == 'json':
            return r.json()
        else:   
            return r.text
            

class FrameLogger(Logger):
    """
        DatFrame Extension to campell.Logger 
        All frame read methods return pandas DataFrame objects 
    """
    def __init__(self,url,user="anonymous",password="",timeZone="UTC"):
        super().__init__(url,user,password)
        self.tz = timezone(timeZone)
        self.parser = lambda t: self.tz.localize(datetime.strptime(t,"%Y-%m-%d %H:%M:%S"))
    
    def frameMostRecent(self,uri,records):
        return self.__frame(self.dataMostRecent(uri,records,format='toa5'))

    def frameSinceTime(self,uri,date):
        return self.__frame(self.dataSinceTime(uri, date,format='toa5'))
        
    def frameSinceRecord(self,uri,record):
        return self.__frame(self.dataSinceRecord(uri,record,format='toa5'))
    
    def frameBackfill(self,uri,seconds): 
        return  self.__frame(self.dataBackfill(uri,seconds,format='toa5'))

    def __frame(self,data):
        return pd.read_csv(StringIO(data),header=[1,2,3],sep=',',na_values='NAN',parse_dates=True,index_col=0, date_parser=self.parser)
          
            

            


