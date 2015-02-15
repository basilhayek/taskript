# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:54:06 2015

@author: bhayek
"""

import Tkinter
from datetime import datetime, timedelta
import webbrowser
import workclock

def copyToClipboard(string):
    r = Tkinter.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(string)
    r.destroy()

def timecardToClipboard(weekEnding):
    fileName = 'TimeCard-' + weekEnding + '.txt'
    fileIn = open('.//data//' + fileName, 'r')
    timecard = fileIn.read()
    copyToClipboard(timecard)

def updateValues(timecard, parser):
    #TODO: P3 - Fix this to be dynamic
    sites = ['Client','Work']    
    for site in sites:
        dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        for day in dow:
            dayHours = parser.get('Tracking.' + site, day)
            timecard = timecard.replace('<' + day.upper() + '>', dayHours)
    return timecard

def getWeekEnding(weekContaining, dow):
    weekEnding = weekContaining + timedelta( (dow-weekContaining.weekday()) % 7 )
    return weekEnding.date()

def saveTimecard(weekContaining, parser):
    weekEnding = getWeekEnding(weekContaining, 6).strftime("%Y-%m-%d")
    fileName = 'TimeCard-' + weekEnding + '.txt'
    fileIn = open('.//data//TimeCardTemplate125474.txt', 'r')
    timecard = updateValues(fileIn.read(), parser)
    date = datetime.strptime(weekEnding, "%Y-%m-%d")
    timecard = timecard.replace('<WE:DD-Mmm-YYYY>', date.strftime('%d-%b-%Y'))
    fileOut = open('.//data//' + fileName, 'w')
    fileOut.write(timecard)

def submitTimecard(currentLocation, parser):
    nextSubmit = datetime.strptime(parser.get('Tracking','week'), '%Y-%m-%d') 

    timecardURL = 'http://timetracking/upload.aspx'
    if currentLocation == 'Home':
        timecardURL = 'https://us.webvpn.sapient.com/,DanaInfo=timetracking+Upload.aspx'
   
    timecardToClipboard(nextSubmit.strftime('%Y-%m-%d'))
   
    nextSubmit = nextSubmit + timedelta(days=7)
    workclock.updateTracking(nextSubmit, parser)       
   
    webbrowser.open(timecardURL)
