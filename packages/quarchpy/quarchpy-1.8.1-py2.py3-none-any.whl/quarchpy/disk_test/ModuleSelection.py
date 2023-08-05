#!/usr/bin/env python
'''
This contains useful functions to help with quarch module selection

########### VERSION HISTORY ###########

13/08/2018 - Andy Norrie    - First version, based on initial work from Pedro Leao
'''

from device import quarchDevice
from connection_specific.connection_QPS import QpsInterface
from device_specific.quarchQPS import quarchQPS

def GetQpsModuleSelection (QpsConnection):
    
    # Request a list of all USB and LAN accessible power modules
    devList = QpsConnection.getDeviceList()
    # Removes rest devices
    devList = [ x for x in devList if "rest" not in x ]

    # Print the devices, so the user can choose one to connect to
    print ("\n ########## STEP 1 - Select a Quarch Module. ########## \n")
    print (' --------------------------------------------')
    print (' |  {:^5}  |  {:^30}|'.format("INDEX", "MODULE"))
    print (' --------------------------------------------')
        
    try:
        for idx in xrange(len(devList)):
            print (' |  {:^5}  |  {:^30}|'.format(str(idx+1), devList[idx]))
            print(' --------------------------------------------')
    except:
        for idx in range(len(devList)):
            print (' |  {:^5}  |  {:^30}|'.format(str(idx+1), devList[idx]))
            print(' --------------------------------------------')

    # Get the user to select the device to control
    try:
        moduleId = int(raw_input ("\n>>> Enter the index of the Quarch module: "))
    except NameError:
        moduleId = int(input ("\n>>> Enter the index of the Quarch module: "))

    # Verify the selection
    if (moduleId > 0 and moduleId <= len(devList)):
        myDeviceID = devList[moduleId-1]
    else:
        myDeviceID = None

    return myDeviceID