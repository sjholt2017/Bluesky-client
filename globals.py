# Import Python modules
import logging

# Global Vairables
logonID = ""
password = ""
versionNumber = "0.1 (draft)"
notificationsRefreshInterval = 300000 # 5 minutes
feedRefreshInterval = 300000 # 5 minutes
logfileName = "blueskyapp.log"
firstTimeFeed = True
lastUpdated = ""

# Logging Configuration
logging.basicConfig(filename=logfileName,
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()
