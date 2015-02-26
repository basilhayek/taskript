# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:35:21 2015

@author: bhayek
"""

from datetime import datetime, timedelta
import timecard
import workclock

class ContextHandler(object):
    def handleContext(self, context):
        """
        @type context: tscontext
        @param context: a tscontext object
        """
        raise NotImplementedError
        
class ClockPunch(ContextHandler):
    def __init__(self, parser):
        self.parser = parser

    def isTrackedLocation(self, category):
        return self.parser.getboolean('Timecard', 'track.' + category)

    def handleContext(self, context):
        lasCat = context.getCategory(context.lasLoc)
        curCat = context.getCategory(context.curLoc)
        if context.isLocationContextChange():
            if self.isTrackedLocation(lasCat):
                context.log('stopClock(' + context.lasLoc + ":" + lasCat + ')')
                self.stopClock(lasCat)
            if self.isTrackedLocation(curCat):
                context.log('startClock(' + context.curLoc + ":" + curCat + ')' + context.curTim.strftime("%Y-%m-%d %H:%M:%S"))
                self.startClock(curCat, context.curTim)
        elif self.isTrackedLocation(curCat):
            if context.isDateContextChange():
                # handle date rollover                
                context.log('lapClock(' + context.lasLoc + ":" + lasCat + ')')
                self.lapClock(curCat, context.curTim)
            else:
                context.log('pingClock(' + context.curLoc + ":" + curCat + ')' + context.curTim.strftime("%Y-%m-%d %H:%M:%S"))
                self.pingClock(curCat, context.curTim)
        else:
            print "nada----"

        # Handle submitting the timecard
        if context.isWeekContextChange():
            timecard.submitTimecard(context.curLoc, self.parser)            
            nextSubmit = datetime.strptime(self.parser.get('Tracking','week'), '%Y-%m-%d')             
            nextSubmit = nextSubmit + timedelta(days=7)
            workclock.resetTracking(nextSubmit)       

    def calcHours(self, startWorkTime, stopWorkTime):
        dtDelta = stopWorkTime - startWorkTime   
        numHours = round((2.0 * dtDelta.seconds / 60 / 60),0) / 2
        return numHours            

    def pingClock(self, location, currentTime):
        self.parser.set('Tracking.' + location, 'last', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
    
    def startClock(self, location, currentTime):
        self.parser.set('Tracking.' + location, 'start', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
        self.parser.set('Tracking.' + location, 'last', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
        self.parser.remove_option('Tracking.' + location, 'stop')
    
    def stopClock(self, location):
        strTemp = self.parser.get('Tracking.' + location, 'last')
        self.parser.set('Tracking.' + location, 'stop', strTemp)
        stopWorkTime = datetime.strptime(strTemp, "%Y-%m-%d %H:%M:%S")
        startWorkTime = datetime.strptime(self.parser.get('Tracking.' + location, 'start'),"%Y-%m-%d %H:%M:%S")
        numHours = self.calcHours(startWorkTime, stopWorkTime)
        self.trackHours(location, startWorkTime, numHours)
    
    def lapClock(self, location, currentTime):
        self.stopClock(location)
        self.startClock(location, currentTime)

    def resetTracking(self, nextSubmit):
# TODO: P3 - Change this to use the log function
        self.parser.set('Pytask','lastAction','resetTracking()')
        self.parser.set('Tracking', 'week', nextSubmit.strftime('%Y-%m-%d'))
    
        #TODO: P3 - Fix this to be dynamic
        sites = ['Client','Work']    
        for site in sites:
            dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            for day in dow:
                self.parser.set('Tracking.' + site,day,str(0))

    # Work -> Ignore -> Work: Keep clocking running
    # Work -> Ignore -> Work-VPN: LapClock
    # Work -> (OTHER) -> Ignore -> Work-VPN: LapClock
    # Work -> (DRIVE) -> Ignore -> Client: LapClock

    def trackHours(self, location, startWorkTime, numHours):
        dow = startWorkTime.strftime("%A")[0:3]
        numHours = numHours + self.parser.getfloat('Tracking.' + location, dow)
        self.parser.set('Tracking.' + location, dow, str(numHours))
        timecard.saveTimecard(startWorkTime, self.parser)

    