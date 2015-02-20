# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 22:31:49 2015

@author: bhayek
"""

from datetime import datetime, timedelta
import tskript
import unittest

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
        self.assertTrue(self.tscontext.isCategory("home"))

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
        self.assertTrue(True)

    def test_dateChangeDiffDate(self):
#        self.parser.set("Pytask","lastrun",lastTime.strftime("%Y-%m-%d %H:%M:%S"))
         self.assertTrue(True)

#if __name__ == '__main__':
#    unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestTskript)
unittest.TextTestRunner(verbosity=2).run(suite)