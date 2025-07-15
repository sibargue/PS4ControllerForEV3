Note that there is no main.py in here.  There are several programs that can be run and worked on.
In order to run a program from VSCode, open the Run Menu and choose Open Configurations.  Then,
change the name of the program to the one that you are working on.  For example:

"program": "/home/robot/${workspaceRootFolderName}/EV3SoccerArcade.py",

main.py has been removed.  When working on this code, you should work on the actual python
file you are interested in.  Note that all of the programs are available to be run
on the brick by browsing the filesystem and choosing one of the .py files.

The putty app is useful to to open a terminal to browse the ev3 file system.
The username is robot, and the password is maker.

Ps4ControllerforEV3
These are a programs that allows a PS4 controller to be used to control an EV3
over a bluetooth connection.
Requirements:
EV3 is running 
EV3 Robot.  For this example I assume a Riley Rover style robot with two back wheels and one front ball 
bearing swivel wheel.  Left Motor is on Port B, and Right Motor is on port C
A PS4 controller (but a PS3 controller should work as well)
A 16-32GB Micro SD card
USB A to USB Mini data cable to connect EV3 to Laptop or a bluetooth connection.  The bluetooth connection
process is quite picky, but once you get the hang of it, very convenient.  Search the Hagerty Robotics
Google drive for "EV3" and you will find a file called "How to Setup an EV3 Robot to be controlled by a PS4 controller"
for a description on how to set up the bluetooth connection from the EV3 to the laptop.
Laptop with Windows 11, but a Mac will work as well
Balena Etcher program downloaded onto Laptop
Microsoft VS Code development environment on Laptop
For troubleshooting, it also helps to have the "putty" remote terminal app.  When logging in, connect to the ev3dev
device and use "robot" as the username and "maker" as the password.

Useful Links
https://www.antonsmindstorms.com/2020/02/14/how-to-connect-a-ps4-dualshock-4-controller-to-your-mindstorms-ev3-brick-with-bluetooth/#more-2357 
https://www.antonsmindstorms.com/2019/06/15/how-to-run-python-on-an-ev3-brick/
Python for the EV3 Brick…
    https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3/
Now you need to get the sample code to start from.  The PS3 controller seems to work pretty much the same as the PS4 controller so far.  Sample code can be found here.
    https://www.antonsmindstorms.com/2019/06/16/how-to-use-a-ps3-gamepad-with-micropython-on-the-ev3-brick/ 

Controller Research
     The numbers shown below are the Event Type, Event Code, and Event Value for each event.
        1:310:2 means Event Type 1, Event Code 310, and Value 2
        
     L1 Button -    This is binary.  Either gets the event when the button is pressed, or the event when the
                    button is released
        1:310:1     Button is pressed.  Once per button press
        1:310:0     Button is released.

     L2 Button -
        1:312:1     Button is pressed.  Once per button press
        3:2:2       The value of the button from 1 to 255  Another event comes in every time the button is pressed
        3:2:13      a little more or less.  If you manage to keep it exactly the same, no new event comes in.
        ...
        1:312:0     Button is released
        3:2:0       This event comeS in consistently after the button was released
    
    R1 Button -     Different values, but same behavior as L1
        1:311:1
        1:311:0

    R2 Button -     Different values, but same behavior as L2
        1:313:1
        3:5:214
        3:5:255
        3:5:124
        1:313:0
        3:5:0

    Left Joystick - Vertical Action:Push Up then release
        3:1:123 - Joystick starts more or less centered at 127 
        3:1:104 - Gets smaller
        3:1:74  - and smaller...
        3:1:28
        3:1:0   - Until reaches zero
        3:1:4   - And then increases as the stick is released
        3:1:33  - and makes its way back to the center position
        3:1:102 - Going down it increases up to 255 and repeats the
        3:1:128 - retreat back to 128 (not shown here)

    Left Joystick - Horizontal
        3:0:0   - Positioned all the way to the left
        3:0:128 - When it returns to the center position
        3:0:255 - Positioned all the way to the right.  If you hold it here, no more events happen

    Right Joystick - Vertical
        3:4:0   - Positioned all the way to the top
        3:4:128 - When it returns to the center position
        3:4:255 - Positioned all the way to the bottom

    Right Joystick - Horizontal
        3:3:0   - Positioned all the way to the left
        3:3:128 - When it returns to the center position
        3:3:255 - Positioned all the way to the right.  If you hold it here, no more events happen

    Squares Button 
        1:308:1 Button Pressed
        1:308:0 Button Released

    Triangle Button 
        1:307:1 Button Pressed
        1:307:0 Button Released

    Circle Button 
        1:305:1 Button Pressed
        1:305:0 Button Released
    
    Diamonds Button 
        1:304:1 Button Pressed
        1:304:0 Button Released

    Direction Pad - Press then Release each button
        Up - 3:17:4294967295 / 3:17:0
        Left - 3:16:1 / 3:16:0
        Down - 3:17:1 / 3:17:0
        Right - 3:16:42949667295 / 3:16:0

    Combinations
    Actions: Left Stick Vertical Up, R2 Down, R2 released, Left Stick Released
        3:1:118 Left Stick Vertical
        3:1:88
        3:1:45
        3:1:0   Left Stick Vertical reaches top
        3:0:133 Left Stick Horizontal close to center
        3:0:137 "
        3:0:138 "
        1:313:1 R2 Pressed
        3:5:164 R2 Value
        3:5:255 R2 Value
        3:0:139 Left Stick Horizontal close to center
        3:0:142 "
        3:0:143 "
        3:0:144 "
        3:1:1   Left Stick Vertical still near top
        3:0:145 Left Stick Horizontal close to center
        3:0:146 Left Stick Horizontal close to center
        1:313:0 R2 Released
        3:5:0   R2 Trailing 0 value after release
        3:0:145 
        3:0:146
        3:0:143
        3:1:0
        3:0:141
        3:1:42
        3:0:128 Left Stick Horizontal returning to center
        3:1:128 Left Stick Vertical returning to center


 Checklist
     SD card is in brick and it boots the BrickMan OS (EV3DEV)
     The EV3 has been connected to the PS4 controller.  On brick: Wireless and Networks, Bluetooth,
     the Powered and Visible options should be on (filled square)
     Connect to the PS4 controller - On brick, select Start Scan.  On PS4 press AND HOLD the share and PS buttons
     at the same time.  Wait until the front light on the PS4 starts flashing white RAPIDLY.  Not the slow pulsing.
     If the light on the controller gets to the slow pulsing light, you need to power off the controller (hold down the
     home key until it turns off) and try again.
     The device list on the brick will expand, so scroll down to see "Wireless Controller"
     Pair if it isn't already paired
     Connect if it is already paired.
     When you see "Disconnect", that means it is connected.
     Run the program on the brick by backing up (upper left button) until you see a menu with File Browser.
     Browse down to PS4ControllerforEV3 folder and then select the main.py file (this will run the program)
     The green lights will flash, and the program is running.  If it pops back to the menu right away, you probably
     don't have it connected to the controller.
     Pressing upper left button will stop the program.

     Testing the programs to make sure they work, and that the error handling tells the user what they
     need to know to fix the problem.

       - Run with motor disconnected
       - Run with no controller paired
       - Run with controller paired but not connected
       - Run with controller paired and connected and no laptop in devices list
       - Run with controller paired and connected and laptop connected
       - Run with multiple controllers paired and one connected

