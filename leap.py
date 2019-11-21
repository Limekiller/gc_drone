import sys
import serial
import time
import struct

# Path to the LEAP motion libraries
sys.path.insert(0, "/home/bryce/Leap_Motion/leap-motion/pkg/leap-motion-sdk/usr/lib")
import Leap

# Object oriented programming my dude
class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"

# Create a listener object to receive data from the LEAP
listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)

# Connect to the Arduino through the correct serial port and wait for connection
port = serial.Serial("/dev/ttyUSB1", 9600)
time.sleep(2)

# If the LEAP detects no hands in the frame for over 5 seconds, the drone will land.
# We do this by comparing two time variables against each other, and a separate variable to tell if the timer is running or not.
# These are initalized here.
time_start = 0
hands_off_time = time.time()
timer_on = False

# Variables for determining which state the drone is in
flying = False
start = False

# Direction can equal left, right, forwards, back, hover, stopped, or takeoff
direction = "stopped"

velocity = 0

while True:

    # Create an array for all of the information we want to collect/display and continually grab data from the LEAP
    info_arr = []
    frame = controller.frame()

    # Sometimes we need a small delay in the Arduino program. We put a delay here that's larger than any delay in the Arduino program
    # so that serial commands don't build up on the Arduino side
    time.sleep(.05)

    # If the drone has been started,
    if start:
        # a takeoff command is received an the drone is not already flying,
        # Send the corresponding command to the Arduino side and wait 600 ms
        if direction == "takeOff" and not flying:
            port.write(struct.pack('>B', 101))
            flying = True
            time.sleep(0.600)
        # For each direction, send the appropriate command to the Arduino
        elif direction == "up":
            port.write(struct.pack('>B', int(str(velocity)+str(2))))
        elif direction == "down" or direction == "stopped":
            port.write(struct.pack('>B', int(str(velocity)+str(3))))
        elif direction == "right":
            port.write(struct.pack('>B', int(str(velocity)+str(4))))
        elif direction == "left":
            port.write(struct.pack('>B', int(str(velocity)+str(5))))
        elif direction == "forwards":
            port.write(struct.pack('>B', int(str(velocity)+str(6))))
        elif direction == "back":
            port.write(struct.pack('>B', int(str(velocity)+str(7))))
        elif direction == "hover":
            port.write(struct.pack('>B', 100))
        elif direction == "kill":
            port.write(struct.pack('>B', 108))

        print direction

    # If there are no hands in view,
    if len(frame.hands) == 0:

        # and the drone has already started, we start a timer for 5 seconds if there is not already such a timer running.
        if start:
            if not timer_on:
                hands_off_time = time.time()
                timer_on = True
            # If such a timer is running already, we check to see if it has surpassed 5 seconds, and if so,
            # "reset" the timer and the drone. This allows us to take off again once the drone lands
            else:
                if time.time() - hands_off_time > 5:
                    start = False
                    direction = "stopped"
                    timer_on = False
                    flying = False

        # If we aren't already stopped due to the timer, just set the drone to hover
        if start and direction != "stopped":
            direction = "hover"

        print "Please move one hand into the frame to control the drone"

    # If there is one hand in view,
    elif len(frame.hands) == 1:

        # Grab all the information for that hand and turn off any timers
        hands = frame.hands
        timer_on = False

        print hands[0].palm_position

        # Here, we determine the direction the drone should move in by the position of the hand.
        # Essentially, there is an invisible 3D cube safe zone, if the hand is within which the drone will hover.
        # On any side of this cube the drone will start to move in the same direction.

        # We also determine the velocity the drone should move at by the position as well.
        # Based on how far away from the center the hand is, the drone will move faster or slower.
        # How do we do this? First, add back the offset to the hand position
        # (The amount from 0 that is matched before the drone starts moving in a direction).
        # We integer-divide that by some number to reduce the scale (we want the drone to reach top speed well before the hand is as far
        # away from the center as it can go), and take the absolute value, as the number may be negative up to this point.
        # Finally, we clamp it between 10 and 20 (using a max and min function because Python doesn't have clamp).
        # We chose these numbers to guarantee that we always have two digits. The range is 0 - 10, but we didn't want to worry
        # about sometimes having one digit for our velocity and sometimes having two. This makes it easier to talk to the Arduino.

        # With the velocity and direction information, we can tell the Arduino exactly the information we need.
        # We send it an integer velocitydirection -- 152, for example. This would tell the Arduino that our velocity is 15 (5),
        # and our direction is 2 (up). The direction goes last because this number can only go up to 255. With this scheme,
        # The highest we can get is 207.
        if hands[0].palm_position[0] < -50:
            direction = 'left'
            velocity = max(0, min(abs(int((hands[0].palm_position[0] + 50) / 5)) + 10, 20))
        elif hands[0].palm_position[0] > 50:
            direction = 'right'
            velocity = max(0, min(abs(int((hands[0].palm_position[0] - 50) / 5)) + 10, 20))
        elif hands[0].palm_position[2] < -50:
            direction = 'forwards'
            velocity = max(0, min(abs(int((hands[0].palm_position[2] + 50) / 5)) + 10, 20))
        elif hands[0].palm_position[2] > 50:
            direction = 'back'
            velocity = max(0, min(abs(int((hands[0].palm_position[2] - 50) / 2)) + 10, 20))
        elif hands[0].palm_position[1] < 150:
            direction = 'down'
            velocity = max(0, min(abs(int((hands[0].palm_position[1] - 150) / 5)) + 10, 20))
        elif hands[0].palm_position[1] > 300:
            direction = 'up'
            velocity = max(0, min(abs(int((hands[0].palm_position[1] - 300) / 5)) + 10, 20))
        else:
            direction = 'hover'
            velocity = 10

        print velocity

        # If we are not already flying but a hand is detected, send a takeoff command and set the drone to started
        if not flying:
            start = True
            direction = "takeOff"

        # If the hand makes a fist, do something
        if hands[0].grab_strength == 1:
            direction = "kill"
            time.sleep(0.500);

    # If more hands are detected, just hover
    else:
        direction = "hover"
        print "Please use only one hand at a time"



