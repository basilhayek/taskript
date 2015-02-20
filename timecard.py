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

def writeBlankRows(rowNum, timecard, parser):
    timecardRow = parser.get('Timecard','row.blank')
    timecardRow = timecardRow.replace("<ROW>", str(rowNum))
    timecard = timecard + timecardRow.replace("\\n","\n").replace("\\t","\t")
    return timecard
    
def writeLocationHours(rowNum, location, timecard, parser):
    dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    timecardRow = parser.get('Timecard','row.hours')
    for day in dow:
        dayHours = parser.get('Tracking.' + location, day)
        timecardRow = timecardRow.replace('<' + day.upper() + '>', dayHours)
    timecardRow = timecardRow.replace("<PID>", "125474")
    timecardRow = timecardRow.replace("<ROW>", str(rowNum))
    timecardRow = timecardRow.replace("<LOCATION>", parser.get("Timecard", "location." + location))
    timecard = timecard + timecardRow.replace("\\n","\n").replace("\\t","\t")
    return timecard

def getWeekEnding(weekContaining, dow):
    weekEnding = weekContaining + timedelta( (dow-weekContaining.weekday()) % 7 )
    return weekEnding.date()

def prepareTimecard(weekEnding, parser):
    fileIn = open('.//data//TimeCardTemplateGeneric.txt', 'r')
    timecard = fileIn.read()    
    timecard = timecard.replace('<WE:DD-Mmm-YYYY>', weekEnding.strftime('%d-%b-%Y'))
    return timecard

def writeTimecard(weekEnding, timecard):
    fileName = 'TimeCard-' + weekEnding.strftime("%Y-%m-%d") + '.txt'
    fileOut = open('.//data//' + fileName, 'w')
    fileOut.write(timecard)
    fileOut.close()

def saveTimecard(weekContaining, parser):
    weekEnding = getWeekEnding(weekContaining, 6)
    timecard = prepareTimecard(weekEnding, parser)
    numRows = 0
    #TODO: P3 - Fix this to be dynamic
    sites = ['Client','Work']    
    for site in sites:
        numRows = numRows + 1
        timecard = writeLocationHours(numRows, site, timecard, parser)
    for rowNum in range(numRows + 1, 21):
        timecard = writeBlankRows(rowNum, timecard, parser)
    writeTimecard(weekEnding, timecard)

def submitTimecard(currentLocation, parser):
    nextSubmit = datetime.strptime(parser.get('Tracking','week'), '%Y-%m-%d') 

    timecardURL = 'http://timetracking/upload.aspx'
    if currentLocation == 'Home':
        timecardURL = 'https://us.webvpn.sapient.com/,DanaInfo=timetracking+Upload.aspx'
   
    timecardToClipboard(nextSubmit.strftime('%Y-%m-%d'))
   
    nextSubmit = nextSubmit + timedelta(days=7)
    workclock.resetTracking(nextSubmit, parser)       
   
    webbrowser.open(timecardURL)
