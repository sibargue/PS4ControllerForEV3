#!/usr/bin/env pybricks-micropython

# Hagerty Robotics Program - EV3 Soccer Robot Program
# Version 1.0
# Last Update 2/21/2025

# This program is based off of the "How to use a PS3 Gamepad with Pybricks MicroPython on the EV3 brick"
# at www.antonsmindstorms.com.  The link is:
# https://www.antonsmindstorms.com/2019/06/16/how-to-use-a-ps3-gamepad-with-micropython-on-the-ev3-brick/

# This version adds the use of the left joystick to improve the ability to drive the robot in straight
# lines and do point turns.  The right joystick is still an Arcade mode controller that is fed directly
# to the motors with the minor change that a deadband prevents below threshold commands from slowly driving
# the robot in case the joystick centering is off.

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

# The left stick will only activate if one of the two axis are above this level
LEFT_STICK_THRESHOLD = 50

# The amount of adjustment when found to not be driving straight
DRIVE_STRAIGHT_ADJUSTMENT = 5

# Number of degrees of difference before drive straight adjustment is applied
DRIVE_STRAIGHT_THRESHOLD = 5

# Ignore right stick values below this level so the robot won't go driving off if the joystick reports
# very small levels while not being actively used (calibration error).  Also known as a deadband
RIGHT_STICK_THRESHOLD = 5

# Used to display on the brick screen
ev3 = EV3Brick()

# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize variables. 
# Assuming sticks are in the middle when starting.
right_stick_x = 124
right_stick_y = 124
left_stick_x = 124
left_stick_y = 124

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
drive_straight = False



while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 3:
        right_stick_x = value
    if ev_type == 3 and code == 4:
        right_stick_y = value
    if ev_type == 3 and code == 0:
        left_stick_x = value
    if ev_type == 3 and code == 1:
        left_stick_y = value

    # It is hard to drive directly forward or backward, so will use the left stick
    # to drive directly forward, or turn in place degrees
    # Scale stick positions to -1, 1
    fixed_forward = scale(left_stick_y, (0,255), (100,-100))
    fixed_left = scale(left_stick_x, (0,255), (100,-100))
    # Ignore small changes in the stick position.  You really have to want it
    if fixed_forward < LEFT_STICK_THRESHOLD and fixed_forward > -LEFT_STICK_THRESHOLD: 
        fixed_forward = 0
        drive_straight = False

    else:
        adjust_to_drive_straight = False
        if drive_straight == False:
            # Reset the encoder values because we are starting to drive straight
            drive_straight = True
            left_motor.reset_angle(0)
            right_motor.reset_angle(0)

        if drive_straight == True:
            #We were already driving straight, make adjustments to motors if we are off course
            if left_motor.angle() - right_motor.angle() > DRIVE_STRAIGHT_THRESHOLD:
                adjust_to_drive_straight = -DRIVE_STRAIGHT_ADJUSTMENT
            elif left_motor.angle() - right_motor.angle() < DRIVE_STRAIGHT_THRESHOLD:
                adjust_to_drive_straight = DRIVE_STRAIGHT_ADJUSTMENT
              
    # If the left joystick is far enough to the left or right, use it
    if fixed_left < LEFT_STICK_THRESHOLD and fixed_left > -LEFT_STICK_THRESHOLD:
        fixed_left = 0

    # Scale stick positions to -100,100
    forward = scale(right_stick_y, (0,255), (100,-100))
    left = scale(right_stick_x, (0,255), (100,-100))
    

    # The fixed values override the other stick
    if fixed_forward != 0:
        left_motor.dc(fixed_forward + adjust_to_drive_straight)
        right_motor.dc(fixed_forward - adjust_to_drive_straight)

    elif fixed_left != 0:
        left_motor.dc(-fixed_left)
        right_motor.dc(fixed_left)
    else:
        # Set motor voltages. If we're steering left, the left motor
        # must run backwards so it has a -left component
        # It has a forward component for going forward too. 
        if (forward > -RIGHT_STICK_THRESHOLD and forward < RIGHT_STICK_THRESHOLD and
            left    > -RIGHT_STICK_THRESHOLD and left    < RIGHT_STICK_THRESHOLD ) :
            forward = 0
            left = 0

        left_motor.dc(forward - left)
        right_motor.dc(forward + left)

     # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()