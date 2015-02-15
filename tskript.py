# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:51:54 2015

@author: bhayek
"""

import socket
from datetime import datetime
import workclock
import timecard

def isTrackedLocation(location, parser):
    return parser.getboolean('Location', 'Track.' + location)

def getIPOctets(ipAddress, numOctets):
    if numOctets == 4:
        return ipAddress
    posDot = 0
    for i in range(0, numOctets):
        posDot = ipAddress.find('.', posDot + 1)
    strAddress = ipAddress[0:posDot]
    return strAddress

def locationChange(currentLocation, parser):
    locChangeType = 0
    lastLocation = parser.get('Pytask', 'lastLocation')
    if (currentLocation != 'ignore') and (lastLocation != currentLocation):
        locChangeType = 1
    if isTrackedLocation(lastLocation, parser):
        locChangeType = locChangeType | 2
    if isTrackedLocation(currentLocation, parser):
        locChangeType = locChangeType | 4
    return locChangeType

def dateChange(currentTime, parser):
    dateChangeType = 0
    lastTime = datetime.strptime(parser.get('Pytask', 'lastrun'),
                                 "%Y-%m-%d %H:%M:%S")
    if lastTime.date() != currentTime.date():
        dateChangeType = 1
        nextSubmit = datetime.strptime(parser.get('Tracking', 'week'),
                                       '%Y-%m-%d')
        if currentTime.date() > nextSubmit.date():
            dateChangeType = dateChangeType | 2
    return dateChangeType


def handleContextChange(changeType, currentLocation, currentTime, parser):
    # Handle location changes

    trackLocation = parser.getboolean("Location", "Track." + currentLocation)
    lastLocation = parser.get("Pytask", "lastLocation")
    if changeType & 1 == 1:
        # We have changed locations, and need to track the current location
        if trackLocation:
            workclock.stopClock(lastLocation, parser)
            workclock.startClock(currentLocation, currentTime, parser)
        # Changed locations, but no need to track the current location
        else:
            workclock.stopClock(lastLocation, parser)

    # Handle date rollover at work
    if changeType & 16 == 16:
        # This only matters if we're at a place where we should track time
        if trackLocation:
            workclock.lapClock(currentLocation, currentTime, parser)

    # Handle time card submission
    if changeType & 32 == 32:
        timecard.submitTimecard(currentLocation, parser)

def contextChange(currentLocation, currentTime, parser):
    changeType = locationChange(currentLocation, parser)
    changeType = changeType | (dateChange(currentTime, parser) << 4)
    parser.set('Pytask', 'lastAction', 'contextChange()=' + str(changeType))
    return changeType

def getCurrentLocation(parser):
    currentIP = socket.gethostbyname(socket.gethostname())
    matchIP = getIPOctets(currentIP, 2)
    currentLocation = parser.get('IPMapping',matchIP)
    return currentLocation

def updateConfig(currentTime, currentLocation, parser):
    strTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    parser.set('Pytask', 'lastRun', strTime)
    parser.set('Pytask', 'lastLocation', currentLocation)
    if isTrackedLocation(currentLocation, parser):
        workclock.pingClock(currentLocation, currentTime, parser)
    parser.write(open('taskript.ini', 'w'))
