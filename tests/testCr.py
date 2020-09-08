'''
Created on 2020-09-08
@author: oliver
'''
import unittest
from campbell.logger import CrLogger
from datetime import datetime, timedelta


class CrTest(unittest.TestCase):    

    URL = "http://132.180.116.106"
    URI = "dl:sonics_2d_10sec"
    
    def setUp(self):
        self.dev = CrLogger(self.URL)

    def testGetClock(self):        
        print(self.dev.getClock())
    
    def testGetSymbols(self):
        print(self.dev.getSymbols())
    
    def testGetTableUris(self):
        print(self.dev.getTableUris())

    def testDataMostRecent(self):
        print(self.dev.dataMostRecent(self.URI,10))

    def testDataSinceTime(self):
        # Last minute 
        lmin = self.dev.getClock() - timedelta(seconds=60)
        print(self.dev.dataSinceTime(self.URI,lmin))

    def testDataSinceRecord(self):
        d = self.dev.dataMostRecent(self.URI,1) 
        nr = d['data'][0]['no'] 
        print("Nr:{}".format(nr))      
        print(self.dev.dataSinceRecord(self.URI,nr))

    def testDataBackFill(self):
        print(self.dev.dataBackfill(self.URI,120))

if __name__ == "__main__":
    unittest.main()
