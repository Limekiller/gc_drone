import sys
import serial
import time
import struct

# Path to the LEAP motion libraries
sys.path.insert(0, "/home/bryce/Leap_Motion/leap-motion/pkg/leap-motion-sdk/usr/lib")
import Leap


# Modify the default LEAP listener object so that we can verify when it is connected
class Listener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


# Create a listener object to receive data from the LEAP
listener = Listener()
controller = Leap.Controller()
controller.add_listener(listener)

# Connect to the Arduino through the correct serial port and wait for connection
port = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(2)

# If the LEAP detects no hands in the frame for over 5 seconds, the drone will land.
# We do this by comparing two time variables against each other, and a separate variable to tell if the timer is running or not.
# These are initalized here.
time_start = 0
hands_off_time = time.time()
timer_on = False

# Variables for determining which state the drone is in
# Start is used to determine if the drone is ready to fly or not,
# and flying tells us if the drone actually is in the air
flying = False
start = False

while True:

    # Grab a frame object from the LEAP, which contains all the data we need
    frame = controller.frame()

    # Sometimes we need a small delay in the Arduino program. We put a delay here that's larger than any delay in the Arduino program
    # so that serial commands don't build up on the Arduino side
    time.sleep(.05)

    # Bytes are sent to the Arduino 4 at a time: the first for left and right, the second for up and down,
    # the third for forward and back, and the last for any miscellaneous data we might want to send.

    # So here we are telling it to keep R/L and F/B steady, but set U/D at full velocity.
    # We are also sending a 15 in the 4th byte, which tells the drone that it is time to take off.
    if start and not flying:
        port.write(struct.pack('>B', 128))
        port.write(struct.pack('>B', 255))
        port.write(struct.pack('>B', 128))
        port.write(struct.pack('>B', 15))

        # When 15 is sent in the 4th byte, the Arduino calls a "takeoff" function on its side. This function
        # has a number of delays in it that total up to 600 ms, so we delay on this side as well.
        flying = True
        time.sleep(0.600)


    # If there are no hands in view,
    if len(frame.hands) == 0:

        # and the drone has already started, we start a timer for 5 seconds if there is not already such a timer running.
        if start:

            # If there are no hands in view, we just want the drone to hover in place,
            # so we set all axes to the middle voltage
            port.write(struct.pack('>B', 128))
            port.write(struct.pack('>B', 128))
            port.write(struct.pack('>B', 128))
            port.write(struct.pack('>B', 0))

            if not timer_on:
                hands_off_time = time.time()
                timer_on = True

            # If such a timer is running already, we check to see if it has surpassed 5 seconds, and if so,
            # "reset" the timer and the drone. This allows us to take off again once the drone lands
            else:
                if time.time() - hands_off_time > 5:
                    print "Ready!"
                    start = False
                    timer_on = False
                    flying = False

        print "Please move one hand into the frame to control the drone"

    # If there is one hand in view,
    elif len(frame.hands) == 1:

        # If we are not already flying but a hand is detected, set "Start" to true and just skip the rest of this loop.
        # Then we'll hit the block above where the takeoff command is sent.
        if not flying:
            start = True
            continue

        # Grab all the information for the hand and turn off any timers
        hands = frame.hands
        timer_on = False

       # print(int(max(0, min(hands[0].palm_position[0] + 128, 255))))
       # print(int(max(0, min(-(hands[0].palm_position[2] + 128) + 255, 255))))
       # print(int(max(0, min(hands[0].palm_position[1] - 100, 255))))

        # Take the data from the LEAP and convert it into a number between 0 and 255 for each axis based on position.
        # We then send this number straight to the Arduino, and the Arduino applies the number -- which corresponds
        # directly to the exact voltage we want. Efficient!
        # A more thorough explanation: we want the "centerpoint" for the LEAP to output a value of 128, not 0. So we add 128
        # to each number and clamp it between 0 and 255. For the second value, this ended up being backwards, so we took the
        # negative value and added 255 to it to reverse the numbers.
        # Also, for the third value (up and down), 0 is actually all the way down, rather than in the center, like the others.
        # So we just had to treat it differently (subtracting 100 to get the values we want instead of adding 128)
        port.write(struct.pack('>B',  int(max(0, min(hands[0].palm_position[0] + 128, 255)))))
        port.write(struct.pack('>B',  int(max(0, min(-(hands[0].palm_position[2] + 128) + 255, 255)))))
        port.write(struct.pack('>B',  int(max(0, min(hands[0].palm_position[1] - 100, 255)))))
        port.write(struct.pack('>B', 0))

    # If more hands are detected, just hover
    else:

        port.write(struct.pack('>B', 128))
        port.write(struct.pack('>B', 128))
        port.write(struct.pack('>B', 128))
        port.write(struct.pack('>B', 0))
        print "Please use only one hand at a time"



