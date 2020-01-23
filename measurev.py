# *********************************************************
# This program illustrates a few commonly-used programming
# features of your Keysight oscilloscope.
# *********************************************************
# Import modules.
# ---------------------------------------------------------
import visa
import string
import struct
import sys
import requests

# Global variables (booleans: 0 = False, 1 = True).
# ---------------------------------------------------------
debug = 0
# =========================================================
# Send a command and check for errors:
# =========================================================
def do_command(command, hide_params=False):
    if hide_params:
        (header, data) = string.split(command, " ", 1)
        if debug:
            print("\nCmd = '%s'" % header)
    else:
        if debug:
            print("\nCmd = '%s'" % command)

    InfiniiVision.write("%s" % command)

    if hide_params:
        check_instrument_errors(header)
    else:
        check_instrument_errors(command)

# =========================================================
# Send a command and binary values and check for errors:
# =========================================================
def do_command_ieee_block(command, values):
    if debug:
        print("Cmb = '%s'" % command)
    InfiniiVision.write_binary_values("%s " % command, values, datatype='c')
    check_instrument_errors(command)

# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query):
    if debug:
        print("Qys = '%s'" % query)
    result = InfiniiVision.query("%s" % query)
    check_instrument_errors(query)
    return result

# =========================================================
# Send a query, check for errors, return floating-point value:
# =========================================================
def do_query_number(query):
    if debug:
        print("Qyn = '%s'" % query)
    results = InfiniiVision.query("%s" % query)
    check_instrument_errors(query)
    return float(results)

# =========================================================
# Send a query, check for errors, return binary values:
# =========================================================
def do_query_ieee_block(query):
    if debug:
        print("Qys = '%s'" % query)
    result = InfiniiVision.query_binary_values("%s" % query, datatype='s')
    check_instrument_errors(query)
    return result[0]

# =========================================================
# Check for instrument errors:
# =========================================================
def check_instrument_errors(command):
    while True:
        error_string = InfiniiVision.query(":SYSTem:ERRor?")
        if error_string:  # If there is an error string value.
            if error_string.find("+0,", 0, 3) == -1:  # Not "No error".

                print("ERROR: %s, command: '%s'" % (error_string, command))
                print("Exited because of error.")
                sys.exit(1)

            else:  # "No error"
                break
        else:  # :SYSTem:ERRor? should always return string.
            print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
            print("Exited because of error.")
            sys.exit(1)


#def capture():

def analyze():
    # Make measurements.
    # --------------------------------------------------------
    do_command(":MEASure:VMAX")
    qresult_vmax = do_query_string(":MEASure:VMAX?")
    #print("VMAX : %s" % qresult_vmax)

    do_command(":MEASure:VMIN")
    qresult_vmin = do_query_string(":MEASure:VMIN?")
   # print("VMIN : %s" % qresult_vmin)

    do_command(":MEASure:VPP")
    qresult_vpp = do_query_string(":MEASure:VPP?")
    #print("VPP : %s" % qresult_vpp)

    do_command(":MEASure:VAMPlitude")
    qresult_vam = do_query_string(":MEASure:VAMPlitude?")
    #print("V amplitude : %s" % qresult_vam)

    do_command(":MEASure:VAVerage")
    qresult_vav = do_query_string(":MEASure:VAVerage?")
    #print("V average : %s" % qresult_vav)

    do_command(":MEASure:FREQuency")
    qresult_fre = do_query_string(":MEASure:FREQuency?")
    #print("Frequency: %s" % qresult_fre)

    do_command(":MEASure:PERiod")
    qresult_per = do_query_string(":MEASure:PERiod?")
    #print("Period : %s" % qresult_per)




# =========================================================
# Main program:
# =========================================================

rm = visa.ResourceManager()
InfiniiVision = rm.open_resource("USB0::0x0957::0x179B::MY51452776::0::INSTR")
InfiniiVision.timeout = 15000
InfiniiVision.clear()

# Initialize the oscilloscope, capture data, and analyze.
#initialize()
#capture()
analyze()
print("End of program.")
