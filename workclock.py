# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:35:21 2015

@author: bhayek
"""

from datetime import datetime

def updateTracking(nextSubmit, parser):
    parser.set('Pytask','lastAction','updateTracking()')
    parser.set('Tracking', 'week', nextSubmit.strftime('%Y-%m-%d'))
    dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] 
    for day in dow:
        parser.set('Tracking',day,str(0))

def trackHours(startWorkTime, numHours, parser):
    parser.set('Tracking',startWorkTime.strftime("%A")[0:3], str(numHours))

def startWorkClock(currentTime, parser):
    parser.set('Pytask','lastAction','startWorkClock()')
    parser.set('Work', 'start', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
    parser.set('Work', 'last', currentTime.strftime("%Y-%m-%d %H:%M:%S"))
    parser.remove_option('Work', 'stop')

def stopWorkClock(parser):
    parser.set('Pytask','lastAction','stopWorkClock()')
    strTemp = parser.get('Work', 'last')
    parser.set('Work', 'stop', strTemp)
    stopWorkTime = datetime.strptime(strTemp, "%Y-%m-%d %H:%M:%S")
    startWorkTime = datetime.strptime(parser.get('Work', 'start'),"%Y-%m-%d %H:%M:%S")
    dtDelta = stopWorkTime - startWorkTime    
    numHours = round((2 * dtDelta.seconds / 60 / 60),0) / 2
    trackHours(startWorkTime, numHours, parser)

def lapWorkClock(currentTime, parser):
    stopWorkClock(parser)
    startWorkClock(currentTime, parser)
    