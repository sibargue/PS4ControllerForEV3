#!/usr/bin/env pybricks-micropython

# Author: Stefan Ibarguen

# This program is based off of the "How to use a PS3 Gamepad with Pybricks MicroPython on the EV3 brick"
# at www.antonsmindstorms.com.  The link is:
# https://www.antonsmindstorms.com/2019/06/16/how-to-use-a-ps3-gamepad-with-micropython-on-the-ev3-brick/

# This version of the Hagerty Robotics Soccer Robot program provides the following:
#
# Choose either tank or arcade controls using the triangle button
# Choose to moderate the turns in the arcade controls using the Circle and Squares buttons
# Code to automatically detect the name of the event file associated with the controller
# Code to detect a missing controller and display an appropriate error message on the robot
# Code to detect a missing motor (B and C are required) and display an appropriate error message
# Code to handle optional motors on ports A and D using the L1/L2 and R1/R2 buttons

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# from EV3SoccerUtil import scale, getInputFilename, getMotors
from EV3SoccerUtil import *

import struct

def handle_options_menu( values, in_file ):
    """
    Displays a menu on the EV3 screen that allows the user to
    optionally enable the A and/or D motors.  It modifies the
    values array with "Y" or "N" to indicate whether or not that
    motor has been enabled by the user.

    Example values ["N"]["N"] indicates that motors are not enabled
    by default.

    in_file - The file handle for the input from the PS4 controller (already open)

    Example: handle_options_menu( values, in_file )
             User selects both motors to be enabled
             return ["Y"]["Y"]
    """
    selection = 0
    done = False

    # Display the screen constants
    ev3.screen.clear()
    ev3.screen.draw_text( 5, 1, "Port" )
    ev3.screen.draw_text( 95,1, "Enabled" )
    ev3.screen.draw_text( 10,20,"A")
    ev3.screen.draw_text( 10,40,"D")

    # Display the default menu values
    ev3.screen.draw_text( 100, 20, values[0] )
    ev3.screen.draw_text( 100, 40, values[1] )
    
    # Display the current selection marker
    ev3.screen.draw_text( 85, 20, "*")

    # Display instructions
    ev3.screen.draw_text( 1, 80, "DirPad to select")
    ev3.screen.draw_text( 1, 100, "Option when done")

    # Read from the file (controller)
    # long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'    
    EVENT_SIZE = struct.calcsize(FORMAT)
    event = in_file.read(EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

        # For debugging purposes
        # if ev_type != 0:
        #     outtext = str(ev_type) + ":" + str(code) + ":" + str(value)
        #     print(outtext)
        #     print( str(selection) + " " + str( values) )

        # Directional Pad Vertical
        if ev_type == EVENT_RANGE and code == CODE_DPAD_VRANGE and value != VALUE_BUTTON_RELEASED:
            # Clear the current selection indicator
            ev3.screen.draw_text( 85, 20+selection*20, "  ", background_color=Color.WHITE)
            # Toggle the selection
            selection = ( selection + 1 ) % 2
            # Display the new selection indicator
            ev3.screen.draw_text( 85, 20+selection*20, "*", background_color=Color.WHITE )

        # Directional Pad Horizontal - toggle value
        if ev_type == EVENT_RANGE and code == CODE_DPAD_HRANGE and value != VALUE_BUTTON_RELEASED:
            # Toggle the value selected
            if values[selection] == "Y":
                values[selection] = "N"
            else:
                values[selection] = "Y"
            # Display the updated value
            ev3.screen.draw_text( 100, 20+20*selection, values[selection], background_color=Color.WHITE )

        # Option Button to exit menu
        if ev_type == EVENT_BUTTON and code == CODE_OPTION and value == VALUE_BUTTON_PRESSED:
            # All done.  Stick around until the option button is released
            done = True

        # Make sure to clear out the button up event from the queue
        if done and ev_type == EVENT_BUTTON and code == CODE_OPTION and value == VALUE_BUTTON_RELEASED:
            ev3.screen.clear()
            return values

        # Finally, read another event
        event = in_file.read(EVENT_SIZE)

    return 

def EV3Soccer( enableMotorA, enableMotorB, enableMotorC, enableMotorD):

    # Control type A = Arcade (Default), T=Tank
    ctrltype = "Arc"

    # The deadband means ignore any settings below this.  Prevents the robot from moving unless the joystick
    # is really being toggled
    STICK_THRESHOLD = 10

    # The turn multiplier can be used to slow down turning.  The values are between 10 and 100
    # 100 means no throttling.  10 means only 10% turning speed.
    turn_multiplier = 100

    # Display Controls and Status
    ev3.screen.clear()
    ev3.screen.draw_text(1,1,   "Circle/Square")
    ev3.screen.draw_text(1,21,  "  - Turn Change")
    ev3.screen.draw_text(1,41,  "Triangl - Arc/Tank")
    ev3.screen.draw_text(1,80,  "Option - +Motors", background_color=Color.WHITE)
    ev3.screen.draw_text(1,100, "Turn:" + str(turn_multiplier) + " " + ctrltype, background_color=Color.WHITE)

    wait(2000)

    # Find the gamepad event filename
    infile_path = getInputFilename()
    print ( infile_path )

    # Display an error if couldn't find the event handler filename (probably not connected)
    if ( infile_path == "" ) :
        ev3.screen.clear()
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
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

    # Check if the Option button was pressed.  This is the user's chance to enable the
    # optional A and/or D motors
    if ev_type == EVENT_BUTTON and code == CODE_OPTION and value == VALUE_BUTTON_PRESSED:
        values = ["N"] * 2
        if enableMotorA:
            values[0] = "Y"
        if enableMotorD:
            values[1] = "Y"
        handle_options_menu( values, in_file )
        if values[0] == "Y":
            enableMotorA = True
        else:
            enableMotorA = False

        if values[1] == "Y":
            enableMotorD = True
        else:
            enableMotorD = False

    # Make sure that motors B and C are connected
    foundMotorB = False
    foundMotorC = False
    foundMotorA = False
    foundMotorD = False
    motors = getMotors()
    print(motors)
    for item in motors:
        if ( item == "B") : foundMotorB = True
        if ( item == "C") : foundMotorC = True
        if ( item == "A") : foundMotorA = True
        if ( item == "D") : foundMotorD = True
   
    # Generate list of motors to display as status
    motorstatus = ""
    if ( foundMotorA ):
        motorstatus="A"
    if ( foundMotorB ):
        motorstatus += "B"
    if ( foundMotorC ):
        motorstatus += "C"
    if ( foundMotorD ):
        motorstatus += "D"

    if enableMotorB or enableMotorC:
        if ( foundMotorB == False or foundMotorC == False ):
            ev3.screen.draw_text(10,70,"ERR Motors B+C")
            ev3.screen.draw_text(10,90,"not connected")
            if ( foundMotorB == False):
                print( "ERROR: No motor found on Port B")
            if ( foundMotorC == False):
                print( "ERROR: No motor found on Port C")
            wait(5000)
            return

    # Check for Optional Motors
    if ( enableMotorA):
        if ( foundMotorA == False ):
            ev3.sceen.draw_text("MISSING MOTOR A")
            wait(2000)
            enableMotorA = False
        else:
            motorA = Motor(Port.A)

    if ( enableMotorD):
        if ( foundMotorD == False ):
            ev3.sceen.draw_text("MISSING MOTOR D")
            wait(2000)
            enableMotorD = False
        else:
            motorD = Motor(Port.D)

    # Declare required wheel motors
    if enableMotorB: 
        left_motor = Motor(Port.B)
    if enableMotorC:
        right_motor = Motor(Port.C)

    # Initialize variables. 
    # Assuming sticks are in the middle when starting.
    right_stick_x = 124
    right_stick_y = 124
    left_stick_y = 124

    # Process Optional Motors
    left_button_up_pressing = 0
    left_button_down_pressing = 0
    right_button_up_pressing = 0
    right_button_down_pressing = 0

    # Wait for an event to be reported in the event file
    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

        # Used to only update screen if circle/square/triangle pressed
        ctrlchange = False

        # Right Horizontal stick value change
        if ev_type == EVENT_RANGE and code == CODE_RSTICK_HRANGE:
            right_stick_x = value
        # Right Vertical stick value change
        if ev_type == EVENT_RANGE and code == CODE_RSTICK_VRANGE:
            right_stick_y = value
        # Left Vertical stick value change
        if ev_type == EVENT_RANGE and code == CODE_LSTICK_VRANGE:
            left_stick_y = value

        # Modify turn multiplier with the Square and Circle buttons
        if ev_type == EVENT_BUTTON and code == CODE_CIRCLE and value == VALUE_BUTTON_PRESSED:
            # Circle Button.  Increase turning speed.  Make sure we only read the circle_button_press once per press
            # increase by .10 within limit
            turn_multiplier = min( (turn_multiplier + 10), 100 )
            ctrlchange = True

        if ev_type == EVENT_BUTTON and code == CODE_SQUARE and value == VALUE_BUTTON_PRESSED:
            # Square Button.  Decrease turning speed.
            # decrease by .10 within limit
            ctrlchange = True
            turn_multiplier = max( (turn_multiplier - 10), 10 )

        if ev_type == EVENT_BUTTON and code == CODE_TRIANGLE and value == VALUE_BUTTON_PRESSED:
            # Triangle button. Toggle Arcade / Tank mode
            ctrlchange = True
            if ctrltype == "Arc":
                ctrltype = "Tank"
            else:
                ctrltype = "Arc"

        if ev_type != 0:
            outtext = str(ev_type) + ":" + str(code) + ":" + str(value)
            print(outtext)

        #Left 1 (up)
        if ev_type == EVENT_BUTTON and code == CODE_L1:  #Up
            left_button_up_pressing = value
            #print("L Up")
        #Left 2 (down)
        if ev_type == EVENT_BUTTON and code == CODE_L2:  #Down
            left_button_down_pressing = value
            #print("L Down")
        #Right 1 (up)
        if ev_type == EVENT_BUTTON and code == CODE_R1:  #Up
            #print("R Up")
            right_button_up_pressing = value
        #Right 2 (down)
        if ev_type == EVENT_BUTTON and code == CODE_R2:  #Up
            #print("R Down")
            right_button_down_pressing = value

        if ( enableMotorA):    
            if ( left_button_up_pressing == 1):
                motorA.dc(100)
            elif ( left_button_down_pressing == 1):
                motorA.dc(-100)
            else:
                motorA.dc(0)        
            
        if ( enableMotorD):    
            if ( right_button_up_pressing == 1):
                motorD.dc(100)
            elif ( right_button_down_pressing == 1):
                motorD.dc(-100)
            else:
                motorD.dc(0)        

        if ( ctrltype == "Arc"):
            # Arcade Controls

            # Scale stick positions from 0-255 into 100,-100
            # This can be used to reverse the forward direction by changing 100,-100 to -100,100
            forward = scale(right_stick_y, (0,255), (100,-100))
            left = scale(right_stick_x, (0,255), (100,-100))

            # If none of the stick directions is significant, don't move at all
            if (abs(forward) < STICK_THRESHOLD and abs(left) < STICK_THRESHOLD ) :
                forward = 0
                left = 0

            # Set motor voltages. If we're steering left, the left motor
            # must run backwards so it has a -left component
            # It has a forward component for going forward too. 
            if enableMotorB:
                left_motor.dc(forward - left*turn_multiplier/100)
            if enableMotorC:
                right_motor.dc(forward + left*turn_multiplier/100)
        else:
            # Tank controls

            # Scale stick positions to -100,100
            right_speed = scale(right_stick_y, (0,255), (100,-100))
            left_speed = scale(left_stick_y, (0,255), (100,-100))

            # Don't move if the joystick is really close to 0,0
            if abs(right_speed) < STICK_THRESHOLD and abs(left_speed) < STICK_THRESHOLD:
                right_speed = 0
                left_speed = 0 

            if enableMotorB:
                left_motor.dc(left_speed)
            if enableMotorC:
                right_motor.dc(right_speed)

        # Update the display if the control mode changed
        if ctrlchange:
            ev3.screen.draw_text(1,80, "Turn:" + str(turn_multiplier) + "% " + ctrltype + "    ", background_color=Color.WHITE)
            print("Turn:" + str(turn_multiplier) + " Control Type:" + ctrltype )
            
        # Finally, read another event
        event = in_file.read(EVENT_SIZE)

    in_file.close()
    return

# Used to display on the brick screen
ev3 = EV3Brick()

ev3.screen.draw_text(10,10,"Soccer")
ev3.screen.draw_text(10,30,"07/11/25")
wait(1000)

EV3Soccer(False, False, False, False)