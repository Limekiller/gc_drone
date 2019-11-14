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

    def on_frame(self, controller):

        # Create an array for all of the information we want to collect/display
        info_arr = []
        frame = controller.frame()

        # Collect information if there is a hand in view
        if len(frame.hands) == 0:
            print "Please move one hand into the frame to control the drone"
        elif len(frame.hands) == 1:
            info_arr.append("Propeller on")
            hands = frame.hands

            # Determine direction on Y axis
            if hands[0].palm_velocity[1] > 50:
                info_arr.append(1)
            elif hands[0].palm_velocity[1] < -50:
                info_arr.append(-1)
            else:
                info_arr.append(0)

            # Determine direction on X axis
            if hands[0].palm_velocity[0] > 50:
                info_arr.append(1)
            elif hands[0].palm_velocity[0] < -50:
                info_arr.append(-1)
            else:
                info_arr.append(0)

            # Determine direction on Z axis
            if hands[0].palm_velocity[2] > 50:
                info_arr.append("ZDirection: Back")
            elif hands[0].palm_velocity[2] < -50:
                info_arr.append("ZDirection: Forwards")
            else:
                info_arr.append("ZDirection: None")

            # Determine which way palm is facing
            hand_dir = hands[0].palm_normal.roll
            if -0.75 < hand_dir < 1:
                info_arr.append("Facing: Down")
            elif -0.75 > hand_dir > -2.5:
                info_arr.append("Facing: Left")
            elif 1 < hand_dir < 3:
                info_arr.append("Facing: Right")
            else:
                info_arr.append("Facing: Up")

            print info_arr
            if info_arr[1] == 0 and info_arr[2] == 0:
               port.write(struct.pack('>B', 0))
            elif abs(info_arr[1]) == 1 and info_arr[2] == 0:
               port.write(struct.pack('>B', 1))
            elif info_arr[1] == 0 and abs(info_arr[2]) == 1:
               port.write(struct.pack('>B', 2))
            elif abs(info_arr[1]) == 1 and abs(info_arr[2]) == 1:
               port.write(struct.pack('>B', 3))
        else:
            print "Please use only one hand at a time"

listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)

port = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(2)

while True:
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        exit()
