import tskript



#
# Main()
#

# TODO: P2: Change location change threshold (e.g., time difference > 
#       2 x interval, clock off and restart clock)
# TODO: P2: Refactor to use categories for locations:
#       VPN -> Work
#       Office -> Work

parser.set("Pytask","lastaction","launch")
currentLocation = tskript.getCurrentLocation(parser)
changeType = tskript.contextChange(currentLocation, currentTime, parser)
if changeType > 1:
    tskript.handleContextChange(changeType, currentLocation, currentTime, parser)
   
tskript.updateConfig(currentTime, currentLocation, parser)
