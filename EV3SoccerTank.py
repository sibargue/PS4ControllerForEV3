#!/usr/bin/env pybricks-micropython

# This is a version of the robot control program that uses tank control
# Right stick vertical axis controls right motor
# Left stick vertical axis controls the left motor
# See the readme.txt for important information
# Added error processing for missing motors and controller.  Added auto detection
# of the event filename so that it does not matter if a laptop has been connected
# via bluetooth.

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from EV3SoccerUtil import scale, getInputFilename, getMotors

import struct

def EV3SoccerTank():

    # The deadband means ignore any settings below this.  Prevents the robot from moving unless the joystick
    # is really being toggled
    STICK_THRESHOLD = 10

    # The turn threshold limits the delta between the left and right motors.  Setting this to 200
    # means no turn throttling.  Setting it to a small number like 10 would make all turns very slow.
    # The number must be an integer between 0 and 200
    turn_threshold = 200

    # Used to display on the brick screen
    ev3 = EV3Brick()

    # Display who we are
    ev3.screen.draw_text(10,10,"PS4CtrlTank")
    ev3.screen.draw_text(10,30,"07/05/25")

    # Make sure that motors B and C are connected
    foundMotorB = False
    foundMotorC = False
    motors = getMotors()
    for item in motors:
        if ( item == "B") : foundMotorB = True
        if ( item == "C") : foundMotorC = True

    if ( foundMotorB == False or foundMotorC == False ):
        ev3.screen.draw_text(10,70,"ERR Motors B+C")
        ev3.screen.draw_text(10,90,"not connected")
        if ( foundMotorB == False):
            print( "ERROR: No motor found on Port B")
        if ( foundMotorC == False):
            print( "ERROR: No motor found on Port C")
        wait(5000)
        return

    # Declare motors 
    left_motor = Motor(Port.B)
    right_motor = Motor(Port.C)

    # Initialize variables. 
    # Assuming sticks are in the middle when starting.
    right_stick_y = 124
    left_stick_y = 124

    # Assume circle and square buttons start off not pressed
    last_circle_button = 0
    last_square_button = 0

    # Find the gamepad event filename
    infile_path = getInputFilename()

    # Display an error if couldn't find the event handler filename (probably not connected)
    if ( infile_path == "" ) :
        ev3.screen.draw_text(10,70,"ERR Controller")
        ev3.screen.draw_text(10,90," ? connected ?")
        # prints go to the debug screen when connected to a laptop
        print("ERROR: Could not find Wireless Controller entry in the devices file")
        print("ERROR: Controller connected?")
        wait(5000)
        return

    # open file in binary mode
    in_file = open(infile_path, "rb")

    # Read from the file
    # long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'    
    EVENT_SIZE = struct.calcsize(FORMAT)
    event = in_file.read(EVENT_SIZE)

    # Wait for an event to be reported in the event file
    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
        if ev_type == 3 and code == 1:
            right_stick_y = value
        if ev_type == 3 and code == 4:
            left_stick_y = value

        # Scale stick positions to -100,100
        right_speed = scale(right_stick_y, (0,255), (100,-100))
        left_speed = scale(left_stick_y, (0,255), (100,-100))

        # Don't move if the joystick is really close to 0,0
        if abs(right_speed) < STICK_THRESHOLD and abs(left_speed) < STICK_THRESHOLD:
            right_speed = 0
            left_speed = 0 

        right_motor.dc(right_speed)
        left_motor.dc(left_speed)

        # Finally, read another event
        event = in_file.read(EVENT_SIZE)

    in_file.close()
    return

EV3SoccerTank()

