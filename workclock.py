# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:35:21 2015

@author: bhayek
"""

from datetime import datetime
import timecard

def updateTracking(nextSubmit, parser):
    parser.set('Pytask','lastAction','updateTracking()')
    parser.set('Tracking', 'week', nextSubmit.strftime('%Y-%m-%d'))

    #TODO: P3 - Fix this to be dynamic
    sites = ['Client','Work']    
    for site in sites:
        dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        for day in dow:
            parser.set('Tracking.' + site,day,str(0))

def trackHours(location, startWorkTime, numHours, parser):
    dow = startWorkTime.strftime("%A")[0:3]
    numHours = numHours + parser.getfloat('Tracking.' + location, dow)
    parser.set('Tracking.' + location, dow, str(numHours))
    timecard.saveTimecard(startWorkTime, parser)

def pingClock(location, currentTime, parser):
    parser.set('Tracking.' + location, 'last', currentTime.strftime("%Y-%m-%d %H:%M:%S"))

def startClock(location, currentTime, parser):
    parser.set('Pytask','lastAction','startClock(' + location + ')')
    parser.set('Tracking.' + location, 'start', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
    parser.set('Tracking.' + location, 'last', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
    parser.remove_option('Tracking.' + location, 'stop')

def stopClock(location, parser):
    parser.set('Pytask','lastAction','stopClock()')
    strTemp = parser.get('Tracking.' + location, 'last')
    parser.set('Tracking.' + location, 'stop', strTemp)
    stopWorkTime = datetime.strptime(strTemp, "%Y-%m-%d %H:%M:%S")
    startWorkTime = datetime.strptime(parser.get('Tracking.' + location, 'start'),"%Y-%m-%d %H:%M:%S")
    dtDelta = stopWorkTime - startWorkTime   
    numHours = round((2 * dtDelta.seconds / 60 / 60),0) / 2
    trackHours(location, startWorkTime, numHours, parser)

def lapClock(location, currentTime, parser):
    stopClock(location, parser)
    startClock(location, currentTime, parser)
    