# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 22:31:49 2015

@author: bhayek
"""

from datetime import datetime, timedelta
import tskript
import unittest

# from geoip import geolite2
# import win_inet_pton
# import socket

import urllib, json

class TestTskript(unittest.TestCase):
   
    def setUp(self):
        self.tscontext = tskript.tscontext('unittest.ini')
        
    def setLocTime(self, lasLoc, lasTim, curLoc, curTim):
        self.tscontext.lasLoc = lasLoc
        self.tscontext.lasTim = lasTim
        self.tscontext.curLoc = curLoc
        self.tscontext.curTim = curTim
        
    def test_isHome(self):
        curTim = datetime.now()
        del2Hours = timedelta(hours=-2)
        self.setLocTime("OfficeBOS", curTim + del2Hours, "Home", curTim)
        self.assertTrue(self.tscontext.isCategory("Home"))

    def test_contextChangeW2H(self):
        curTim = datetime.now()
        del2Hours = timedelta(hours=-2)
        self.setLocTime("OfficeBOS", curTim + del2Hours, "Home", curTim)
        self.assertTrue(self.tscontext.isLocationContextChange())

    def test_contextChangeW2V(self):
        curTim = datetime.now()
        del2Hours = timedelta(hours=-2)
        self.setLocTime("OfficeBOS", curTim + del2Hours, "VPNBOS", curTim)
        self.assertFalse(self.tscontext.isLocationContextChange())

    def test_dateChangeSameDate(self):
        houradj = int(self.tscontext.lasTim.hour / 2)
        curTim = self.tscontext.lasTim + timedelta(hours=-houradj)
        self.tscontext.curTim = curTim
        self.assertFalse(self.tscontext.isDateContextChange())

    def test_dateChangeDiffDate(self):
        curTim = self.tscontext.lasTim + timedelta(hours=36)
        self.tscontext.curTim = curTim
        self.assertTrue(self.tscontext.isDateContextChange())
        self.assertTrue(True)

    def test_weekChangeDiffWeek(self):
        curTim = self.tscontext.lasTim + timedelta(days=8)
        self.tscontext.curTim = curTim
        self.assertTrue(self.tscontext.isWeekContextChange())
		
#    def test_geolite2_locateme(self):
#        match = geolite2.lookup_mine()
#        print match

    def test_hostip_locateme(self):
        data = json.loads(urllib.urlopen("http://api.hostip.info/get_json.php").read())
        print data["ip"]
        print data["city"]



#if __name__ == '__main__':
#    unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestTskript)
unittest.TextTestRunner(verbosity=2).run(suite)