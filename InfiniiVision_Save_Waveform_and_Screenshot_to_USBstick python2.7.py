# -*- coding: utf-8 -*-

## DO NOT CHANGE ABOVE LINE

# Python for Test and Measurement
#
# Requires VISA installed on Control PC
# 'keysight.com/find/iosuite'
# Requires PyVISA to use VISA in Python
# 'http://pyvisa.sourceforge.net/pyvisa/'

## Keysight IO Libraries 17.1.19xxx
## Anaconda Python 2.7.7 64 bit
## pyvisa 1.8
## Windows 7 Enterprise, 64 bit

##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
## Copyright © 2015 Keysight Technologies Inc. All rights reserved.
##
## You have a royalty-free right to use, modify, reproduce and distribute this
## example files (and/or any modified version) in any way you find useful, provided
## that you agree that Keysight has no warranty, obligations or liability for any
## Sample Application Files.
##
##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

##############################################################################################################################################################################
##############################################################################################################################################################################
## Import Python modules
##############################################################################################################################################################################
##############################

## Import python modules - Not all of these are used in this program; provided for reference
import sys
import visa
import time
import struct
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

##############################################################################################################################################################################
##############################################################################################################################################################################
## Intro, general comments, and instructions
##############################################################################################################################################################################
##############################################################################################################################################################################

## This example program is provided as is and without support. Keysight is not responsible for modifications.
## Standard Python style is not followed to allow for easier reading by non-Python programmers.

## Keysight IO Libraries 17.1.19xxx was used.
## Anaconda Python 2.7.7 64 bit is used
## pyvisa 1.8 is used
## Windows 7 Enterprise, 64 bit (has implications for time.clock if ported to unix type machine, use time.time instead)

## HiSlip and Socket connections not supported

## DESCRIPTION OF FUNCTIONALITY
## Shows how to save a screenshot and waveforms to a USB stick, with error checking.
##
## This script should work for all InfiniiVision and InfiniiVision-X oscilloscopes:
## DSO5000A, DSO/MSO6000A/L, DSO/MSO7000A/B, EDU/DSOX1000A/G, DSO/MSO-X2000A, DSO/MSO-X3000A/T, DSO/MSO-X4000A, DSO/MSO-X6000A, M924xA PXIe scopes

##############################################################################################################################################################################
##############################################################################################################################################################################
## DEFINE CONSTANTS
##############################################################################################################################################################################
##############################################################################################################################################################################

## Initialization constants
SCOPE_VISA_ADDRESS = "USB0::0x0957::0x179B::MY51452776::0::INSTR" # Get this from Keysight IO Libraries Connection Expert #Note: sockets are not supported in this revision of the script, and pyVisa 1.6.3 does not support HiSlip
GLOBAL_TOUT =  10000 # IO time out in milliseconds

##############################################################################################################################################################################
##############################################################################################################################################################################
## Define a Python helper function
##############################################################################################################################################################################
##############################################################################################################################################################################

## Define Error Check function
def ErrCheck(TARGET_INSTRUMENT):
    myError = []
    ErrorList = TARGET_INSTRUMENT.query(":SYSTem:ERRor?").split(',')
    Error = ErrorList[0]
    while int(Error)!=0:
        print("Error #: " + ErrorList[0])
        print("Error Description: " + ErrorList[1])
        myError.append(ErrorList[0])
        myError.append(ErrorList[1])
        ErrorList = TARGET_INSTRUMENT.query(":SYSTem:ERRor?").split(',')
        Error = ErrorList[0]
        myError = list(myError)
    return myError

##############################################################################################################################################################################
##############################################################################################################################################################################
## Connect and initialize scope
##############################################################################################################################################################################
##############################################################################################################################################################################

## Define VISA Resource Manager & Install directory
## This directory will need to be changed if VISA was installed somewhere else.
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
## This is more or less ok too: rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
## In fact, it is generally not needed to call it explicitly
## rm = visa.ResourceManager()

