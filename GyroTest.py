#!/usr/bin/env pybricks-micropython

# Hagerty Robotics Program - EV3 GyroScope Testing
# Version 1.0
# Last Update 3/16/2025

# This program is intended to test the accuracy of the EV3 Gyroscop on the EV3 brick"

# This is a basic Riley Rover style robot.  I will add one Gyro sensor to the front center, and
# one to the back center.  Then, perform a series of tests.
# Test 1
#      Drive in a circle and beep after every 45 degree turn.  Drive the circle twice.
# Test 2
#      Drive in a very small square using the gyro to make the 90 degree turns.  Drive the square twice.

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

# Used to display on the brick screen
ev3 = EV3Brick()

# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
 
# Declare Gyros
front_gyro = GyroSensor(Port.S1)
back_gyro = GyroSensor(Port.S2)

# Find the PS3 Gamepad for control:
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

GYRO_CALIBRATION_LOOP_COUNT = 200
INT TESTSPEED = 50

int TEST_CIRCLE = 1
int TEST_SQUARE = 2
int curTest = TEST_CIRCLE

# Used in a 90 degree turn.  First tuple is the angle, 
# second tuple is how fast to go until you get to that angle
turn_90 = (4, [70, 50], [80, 50], [85, 30], [89, 10])

def right_turn_with_gyro( speed, l_motor, g_sensor )
    index = 1
    g_sensor.reset_angle(0)
    while True
        new_speed = speed[index][1]
        ev3.screen.draw_text(10,10,index)
        ev3.screen.draw_text(10,40,speed)
        l_motor.dc( speed )
        if  g_sensor(angle) > speed[index][0] 
           index += 1
        if index > speed[0]
            l_motor.stop() 
            break;

right_turn_with_gyro( turn_90, left_motor, front_gyro)

'''
left_motor.dc(TESTSPEED)
right_motor.dc(TESTSPEED * 0.80)
front_gyro.reset_angle(0)
back_gyro.reset_angle(0)
lastPos = 0
lastBeepPos = 0

sleep(1000)
while True
    gyro_sensor_value = front_gyro.angle()
    if ( gyro_sensor_value > 720 )
        left_motor.stop()
        right_motor.stop()
        break

    if gyro_sensor_value > lastBeepPos + 45
        lastBeepPos += 45
        ev3.speaker.beep(500,100)

front_gyro.reset_angle(0)
back_gyro.reset_angle(0)
sleep(1000)    
while True
    left_motor.dc(TESTSPEED)
    right_motor.dc(TESTSPEED)
    sleep(500)

    right_motor.stop()
    while ( front_gyro.angle < 90 )
    
rightTurnPID( speed, theLeftMotor  )
    left_motor

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
'''
