# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 22:06:45 2015

@author: bhayek
"""

from datetime import datetime, timedelta
import tskript
import unittest
import workclock
import timecard

class TestWorkclock(unittest.TestCase):
   
    def setUp(self):
        self.tscontext = tskript.tscontext('unittest.ini')
        self.parser = self.tscontext.parser
        self.clock = workclock.ClockPunch(self.parser)
        
    def setLocTime(self, lasLoc, lasTim, curLoc, curTim):
        self.tscontext._debugset(lasLoc, lasTim, curLoc, curTim)

    def test_contextChangeW2H(self):
        curTim = datetime.strptime("2015-02-19 08:00:05", "%Y-%m-%d %H:%M:%S")
        self.clock.resetTracking(timecard.getWeekEnding(curTim, 6))
        del2Hours = timedelta(hours=-2)
        self.setLocTime("Home", curTim + del2Hours + del2Hours, "OfficeBOS", curTim + del2Hours)
        self.clock.handleContext(self.tscontext)
        self.setLocTime("OfficeBOS", curTim + del2Hours, "OfficeBOS", curTim)
        self.clock.handleContext(self.tscontext)
        self.tscontext.curLoc = "Home"
        self.clock.handleContext(self.tscontext)
        self.assertEquals(self.parser.get("Tracking.Work", "Thu"), "2.0")

    def test_contextChangeW2V2H(self):
        curTim = datetime.strptime("2015-02-19 08:00:05", "%Y-%m-%d %H:%M:%S")
        self.clock.resetTracking(timecard.getWeekEnding(curTim, 6))
        del2Hours = timedelta(hours=-2)
        self.setLocTime("Home", curTim + (3 * del2Hours), "OfficeBOS", curTim + (2 * del2Hours))
        self.clock.handleContext(self.tscontext)
        self.setLocTime("OfficeBOS", curTim + (2 * del2Hours), "VPNBOS", curTim + del2Hours)
        self.clock.handleContext(self.tscontext)
        self.setLocTime("VPNBOS", curTim + del2Hours, "VPNBOS", curTim)
        self.clock.handleContext(self.tscontext)
        self.tscontext.curLoc = "Home"
        self.clock.handleContext(self.tscontext)
        self.assertEquals(self.parser.get("Tracking.Work", "Thu"), "4.0")

    def test_contextChangeW2Hm(self):
        curTim = datetime.strptime("2015-02-19 08:00:05", "%Y-%m-%d %H:%M:%S")
        self.clock.resetTracking(timecard.getWeekEnding(curTim, 6))
        del2Hours = timedelta(hours=-2)
        self.clock.startClock("Work", curTim + del2Hours)
        self.clock.pingClock("Work", curTim)
        self.clock.stopClock("Work")
        self.assertEquals(self.parser.get("Tracking.Work", "Thu"), "2.0")

    def test_contextChangeW2Vm(self):
        curTim = datetime.strptime("2015-02-19 08:00:05", "%Y-%m-%d %H:%M:%S")
        self.clock.resetTracking(timecard.getWeekEnding(curTim, 6))
        del2Hours = timedelta(hours=-2)
        self.clock.startClock("Work", curTim + del2Hours + del2Hours)
        self.clock.pingClock("Work", curTim + del2Hours)
        self.clock.stopClock("Work")
        self.clock.startClock("Work", curTim + del2Hours)
        self.clock.pingClock("Work", curTim)
        self.clock.stopClock("Work")
        self.assertEquals(self.parser.get("Tracking.Work", "Thu"), "4.0")

    def test_OneHour_Exact(self):
        strStart = "2015-02-25 20:29:48"
        strStop = "2015-02-25 21:29:48"
        numHours = 1
        stopWorkTime = datetime.strptime(strStop, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(strStart, "%Y-%m-%d %H:%M:%S")
        self.assertEquals(self.clock.calcHours(startWorkTime, stopWorkTime), numHours)

    def test_TwoHour_JustUnder(self):
        strStart = "2015-02-25 20:29:48"
        strStop = "2015-02-25 22:29:54"
        numHours = 2
        stopWorkTime = datetime.strptime(strStop, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(strStart, "%Y-%m-%d %H:%M:%S")
        self.assertEquals(self.clock.calcHours(startWorkTime, stopWorkTime), numHours)

    def test_TwoHour_WayUnder(self):
        strStart = "2015-02-25 20:00:00"
        strStop = "2015-02-25 21:45:30"
        numHours = 2
        stopWorkTime = datetime.strptime(strStop, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(strStart, "%Y-%m-%d %H:%M:%S")
        self.assertEquals(self.clock.calcHours(startWorkTime, stopWorkTime), numHours)

    def test_HalfHour_JustOver(self):
        strStart = "2015-02-25 20:00:00"
        strStop = "2015-02-25 20:35:30"
        numHours = 0.5
        stopWorkTime = datetime.strptime(strStop, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(strStart, "%Y-%m-%d %H:%M:%S")
        self.assertEquals(self.clock.calcHours(startWorkTime, stopWorkTime), numHours)
        
    def test_HalfHour_RoundsUp(self):
        strStart = "2015-03-02 08:24:48"
        strStop = "2015-03-02 19:43:16"
        numHours = 11.0
        stopWorkTime = datetime.strptime(strStop, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(strStart, "%Y-%m-%d %H:%M:%S")
        self.assertEquals(self.clock.calcHours(startWorkTime, stopWorkTime), numHours)

suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkclock)
unittest.TextTestRunner(verbosity=2).run(suite)