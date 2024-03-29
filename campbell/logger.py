from datetime import datetime
import requests 

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

      
    def __init__(self,url,user="anonymous",password="", timeout=10):
        self.url = url
        self.auth=(user, password)
        self.timeout = timeout
            
    def getClock(self):
        """
        Get Logger clock information
        @returns current logger time as date without timezone
        """
        r = requests.get(self.url,"?command=ClockCheck&format=json",auth=self.auth,timeout=self.timeout)
        return datetime.strptime(str(r.json()['time']),self.iso_timestamp)

    def getSymbols(self):
        """
        Get all symbol details from logger
        @returns list of symbols 
        """
        r = requests.get(self.url,"?command=BrowseSymbols&format=json",auth=self.auth,timeout=self.timeout)
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
        @param records: number of records  
        @param format: response format html|json|toa5|tob1|xml
        """
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"most-recent",records),auth=self.auth,timeout=self.timeout)
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
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format, uri,"since-time",since),auth=self.auth,timeout=self.timeout)
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
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"since-record",record),auth=self.auth,timeout=self.timeout)
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
        r = requests.get(self.url,"?command=dataquery&format={}&uri={}&mode={}&p1={}".format(format,uri,"Backfill",seconds),auth=self.auth,timeout=self.timeout)
        if format == 'json':
            return r.json()
        else:   
            return r.text
            


            

            


