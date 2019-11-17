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

# port = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(2)
time_start = 0
flying = False
start = False

hands_off_time = time.time()
timer_on = False

direction = "stopped" # direction can equal up, down, left, right, hover
avg_y_list = [0 for i in range(5)]
avg_x_list = [0 for i in range(5)]
avg_z_list = [0 for i in range(5)]

while True:

    # Create an array for all of the information we want to collect/display
    info_arr = []
    frame = controller.frame()

    time.sleep(.05)

    print direction
    if start:
        if direction == "takeOff" and not flying:
            # port.write(struct.pack('>B', 1))
            flying = True
            time.sleep(0.600)
        #elif direction == "up":
        #    # port.write(struct.pack('>B', 2))
        #elif direction == "down":
        #    # port.write(struct.pack('>B', 3))
        #elif direction == "right":
        #    # port.write(struct.pack('>B', 4))
        #elif direction == "left":
        #    # port.write(struct.pack('>B', 5))
        #elif direction == "hover":
        #    # port.write(struct.pack('>B', 0))

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

        # Determine direction on Y axis
        avg_y_list.pop(0)
        if hands[0].palm_velocity[1] > 50:
            info_arr.append(1)
            avg_y_list.append(1)
        elif hands[0].palm_velocity[1] < -50:
            info_arr.append(-1)
            avg_y_list.append(-1)
        else:
            info_arr.append(0)
            avg_y_list.append(0)

        # Determine direction on X axis
        avg_x_list.pop(0)
        if hands[0].palm_velocity[0] > 50:
            info_arr.append(1)
            avg_x_list.append(1)
        elif hands[0].palm_velocity[0] < -50:
            info_arr.append(-1)
            avg_x_list.append(-1)
        else:
            info_arr.append(0)
            avg_x_list.append(0)

        # Determine direction on Z axis
        avg_z_list.pop(0)
        if hands[0].palm_velocity[2] > 50:
            info_arr.append(-1)
            avg_z_list.append(-1)
        elif hands[0].palm_velocity[2] < -50:
            info_arr.append(1)
            avg_z_list.append(1)
        else:
            info_arr.append(0)
            avg_z_list.append(0)

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

        print info_arr
        print avg_x_list

        # Detect left and right motion
        if avg_x_list.count(avg_x_list[0]) == 5:
            if info_arr[1] == 1:
                direction = 'right'
                flying = True
            elif info_arr[1] == -1:
                direction = 'left'
                flying = True

        # Detect back and forth motion
        if avg_z_list.count(avg_z_list[0]) == 5:
            if info_arr[2] == 1:
                direction = 'forward'
                flying = True
            elif info_arr[2] == -1:
                direction = 'back'
                flying = True

        # Detect up and down motion
        if avg_y_list.count(avg_y_list[0]) == 5:
            if info_arr[0] == 1:
                direction = 'up'
                flying = True
            elif info_arr[0] == -1:
                direction = 'down'
                flying = True

        if info_arr[3] == 2:
            direction = "hover"

        if not flying:
            start = True
            direction = "takeOff"

        if hands[0].grab_strength == 1:
            direction = "stopped"

    else:
        direction = "hover"
        print "Please use only one hand at a time"



