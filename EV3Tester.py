#!/usr/bin/env pybricks-micropython

# Hagerty Robotics Program - EV3 Device Tester
# Version 1.0
# Last Update 4/13/2025

# This program is based off of the "How to use a PS3 Gamepad with Pybricks MicroPython on the EV3 brick"
# at www.antonsmindstorms.com.  The link is:
# https://www.antonsmindstorms.com/2019/06/16/how-to-use-a-ps3-gamepad-with-micropython-on-the-ev3-brick/

# This program uses input from the PS4 Controller to run various tests on EV3 Devices.
# First up is a motor tester.

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

# for listing filesystem directories
from os import (listdir)


# Used to display on the brick screen
ev3 = EV3Brick()

motor_dir = "/sys/class/tacho-motor"
sensor_dir = "/sys/class/lego-sensor"
type_file = "driver_name"
port_file = "address" #Sensor: ev3-ports:in4  Motor: ev3-ports:outC

class MotorType():
    MEDIUM = "lego-ev3-m-motor"
    LARGE = "lego-ev3-l-motor"

class SensorType():
    ULTRASONIC = "lego-ev3-us"
    GYRO = "lego-ev3-gyro"
    COLOR = "lego-ev3-color"
    TOUCH = "lego-ev3-touch"
    INFRARED = "lego-ev3-ir"

def make_port(port):
    if port=="A":
        return Port.A
    elif port=="B":
        return Port.B
    elif port=="C":
        return Port.C
    elif port=="D":
        return Port.D
    elif port=="1":
        return Port.S1
    elif port=="2":
        return Port.S2
    elif port=="3":
        return Port.S3
    elif port=="4":
        return Port.S4

# Returns a list of Tuples with (MotorType, Port, Motor)
def get_motors():
    motors = []
    dirs = listdir(motor_dir)
    for dir in dirs:
        f = open(motor_dir + "/" + dir + "/" +type_file)
        motor_type = f.readline().rstrip()
        f = open(motor_dir + "/" + dir + "/" +port_file)
        port = make_port(f.readline()[-2:-1])
        motors.append((motor_type,port, Motor(port)))
    return motors

# Returns a list of Tuples with (SensorType, Port, Sensor--Pybricks sensor object)
def get_sensors():
    sensors = []
    dirs = listdir(sensor_dir)
    for dir in dirs:
        f = open(sensor_dir + "/" + dir + "/" +type_file)
        motor_type = f.readline().rstrip()
        f = open(sensor_dir + "/" + dir + "/" +port_file)
        port = make_port(f.readline()[-2:-1])
        if motor_type == SensorType.COLOR:
            sensors.append((SensorType.COLOR,port, ColorSensor(port)))
        elif motor_type == SensorType.GYRO:
            sensors.append((SensorType.COLOR,port, GyroSensor(port)))
        elif motor_type == SensorType.INFRARED:
            sensors.append((SensorType.COLOR,port, InfraredSensor(port)))
        elif motor_type == SensorType.TOUCH:
            sensors.append((SensorType.COLOR,port, TouchSensor(port)))
        elif motor_type == SensorType.ULTRASONIC:
            sensors.append((SensorType.COLOR,port, UltrasonicSensor(port)))            
    return sensors

def motor_test( portLetter ):
    # Turn on motor for 5 seconds and see how far it goes and what its max RPM is
    # This should be a no-load test for a motor.  That is, have it completely
    # disconnected from everything.
    
    port = make_port( portLetter )
    motor = Motor(port)
    # Zero out the encoder
    motor.reset_angle(0)
    motor.dc(100)
    wait(1000)
    motor.stop()
    print("Distance in 1 second:" + str(motor.angle()) + " Expected 880 ")

    wait(1000)
    motor.reset_angle(0)
    motor.run_angle(720, 3600, wait=True)
    print("Run to Distance 3600 @ 2 Rotations/second.  Final Angle:" + str(motor.angle()) + "Expected 3600")
    wait(1000)
    





# Display the menu and get a response from the user
def handle_menu( in_file ):
    done = False
    selection = 0
    header = ( 5,  1,  "Port"), (95,  1,  "Port")
    menu = (( 10, 20, "1"   ), (100, 20, "A"   ),
            ( 10, 40, "2"   ), (100, 40, "B"   ),
            ( 10, 60, "3"   ), (100, 60, "C"   ),
            ( 10, 80, "4"   ), (100, 80, "D"   ) )
    #Number of selectable elements
    numel = len( menu )

    # Display the header elements
    for row in header:
        ev3.screen.draw_text( row[0], row[1], row[2] )

    # Display the menu elements
    for row in menu:
        ev3.screen.draw_text( row[0], row[1], row[2] )

    # Display the current selection marker
    ev3.screen.draw_text( menu[selection][0] - 9, menu[selection][1], "*")

    # Read from the file
    # long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'    
    EVENT_SIZE = struct.calcsize(FORMAT)
    event = in_file.read(EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

        # When the direction pad should be returning negative one, I am seeing a very large number
        # Just adjusting the value to what I need here
        if value > 2:
            value = -1

        #if ev_type != 0:
        #    outtext = str(ev_type) + ":" + str(code) + ":" + str(selection) + ":" + str(selection) + "     "
        #    ev3.screen.draw_text( 10,100, outtext, background_color=Color.WHITE)

        cur_selection = selection
        # Directional Pad Horizontal
        if ev_type == 3 and code == 16:
            selection = ( selection + value + numel ) % numel
        # Directional Pad Horizontal
        if ev_type == 3 and code == 17:
            selection = ( selection + value*2 + numel ) % numel

        # Option Button to select this entry
        if ev_type == 1 and code == 315 and value == 1:
            break

        if selection != cur_selection:
            # Clear the current selection marker
            ev3.screen.draw_text( menu[cur_selection][0] - 10, menu[cur_selection][1], "  ", background_color=Color.WHITE)
            # Display the current selection marker
            ev3.screen.draw_text( menu[selection][0] - 10, menu[selection][1], "*")
        
        # Finally, read another event
        event = in_file.read(EVENT_SIZE)

    return menu[selection][2]

# Find the PS3 Gamepad:
# /dev/input/event3 is the usual file handler for the gamepad.
# look at contents of /proc/bus/input/devices if it doesn't work.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# which port does the user want to test  
# port = handle_menu( in_file )

#mymotors = get_motors()
#print( mymotors )

motor_test("B")

in_file.close()

#ev3.screen.draw_text( 10,100,port)
wait(1000)

