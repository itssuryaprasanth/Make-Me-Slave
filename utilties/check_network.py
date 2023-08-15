import os
import sys
from utilties.customlogger import file_logger

log = file_logger()


def ping_to_destination_network():
    log.debug("Checking {} is reachable or not".format(sys.argv[1]))
    hostname = sys.argv[1]
    try:
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            log.info("Network is reachable")
            print("VPN connection is successfully")
        else:
            log.debug("Network is not reachable")
            sys.exit(1)
    except:
        log.debug("Error, ping to destination network {}".format(sys.exc_info()))
        sys.exit(1)


ping_to_destination_network()