## Open Connection
## Define & open the scope by the VISA address ; # This uses PyVisa
try:
    KsInfiniiVisionX = rm.open_resource(SCOPE_VISA_ADDRESS)
except Exception:
    print("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n")
    sys.exit()

## Set Global Timeout
## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
KsInfiniiVisionX.timeout = GLOBAL_TOUT

## Clear the instrument bus
KsInfiniiVisionX.clear()

## Clear any previously encountered errors
KsInfiniiVisionX.write("*CLS")

##############################################################################################################################################################################
##############################################################################################################################################################################
## Get and parse the IDN string to determine scope generation
##############################################################################################################################################################################
##############################################################################################################################################################################

## Get and parse IDN string
IDN = str(KsInfiniiVisionX.query("*IDN?"))
## Parse IDN
IDN = IDN.split(',') # IDN parts are separated by commas, so parse on the commas
#mfg = IDN[0] # Python indices start at 0
model = IDN[1]
#SN = IDN[2]
#FW = IDN[3]

scopeTypeCheck = list(model)
if scopeTypeCheck[3] == "-" or scopeTypeCheck[1] == "9":
    generation = "IVX"
else:
    generation = "IVnotX"
del IDN, scopeTypeCheck, model

##############################################################################################################################################################################
##############################################################################################################################################################################
## Save screenshot to USB stick
##############################################################################################################################################################################
##############################################################################################################################################################################

## USB Stick Notes:
    ## USB stick format must be FAT32 format. NTFS not supported.  Most sticks will work, sometimes larger ones do not.
        ## The older, not X scopes only had USB Full Speed host ports, much slower than the High Speed ports on the X scopes, so consider changing the timeout here...
    ## External drives and DC/DVD drives are not supported

TYPE = "png"
filename = "my_screenshot"
location = "" # to select a subfolder... "" means no subfolder.  An example would be "\USB\myfolder\"
    ## Just \USB\... works for the front panel, but the rear panel will be \USBx\ where x is an integer... manually check on the scope...

KsInfiniiVisionX.query(":SYSTEM:DSP '';*OPC?") # Turns of previously displayed (non-error) message

## Main screenshot saving setup commands
KsInfiniiVisionX.write(':SAVE:FILename "' + str(filename) + '"')
    ## Hard to read... it is actually: :SAVE:FILename "my_screenshot" <- notice there is no file extension here
if generation == "IVnotX":
    KsInfiniiVisionX.write(":SAVE:IMAGe:AREA SCReen") # The newer InfiniiVision-Xs do not have this
    # KsInfiniiVisionX.timeout = 50000 # 50 seconds see notes above
KsInfiniiVisionX.write(":SAVE:IMAGe:FACTors 0") # Save scope setup info as text file (0 = no, 1 = yes)
KsInfiniiVisionX.write(":SAVE:IMAGe:FORMat " + str(TYPE))
KsInfiniiVisionX.write(":SAVE:IMAGe:INKSaver 0")
KsInfiniiVisionX.write(":SAVE:IMAGe:PALette COLor")
print("Saving screenshot to USB stick.\n")
try:
    KsInfiniiVisionX.query(':SAVE:IMAGe:STARt "' + str(location) + str(filename) + "." + str(TYPE) +'";*OPC?') # Actually start saving it to a USB stick, wait for *OPC? to come back with a 1 (this is a blcoking commands, so *OPC? cannot get processed until it is done saving the screenshot)
        ## Hard to read.... it is actually: :SAVE:IMAGe:STARt "my_screenshot.png";*OPC?
        ## Note that here *OPC? works well, but DOES NOT when saving waveforms to a stick; a different method is presented below for that.
    ## Typically this will be in less than 10 seconds... so as long as the timeout is 10s or more, this should be just fine.
    Screenshot_Error = ErrCheck(KsInfiniiVisionX)
    if len(Screenshot_Error) == 0:
        print("Screenshot saved to USB stick without error.")
        del Screenshot_Error
    else:
        raise # Raise an error in Python, which will be caught by the follow excpet  block
