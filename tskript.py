# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:51:54 2015

@author: bhayek
"""

import socket
from datetime import datetime
import workclock
import timecard

def getIPOctets(ipAddress, numOctets):
    if numOctets == 4:
        return ipAddress
    posDot = 0
    for i in range (0, numOctets):
        posDot = ipAddress.find('.', posDot + 1) 
    strAddress = ipAddress[0:posDot]
    return strAddress

def weekChange(currentTime, parser):
    nextSubmit = datetime.strptime(parser.get('Tracking','week'), '%Y-%m-%d')  
    if currentTime > nextSubmit:
        return True

def locationChange(currentLocation, parser):
    lastLocation = parser.get('Pytask','lastLocation')
    if (currentLocation != 'ignore') and (lastLocation != currentLocation):
        return True
        
def dateChange(currentTime, parser):
    lastTime = datetime.strptime(parser.get('Pytask', 'lastrun'), "%Y-%m-%d %H:%M:%S")
    if lastTime.date() != currentTime.date():
        return True

def handleContextChange(changeType, currentLocation, currentTime, parser):
    # Handle location changes
    if changeType & 1 == 1:
        # At work, coming from somewhere different, so start the clock
        if currentLocation == 'Work':
            workclock.startWorkClock(currentTime, parser)
        # Got home from work, stop the work clock and record the time
        if currentLocation == 'Home':
            workclock.stopWorkClock(parser)
    
    # Handle date rollover at work
    if changeType & 2 == 2:
        # This only matters if at work
        if currentLocation == 'Work':
            workclock.lapWorkClock(currentTime, parser)
            
    # Handle time card submission
    if changeType & 4 == 4:
        timecard.submitTimecard(currentLocation, parser)

def contextChange(currentLocation, currentTime, parser):
    changeType = 0
    if locationChange(currentLocation, parser):
        changeType = 1
    if dateChange(currentTime, parser):
        changeType = changeType + 2
    if weekChange(currentTime, parser):
        changeType = changeType + 4
    parser.set('Pytask','lastAction','contextChange()=' + str(changeType))
    return changeType

def getCurrentLocation(parser):
    currentIP = socket.gethostbyname(socket.gethostname())
    matchIP = getIPOctets(currentIP, 2)
    currentLocation = parser.get('Location',matchIP)
    return currentLocation

def updateConfig(currentTime, currentLocation, parser):
    strTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    parser.set('Pytask', 'lastRun', strTime)
    parser.set('Pytask', 'lastLocation', currentLocation)
    if currentLocation == 'Work':
        parser.set(currentLocation, 'last', strTime)
    parser.write(open('taskript.ini', 'w'))
