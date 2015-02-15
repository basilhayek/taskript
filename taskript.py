import ConfigParser
from datetime import datetime
import tskript 

currentTime = datetime.now()
parser = ConfigParser.SafeConfigParser()
parser.read('taskript.ini')

# TODO: P2: Handle work at the client site
# TODO: P3: Handle additional hours (work->home->work scenario)

#
# Main()
#

parser.set("Pytask","lastaction","launch")
currentLocation = tskript.getCurrentLocation(parser)
changeType = tskript.contextChange(currentLocation, currentTime, parser)
if changeType > 0:
    tskript.handleContextChange(changeType, currentLocation, currentTime, parser)
    
tskript.updateConfig(currentTime, currentLocation, parser)