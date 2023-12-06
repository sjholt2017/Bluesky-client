#
# Module: writeLogfile
#

# Import Python modules
import sys
import logging

#
# Function: Log any info/error messages to log file
#
def log(message, messageType):

    # Get calling function name
    callingFunction = sys._getframe(1).f_code.co_name

    # Format log message text
    if messageType == "E":
        logMessageText = " Function:" + callingFunction + " > " + message
    else:
        logMessageText = message        

    # Log error
    #print (logMessageText) # Display in console
    if messageType == "E":
        logging.error(logMessageText)
    elif messageType == "I":
        logging.info(logMessageText)
    else:
        logging.error("Unknown Log Message Type")
        
