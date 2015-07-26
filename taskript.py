import tskript
import workclock

# TODO: P2: Change location change threshold (e.g., time difference > 
#       2 x interval, clock off and restart clock)

# TODO: P1: Prompt when unknown location

# TODO: P1: How to check for more robust location by IP address
# http://pythonhosted.org/python-geoip/ -- Reports NH for Wells
# Use JSON: http://api.hostip.info/get_json.php

# TODO: P2: Fix location recognition for timecard submission; 10.0 => No VPN
# 

#
# Main()
#

tscontext = tskript.tscontext('taskript.ini')
parser = tscontext.parser
clock = workclock.ClockPunch(parser)
clock.handleContext(tscontext)

tscontext.close()
