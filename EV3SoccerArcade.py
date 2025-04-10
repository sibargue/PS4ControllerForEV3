#!/usr/bin/env pybricks-micropython

# This is a version of the robot control program that uses arcade control
# Right stick vertical axis controls forward and back
# Right stick horizontal axis controls the turning

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

# The deadband means ignore any settings below this.  Prevents the robot from moving unless the joystick
# is really being toggled
STICK_THRESHOLD = 10

# The turn multiplier can be used to slow down turning.  The values are between 0.1 and 1.0
# 1.0 means no throttling.  .10 means only 10% turning speed.
turn_multiplier = 1.0

# Used to display on the brick screen
ev3 = EV3Brick()

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
last_forward = 0
last_left = 0

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


# Find the PS3 Gamepad:
# /dev/input/event3 is the usual file handler for the gamepad.
# look at contents of /proc/bus/input/devices if it doesn't work.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

ev3.screen.draw_text(10,10,"PS4CtrlArcade")
ev3.screen.draw_text(10,30,"04/10/25")
ev3.screen.draw_text(10,50,"Circle/Square-TurnCtl")

while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 3:
        right_stick_x = value
    if ev_type == 3 and code == 4:
        right_stick_y = value

    # Modify turn multiplier with the Square and Circle buttons
    if ev_type == 1 and code == 305:
        circle_button_pressed = value
        if circle_button_pressed == 1 and last_circle_button == 0:
            turn_multiplier = min( (turn_multiplier + .10), 1.0 )
            last_circle_button = 1
        else:
            last_circle_button = 0

    if ev_type == 1 and code == 308:
        square_button_pressed = value
        if square_button_pressed == 1 and last_square_button == 0:
            turn_multiplier = max( (turn_multiplier - .10), 0 )
            last_square_button = 1
        else:
            last_square_button = 0


    # Scale stick positions to -100,100
    # This can be used to reverse the forward direction by changing -100,100 to 100,-100
    forward = scale(right_stick_y, (0,255), (100,-100))
    left = scale(right_stick_x, (0,255), (-100,100))


    # Set motor voltages. If we're steering left, the left motor
    # must run backwards so it has a -left component
    # It has a forward component for going forward too. 
    if (forward > -STICK_THRESHOLD and forward < STICK_THRESHOLD and
        left    > -STICK_THRESHOLD and left    < STICK_THRESHOLD ) :
        forward = 0
        left = 0

    left_motor.dc(forward - left*turn_multiplier)
    right_motor.dc(forward + left*turn_multiplier)

    if last_circle_button == 1 or last_square_button == 1 or last_left != left or last_forward != forward:
        last_left = left
        last_forward = forward
        ev3.screen.clear()
        outtext = "F= " + str(int(forward)) + " L= " + str(int(left)) + " T= " + str(int(turn_multiplier*100))
        ev3.screen.draw_text(1,45,outtext)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()