# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 22:31:49 2015

@author: bhayek
"""

import ConfigParser
from datetime import datetime, timedelta
import tskript
import workclock
import unittest
import timecard

class TestTskript(unittest.TestCase):
   
    def setUp(self):
        self.currentTime = datetime.now()
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read('unittest.ini')
        
    def test_isTrackedLocation(self):
        self.parser.set("Location","Track.Home","False")
        self.assertEquals(tskript.isTrackedLocation("Home", self.parser), False)

    def test_contextChangeW2H(self)        :
        self.parser.set("Pytask","lastlocation","work")
        currentLocation = "home"
        changeType = tskript.contextChange(currentLocation, self.currentTime, self.parser)
        self.assertEquals(changeType, 1 + 2)

    def test_contextChangeH2W(self)        :
        self.parser.set("Pytask","lastlocation","home")
        currentLocation = "work"
        changeType = tskript.contextChange(currentLocation, self.currentTime, self.parser)
        self.assertEquals(changeType, 1 + 4)

    def test_contextChangeC2W(self)        :
        self.parser.set("Pytask","lastlocation","client")
        currentLocation = "work"
        changeType = tskript.contextChange(currentLocation, self.currentTime, self.parser)
        self.assertEquals(changeType, 1 + 2 + 4)
        
    def test_dateChangeSameDate(self):
        self.parser.set("Pytask","lastrun",self.currentTime.strftime("%Y-%m-%d %H:%M:%S"))
        changeType = tskript.dateChange(self.currentTime, self.parser)        
        self.assertEquals(changeType, 0)

    def test_dateChangeDiffDate(self):
        lastTime = self.currentTime + timedelta(days=-1)
        self.parser.set("Pytask","lastrun",lastTime.strftime("%Y-%m-%d %H:%M:%S"))
        changeType = tskript.dateChange(self.currentTime, self.parser)        
        self.assertEquals(changeType, 1)
       
    def test_dateChangeDiffWeek(self):
        lastTime = self.currentTime + timedelta(days=-1)
        self.parser.set("Pytask","lastrun",lastTime.strftime("%Y-%m-%d %H:%M:%S"))
        lastWeek = self.currentTime + timedelta(days=-7)
        self.parser.set("Tracking","week",lastWeek.strftime("%Y-%m-%d"))
        changeType = tskript.dateChange(self.currentTime, self.parser)        
        self.assertEquals(changeType, 1 + 2)
        
    def test_workClockBasic(self):
        lastTime = self.currentTime + timedelta(hours=-2)
        location = "Work"
        workclock.startClock(location, lastTime, self.parser)
        workclock.pingClock(location, self.currentTime, self.parser)
        workclock.stopClock(location, self.parser)
        hours = self.parser.getfloat('Tracking.' + location, self.currentTime.strftime("%A")[0:3])
        self.assertEqual(hours, 2.0)
        
    def test_weekEnding(self):
        self.assertEquals(timecard.getWeekEnding(self.currentTime, 6), self.currentTime + timedelta(days=1))
        
        

#if __name__ == '__main__':
#    unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestTskript)
unittest.TextTestRunner(verbosity=2).run(suite)