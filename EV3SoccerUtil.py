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

    # Returns a list of motors that are connected
    
def getMotors():
    motor_dir = "/sys/class/tacho-motor"
    port_file = "address" #Sensor: ev3-ports:in4  Motor: ev3-ports:outC

    motors = []
    dirs = listdir(motor_dir)
    for dir in dirs:
        f = open(motor_dir + "/" + dir + "/" +port_file)
        port = f.readline()[-2:-1]
        motors.append(port)
    return motors
