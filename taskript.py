import tskript
import workclock

# TODO: P2: Change location change threshold (e.g., time difference > 
#       2 x interval, clock off and restart clock)

#
# Main()
#

tscontext = tskript.tscontext('taskript.ini')
parser = tscontext.parser
clock = workclock.ClockPunch(parser)
clock.handleContext(tscontext)

tscontext.close()
