#!/usr/bin/env pybricks-micropython

# This is a version of the robot control program that uses arcade control
# Right stick vertical axis controls forward and back
# Right stick horizontal axis controls the turning
# Square button reduces the effect of turns by 10% each press within limits
# Circle button increases the effect of turns by 10% each press within limits
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

def EV3SoccerArcade():

    # The deadband means ignore any settings below this.  Prevents the robot from moving unless the joystick
    # is really being toggled
    STICK_THRESHOLD = 10

    # The turn multiplier can be used to slow down turning.  The values are between 0.1 and 1.0
    # 1.0 means no throttling.  .10 means only 10% turning speed.
    turn_multiplier = 1.0

    # Used to display on the brick screen
    ev3 = EV3Brick()

    # Display who we are
    ev3.screen.draw_text(10,10,"PS4CtrlArcade")
    ev3.screen.draw_text(10,30,"07/05/25")
    ev3.screen.draw_text(10,50,"TurnCtl  O+  Squ-")

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
    right_stick_x = 124
    right_stick_y = 124

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
        # Horizontal stick value change
        if ev_type == 3 and code == 3:
            right_stick_x = value
        # Vertical stick value change
        if ev_type == 3 and code == 4:
            right_stick_y = value

        # Modify turn multiplier with the Square and Circle buttons
        if ev_type == 1 and code == 305:
            # Increase turning speed.  Make sure we only read the circle_button_press once per press
            circle_button_pressed = value
            if circle_button_pressed == 1 and last_circle_button == 0:
                # increase by .10 within limit
                turn_multiplier = min( (turn_multiplier + .10), 1.0 )
                last_circle_button = 1
            else:
                last_circle_button = 0

        if ev_type == 1 and code == 308:
            # Decrease turning speed.  Make sure to only read the button once per press.
            square_button_pressed = value
            if square_button_pressed == 1 and last_square_button == 0:
                # decrease by .10 within limit
                turn_multiplier = max( (turn_multiplier - .10), 0.1 )
                last_square_button = 1
            else:
                last_square_button = 0

        # Scale stick positions from 0-255 into -100,100
        # This can be used to reverse the forward direction by changing -100,100 to 100,-100
        forward = scale(right_stick_y, (0,255), (100,-100))
        left = scale(right_stick_x, (0,255), (-100,100))

        # If none of the stick directions is significant, don't move at all
        if (forward > -STICK_THRESHOLD and forward < STICK_THRESHOLD and
            left    > -STICK_THRESHOLD and left    < STICK_THRESHOLD ) :
            forward = 0
            left = 0

        # Set motor voltages. If we're steering left, the left motor
        # must run backwards so it has a -left component
        # It has a forward component for going forward too. 
        left_motor.dc(forward - left*turn_multiplier)
        right_motor.dc(forward + left*turn_multiplier)

        # Finally, read another event
        event = in_file.read(EVENT_SIZE)

    in_file.close()
    return

EV3SoccerArcade()