except:
    print("Failed at saving a screenshot to a USB stick, or some other error in this process. If a timeout did not occur, check that a USB stick is inserted and that you can manually save a file to the USB tick.  If not, try a different USB stick. If a timeout did occur, increase the timeout.\n")
    print("Aborting script and properly closing scope.\n")
    KsInfiniiVisionX.clear() # Clear scope communications interface
    KsInfiniiVisionX.close() # Close communications interface to scope
    sys.exit()
### Reset the timeout if it was changed for this operation

##############################################################################################################################################################################
##############################################################################################################################################################################
## Save waveform to USB Stick
##############################################################################################################################################################################
##############################################################################################################################################################################

## USB Stick Notes:
    ## USB stick format must be FAT32 format. NTFS not supported.  Most sticks will work, sometimes larger ones do not.
        ## The older, not X scopes only had USB Full Speed host ports, much slower than the High Speed ports on the X scopes, so consider changing the timeout here...
    ## External drives and CD/DVD drives are not supported

## Other note(s):
    ## It is not necessary to specify which channels to save.  All displayed channels are saved.

#####################################################
## Prelimary stuff: ensure there is something to save
KsInfiniiVisionX.write(":TIMebase:SCALe 100 NS") # Set timescale to something fast so we do not have to wait too long
er = str(KsInfiniiVisionX.query("SYST:ERR?"))
KsInfiniiVisionX.write(":TIMebase:POSition 0")
KsInfiniiVisionX.write(":TRIGger:MODE EDGE") # Set trigger type to edge
KsInfiniiVisionX.query(":TRIGger:EDGE:SOURce LINE;*OPC?") # Set trigger source to LINE, so there is ANYTHING to trigger on ; triggers gets set below, so ok to leave this alone
KsInfiniiVisionX.write(":SINGle") # Do a :SINGle to fill up the memory and check the memory size (this is not a proper synchronization, but will work here)
time.sleep(.5)

#####################################################
## Prelimary stuff: Save format, location, name
TYPE = "ASCiixy" # "CSV" or "ASCiixy" or "BINary"
    ## ASCii xy and bianry save data to separate files
    ## MATH channels can only be saved in CSV format
    ## see below for further comments
filename = "my_waveform"
location = "" # to select a subfolder... "" means no subfolder.  An example would be "\USB\myfolder\"
    ## Just \USB\... works for the front panel, but the rear panel will be \USBx\ where x is an integer... manually check on the scope...

KsInfiniiVisionX.write(':SAVE:FILename "' + str(filename) + '"')
    ## Hard to read... it is actually: :SAVE:FILename "my_waveform" <- notice there is no file extension here
KsInfiniiVisionX.write(":SAVE:WAVeform:FORMat " + str(TYPE))
    ## ASCiixy & BINary: these are basically the same record, all points in memory that are within current the timebase.  The below CSV format uses a subset of these.  The max record lengths here are the max memories of the given oscilloscope.  ASCiixy is in csv format, thus it is easy to deal with, but can take a LONG time to save.  Binary is fast and small, but must later be extracted.  An example is provided for this.
	## Binary not recommended to include the setup info as it just makes reading the file harder.
    ## CSV: This is essentially the “measurement record,” which is what the oscilloscope would return if it were queried with the :WAVeform:PONts:MODE NORMAL command.  It represents what is SEEN on screen.  Using a long time base to bring it all on screen should not be used in this method.  It is saved in csv format.
	## Actual max lengths in CSV format depend on oscilloscope, timebase and settings.
	## DSO5000A, MSO/DSO6000A/L: max standard record is 1,000 pts; w/ “Precision” mode on, 10,000 Pts
	## MSO/DSO7000A/B: max standard record is 1,000 pts; w/ “Precision” mode on, ~128,000 Pts
	## X2000A, X3000A/T, X4000A: max standard record is ~65k pts, No “Precision” mode
	## X6000A: max standard record is ~65k pts, “Precision” mode record lengths are adjustable from 100,000 to 1,000,000 points
	## In all cases, this is what math waveforms use.

