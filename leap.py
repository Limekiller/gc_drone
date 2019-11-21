import sys
sys.path.insert(0, "/home/bryce/Leap_Motion/leap-motion/pkg/leap-motion-sdk/usr/lib")
import Leap
import serial
import time
import struct

# Object oriented programming my dude
class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"

listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)

port = serial.Serial("/dev/ttyUSB0", 9600) # Connect to the Arduino through the correct serial port
time.sleep(2) # Wait for connection

# If the LEAP detects no hands in the frame for over 5 seconds, the drone will land.
# We do this by comparing two time variables against each other, and a separate variable to tell if the timer is running or not.
# These are initalized here.
time_start = 0
hands_off_time = time.time()
timer_on = False

# Variables for determining which state the drone is in
flying = False
start = False


direction = "stopped" # direction can equal up, down, left, right, hover
avg_y_list = [0 for i in range(5)]
avg_x_list = [0 for i in range(5)]
avg_z_list = [0 for i in range(5)]

velocity = 0

while True:

    # Create an array for all of the information we want to collect/display
    info_arr = []
    frame = controller.frame()

    time.sleep(.05)

    if start:
        if direction == "takeOff" and not flying:
            port.write(struct.pack('>B', 101))
            flying = True
            time.sleep(0.600)
        elif direction == "up":
            port.write(struct.pack('>B', int(str(velocity)+str(2))))
           # port.write(struct.pack('>B', 102))
        elif direction == "down" or direction == "stopped":
            port.write(struct.pack('>B', int(str(velocity)+str(3))))
           # port.write(struct.pack('>B', 103))
        elif direction == "right":
            port.write(struct.pack('>B', int(str(velocity)+str(4))))
           # port.write(struct.pack('>B', 104))
        elif direction == "left":
            port.write(struct.pack('>B', int(str(velocity)+str(5))))
           # port.write(struct.pack('>B', 105))
        elif direction == "forwards":
            port.write(struct.pack('>B', int(str(velocity)+str(6))))
           # port.write(struct.pack('>B', 106))
        elif direction == "back":
            port.write(struct.pack('>B', int(str(velocity)+str(7))))
           # port.write(struct.pack('>B', 107))
        elif direction == "hover":
            port.write(struct.pack('>B', 100))

        print direction

    # Collect information if there is a hand in view
    if len(frame.hands) == 0:

        if start:
            if not timer_on:
                hands_off_time = time.time()
                timer_on = True
            else:
                if time.time() - hands_off_time > 5:
                    start = False
                    direction = "stopped"
                    timer_on = False
                    flying = False

        if start and direction != "stopped":
            direction = "hover"
        print "Please move one hand into the frame to control the drone"

    elif len(frame.hands) == 1:

        hands = frame.hands
        timer_on = False
        print hands[0].palm_position

        #if -50 < hands[0].palm_position[0] < 50 and 100 < hands[0].palm_position[1] < 200 and -50 < hands[0].palm_position[2] < 50:
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

        # Determine which way palm is facing
        hand_dir = hands[0].palm_normal.roll
        if -0.75 < hand_dir < 0.75:
            info_arr.append(0)
        elif -0.75 > hand_dir > -2.5:
            info_arr.append(-1)
        elif 0.75 < hand_dir < 3:
            info_arr.append(1)
        else:
            info_arr.append(2)

       # # Detect left and right motion
       # if avg_x_list.count(avg_x_list[0]) == 5:
       #     if info_arr[1] == 1:
       #         direction = 'right'
       #         flying = True
       #     elif info_arr[1] == -1:
       #         direction = 'left'
       #         flying = True

       # # Detect back and forth motion
       # if avg_z_list.count(avg_z_list[0]) == 5:
       #     if info_arr[2] == 1:
       #         direction = 'forward'
       #         flying = True
       #     elif info_arr[2] == -1:
       #         direction = 'back'
       #         flying = True

       # # Detect up and down motion
       # if avg_y_list.count(avg_y_list[0]) == 5:
       #     if info_arr[0] == 1 and info_arr[3] == 2:
       #         direction = 'up'
       #         flying = True
       #     elif info_arr[0] == -1:
       #         direction = 'down'
       #         flying = True

       # if info_arr[3] == 2:
       #     direction = "hover"

        if not flying:
            start = True
            direction = "takeOff"

        if hands[0].grab_strength == 1:
            direction = "flip"
            time.sleep(0.400)

    else:
        direction = "hover"
        print "Please use only one hand at a time"



