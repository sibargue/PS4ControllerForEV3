#!/usr/bin/env pybricks-micropython

# This is a version of the robot control program that uses tank control
# Left stick vertical axis controls the left wheel
# Right stick vertical axis controls the right wheel

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

# The turn threshold limits the delta between the left and right motors.  Setting this to 200
# means no turn throttling.  Setting it to a small number like 10 would make all turns very slow.
# The number must be an integer between 0 and 200
turn_threshold = 200

# Used to display on the brick screen
ev3 = EV3Brick()

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
last_left = 0
last_right = 0

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

ev3.screen.draw_text(10,10,"PS4CtrlTank")
ev3.screen.draw_text(10,30,"04/09/25")

while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 1:
        right_stick_y = value
    if ev_type == 3 and code == 4:
        left_stick_y = value

    # Modify turn threshold with the Square and Circle buttons
    if ev_type == 1 and code == 305:
        circle_button_pressed = value
        if circle_button_pressed == 1 and last_circle_button == 0:
            turn_threshold = min( (turn_threshold + 10), 200 )
            last_circle_button = 1
        else:
            last_circle_button = 0

    if ev_type == 1 and code == 308:
        square_button_pressed = value
        if square_button_pressed == 1 and last_square_button == 0:
            turn_threshold = max( (turn_threshold - 10), 0 )
            last_square_button = 1
        else:
            last_square_button = 0


    # Scale stick positions to -100,100
    right_speed = scale(right_stick_y, (0,255), (100,-100))
    left_speed = scale(left_stick_y, (0,255), (100,-100))

    # Don't move if the joystick is really close to 0,0
    if abs(right_speed) < STICK_THRESHOLD and abs(left_speed) < STICK_THRESHOLD:
        right_speed = 0
        left_speed = 0 
    right_motor.dc(right_speed)
    left_motor.dc(left_speed)

    # These robots spin really fast and become uncontrollable.  So, if the delta between the
    # left and right motors is over the threshold, bring the turn down to the threshold
    if abs(right_speed - left_speed) > turn_threshold:
        #find out which speed is faster, and slow it down to meet the threshold
        if abs(right_speed) > abs(left_speed):
            # Need to bring right_speed closer to left_speed
            if right_speed > left_speed:
                right_speed = left_speed + turn_threshold
            else:
                right_speed = left_speed - turn_threshold
        else:
            # Need to bring left_speed closer to right_speed
            if left_speed > right_speed:
                left_speed = right_speed + turn_threshold
            else:
                left_speed = right_speed - turn_threshold

    #Done with filtering, now set the motor speeds
    right_motor.dc(right_speed)
    left_motor.dc(left_speed)

    if last_circle_button == 1 or last_square_button == 1 or last_left != left_speed or last_right != right_speed:
        last_left = left_speed
        last_right = right_speed
        ev3.screen.clear()
        outtext = "R= " + str(int(right_speed)) + " L= " + str(int(left_speed)) + " T= " + str(turn_threshold)
        ev3.screen.draw_text(10,45,outtext)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()