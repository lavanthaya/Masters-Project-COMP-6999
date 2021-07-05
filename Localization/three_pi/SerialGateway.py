#!/usr/bin/env python
#below code was written for python 2
"""
Handles serial communication with the 3pi robot.
"""
import serial
import time

class SerialGateway(object):

    def __init__(self, port="/dev/ttyACM1", baudrate=115200):
        self._port = port
        self._baudrate = baudrate

        self.buffer = []

    def start(self):
        self._serial = serial.Serial(port = self._port, \
                                     baudrate = self._baudrate, \
                                     timeout = None)
            
    def stop(self):
        time.sleep(.1)
        self._serial.close()

    def clear_buffer(self):
        self.buffer = []

    def get_buffer(self):
        #print("BUFFER: --->{}<---".format(self.buffer))
        return self.buffer

    def wait_for_buffer_fill(self, n):
        """Keep testing until the buffer containts n entries, then return."""
        while len(self.buffer) < n:
            self.buffer.append( self._serial.read() )

    def write(self, data):
        #print("WRITING: " + data)
        self._serial.write(data)