## Ask for and adjust length as needed
##PoinActuallyAvail = int(KsInfiniiVisionX.query(":SAVE:WAVeform:LENGth?"))
##KsInfiniiVisionX.write(":SAVE:WAVeform:LENGth " + str(PoinActuallyAvail))
##KsInfiniiVisionX.query(":TIMebase:SCALe 50 S;*OPC?") # Set timebase to longest so all data will be on screen to be saved, else only the points in on the display will be saved
    ## Not for CSV format ever
KsInfiniiVisionX.write(":SAVE:WAVeform:LENGth 1000") ## This can take LONG TIME for ASCII.  You will need to increase the timeout here!!!! A LOT if using ASCII and a lot of points... 1000 Pts will not need a longer timeout
    ## Minimum is 100, max depnds on scope and settings

#####################################################
#####################################################
## Actually save
print("Now saving waveforms to USB stick.\n")
KsInfiniiVisionX.query("*CLS;*OPC?") # Clear all registers before issuing the command to save the data; this is necessary so we can properly determine when the scope is done saving data.
KsInfiniiVisionX.write(':SAVE:WAVeform:STARt "' +  str(location) + str(filename) +'"') # Actually start saving it to a USB stick, wait for *OPC? to come back with a 1
## Hard to read.... it actually read:  :SAVE:WAVeform:STARt "my_waveform" <- note there is no filename extension here

## Now we check the IOC (IO Complete) and IOF (IO Fail) bits on the Operation Event Register to know when it is done saving....

## First definite IOC and IOF criterion:
IO_COMPLETE_BIT = 13 #  the IOC bit is bit-weigh 13 in the Operation Event Register
IO_COMPLETE_MASK = 1<< IO_COMPLETE_BIT # << is a left shift; 1<<13 = 8192 = 2 raised to 13;
IO_COMPLETE = 1 << IO_COMPLETE_BIT
IO_NOT_COMPLETE = 0

IO_FAIL_BIT = 14 #  the IOC bit is bit-weigh 14 in the Operation Event Register
IO_FAIL_MASK = 1<< IO_FAIL_BIT # << is a left shift; 1<<14 = 16384 = 2 raised to 14;
IO_FAIL = 1<< IO_FAIL_BIT
IO_NOT_FAIL = 0

## Define IOF and IOC initial states:
IOC_STATUS = 0
IOF_STATUS = 0

## Begin checking for IO_Status
while IOF_STATUS ==  IO_NOT_FAIL and IOC_STATUS == IO_NOT_COMPLETE: # Note there is no time qualification here... it should just eventually be done, or fail... eventually.
    Status = int(KsInfiniiVisionX.query(":OPER:EVENt?")) # DO NOT use :OPERation
    IOC_STATUS = Status & IO_COMPLETE_MASK # A bitwise and of Status IO_COMPLETE_MASK
    IOF_STATUS = Status & IO_FAIL_MASK
    if IOF_STATUS == IO_FAIL:
        print("FAILED saving waveforms to USB stick.\n")
        print("Check that a USB stick is inserted and that you can manually save a file to the USB tick.  If not, try a different USB stick.\n")
        print("Aborting script and properly closing scope.\n")
        KsInfiniiVisionX.clear() # Clear scope communications interface
        KsInfiniiVisionX.close() # Close communications interface to scope
        sys.exit()
    if IOC_STATUS == IO_COMPLETE: # you need to do this last. If you were to remvoe the USB stick whiel it is saving, it will say that the IO operation is both failed and done...
        print("Done saving waveforms to USB stick.\n")
        break # Break out of while loop to avoid the wait time below
    time.sleep(0.1) # Pause 100 ms to prevent excessive queries (probably ok to go faster)

##############################################################################################################################################################################
##############################################################################################################################################################################
## Done - cleanup
##############################################################################################################################################################################
##############################################################################################################################################################################

KsInfiniiVisionX.clear() # Clear scope communications interface
KsInfiniiVisionX.close() # Close communications interface to scope

print("Done.")