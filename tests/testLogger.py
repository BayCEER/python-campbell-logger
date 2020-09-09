'''
Created on 2020-09-08
@author: oliver
'''
import unittest
from campbell.logger import Logger, FrameLogger
from datetime import datetime, timedelta
import configparser


class ConfigTest(unittest.TestCase):
    def setUp(self):
        conf = configparser.ConfigParser()
        self.assertGreater(len(conf.read('tests/test.conf')),0)
        cd = conf['DEFAULT'] 
        self.URL = cd['URL']
        self.USER = cd['USER']
        self.PASSWORD = cd['PASSWORD']
        self.URI = cd['URI']

class LoggerTest(ConfigTest):

    def setUp(self):
        super().setUp(self)
        self.dev = Logger(url=self.URL,user=self.USER,password=self.PASSWORD)

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


class FrameLoggerTest(ConfigTest):
    
    def setUp(self):
        super().setUp()
        self.dev = FrameLogger(url=self.URL,user=self.USER,password=self.PASSWORD,timeZone="Etc/GMT-1")
    
    def testFrameBackFill(self):
        frame = self.dev.frameBackfill(self.URI,120)
        

if __name__ == "__main__":
    unittest.main()
