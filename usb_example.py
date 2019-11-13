# This program is a companion to the usb_example.ino script.
# It will send a 0 and then a 1 to the Arduino to control an LED.
# The trick is to send bytes (using struct here) rather than strings or anything more complicated.
# Run the Arduino program and then this Python script to see it work.

import serial, time, struct

port = serial.Serial('COM3', 9600)

while True:
    time.sleep(2)
    port.write(struct.pack('>B', 0))
    time.sleep(2)
    port.write(struct.pack('>B', 1))
