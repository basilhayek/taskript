# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:51:54 2015

@author: bhayek
"""

import ConfigParser
import socket
from datetime import datetime

# TODO: P2: Refactor INI file to separate tskript vs activity

def getIPOctets(ipAddress, numOctets):
    if numOctets == 4:
        return ipAddress
    posDot = 0
    for i in range(0, numOctets):
        posDot = ipAddress.find('.', posDot + 1)
    strAddress = ipAddress[0:posDot]
    return strAddress

def getCurrentLocation(parser):
    currentIP = socket.gethostbyname(socket.gethostname())
    matchIP = getIPOctets(currentIP, 2)
    currentLocation = parser.get('IPMapping',matchIP)
    return currentLocation

class tscontext:
    def __init__(self, config):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.optionxform = str
        self.parser.read(config)
        self._config = config
        
        self.curLoc = getCurrentLocation(self.parser)
        self.curTim = datetime.now()

        self._reload()
        self.log("init()")
        self.ping()
        
    def _debugset(self, lasLoc, lasTim, curLoc, curTim):
        self.parser.set('Pytask', 'lastLocation', lasLoc)
        self.parser.set('Pytask', 'lastRun', lasTim.strftime("%Y-%m-%d %H:%M:%S"))
        self._reload()
        self.curTim = curTim
        self.curLoc = curLoc
    
    def _reload(self):
        self.lasLoc = self.parser.get('Pytask','lastLocation')
        self.lasTim = datetime.strptime(self.parser.get('Pytask','lastRun'),"%Y-%m-%d %H:%M:%S") 
        
    def ping(self):
        self.parser.set('Pytask', 'lastLocation', self.curLoc)
        self.parser.set('Pytask', 'lastRun', self.curTim.strftime("%Y-%m-%d %H:%M:%S"))
        
    def close(self):
        self.parser.write(open(self._config, 'w'))
    
    def log(self, action):
#        print action
        self.parser.set("Pytask", "lastAction", action)
    
    def getCategory(self, location):
        return self.parser.get('LocationCategory', location)
        
    def _compareCategory(self, location, checkCategory):
        category = self.getCategory(location)
        return (category==checkCategory)

    def wasCategory(self, checkCategory):
        return self.compareCategory(self.lasLoc, checkCategory)
        
    def isCategory(self, checkCategory):
        return self._compareCategory(self.curLoc, checkCategory)

    def isLocationContextChange(self):
        if self.isCategory('unknown'):
            return False
        else:
            return (self.getCategory(self.curLoc) != 
                    self.getCategory(self.lasLoc))
                    
    def isDateContextChange(self):
        return self.curTim.date() != self.lasTim.date()
            
    def isWeekContextChange(self):
        nextSubmit = datetime.strptime(self.parser.get('Tracking', 'week'),
                                       '%Y-%m-%d')
        return self.curTim.date() > nextSubmit.date()
        
# TODO: P3: Add additional contexts (Month, Hour)