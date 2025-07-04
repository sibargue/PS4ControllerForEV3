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

