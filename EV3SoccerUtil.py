# Utility functions for the EV3Soccer group of programs

from os import (listdir)

# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def getInputFilename():
    """
    Parses the devices file to find the name of the event file that represents the controller
    and returns the full path to the event file.

    Returns the null string if the controller is not found

    example: print(getInputFilename())
    """
    # Find the PS3 Gamepad:
    # Robust finding the Gamepad:
    # The /proc/bus/input/devices file contains a descriptive listing of the devices
    # that are attached to this device (EV3 Brain).  We are only interested in the one
    # that has entries that look like this (among others)
    #
    # N: Name="Wireless Controller"
    # H: Handlers=event???

    # So, open the file, read it line by line looking for the first entry.  Then continue
    # looking for the second entry and grab the "eventX" portion of it to figure out what
    # the correct name is.

    # The event file is in the /dev/input folder

    eventfilename=""
    foundeventfile=False
    # Open the device file
    with open("/proc/bus/input/devices") as file:
        # iterate through the file line by line
        for line in file:
            # Search for the Wireless Controller entry
            if ( line.startswith("N: Name=\"Wireless Controller\"") ):
                foundeventfile = True
            # Only searching for the handler name once the Wireless Controller entry has been found
            if ( foundeventfile ):
                # Search for the Handler name line
                if line.startswith("H: Handlers=event") :
                    # Found the event handler name.  Create the full pathname of the event file
                    eventfilename="/dev/input/" + line[12:].rstrip()
                    # and return it.  Note the file handle is automatically closed upon exit from the loop
                    return(eventfilename)
    # Didn't find the Wireless Controller.  Return the null string                
    return("")

    
def getMotors():
    """
    Finds all the tacho-motors that the system has found and return a list of motor ports.
    For example, it would return [B][C] if there is a motor on ports B and C.

    Returns an empty list if no motors are found.

    example: print getMotors()
    """

    motor_dir = "/sys/class/tacho-motor"
    port_file = "address" #Sensor: ev3-ports:in4  Motor: ev3-ports:outC

    motors = []
    # Get the list of directories
    dirs = listdir(motor_dir)
    for dir in dirs:
        # Open the /sys/class/tacho-motor/XXX/+portfile in each directory
        f = open(motor_dir + "/" + dir + "/" +port_file)
        # Find the motor referenced in the last character of the line in the file
        port = f.readline()[-2:-1]
        # Append it to the list of motors
        motors.append(port)
    # Return the list of motors
    return motors

#PS4 Controller Constants
EVENT_BUTTON = 1
EVENT_RANGE  = 3
#Controls that return a range of values
CODE_LSTICK_HRANGE = 0
CODE_LSTICK_VRANGE = 1
CODE_L2_RANGE =      2
CODE_RSTICK_HRANGE = 3
CODE_RSTICK_VRANGE = 4
CODE_R2_RANGE =      5
# On / Off buttons
CODE_DIAMOND =  304
CODE_CIRCLE =   305
CODE_TRIANGLE = 307
CODE_SQUARE =   308
CODE_L1 =       310
CODE_R1 =       311
CODE_L2 =       312
CODE_R2 =       313
CODE_SHARE =    314
CODE_OPTION =   315
CODE_HOME =     316
CODE_DPAD_HRANGE = 16
CODE_DPAD_VRANGE = 17
# Values returned by buttons
VALUE_DPAD_UP = 4294967295
VALUE_DPAD_DOWN = 0
VALUE_DPAD_RIGHT = 4294967295
VALUE_DPAD_LEFT = 0
VALUE_BUTTON_PRESSED  = 1
VALUE_BUTTON_RELEASED = 0