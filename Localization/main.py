#-*- coding: utf-8 -*-
from time_angle import Time_angle
from pulse_class import Pulse_classifier
from ekf_model import EKF_model
import RPi.GPIO as GPIO
import time
from move_to_goal import MoveToPointController
from moverobot import MoveToPoint
import numpy as np


GPIO.setwarnings(False)
# For GPIO numbering,
GPIO.setmode(GPIO.BCM)

# GPIO pin 23 connected to IR receiver
GPIO.setup(23, GPIO.IN, GPIO.PUD_DOWN)

origin = [0,0] #x,y
sync = False
p_rise=0
p_end = 0
p_start =0
v_sweep_count = 0
h_sweep_count = 0
position_X = 0.0
position_Y = 0.0

f = open("offset.txt", "a")
while True:
    if (GPIO.input(23) and (p_rise==0)):
        p_start = time.clock()

        sweep_offset = (p_start - p_end) * 1000000
        p_rise = 1
    
    elif (not GPIO.input(23) and (p_rise == 1)):
        p_end = time.clock()
        p_len = (time.clock() - p_start)*1000000

        pulse_type = Pulse_classifier(p_len)
        p_rise = 0

        if pulse_type.pulse =='s':
            sync = True
            sweep_type = pulse_type.angle
        
        elif ((pulse_type.pulse == 'p') and (sync == True)):
            sync = False    
            sweep_offset = sweep_offset - p_len  #substracting pulse time to remove sweep pulse width (uSec)

            #Do position calculation
            if ((sweep_offset > 0) and (sweep_offset < (8333-104))): #104 possible minimum sync pulse width
                #Returns V_hor, V_ver in radiants (vector)
                ta = Time_angle(sweep_offset, sweep_type)

                if (sweep_type == 'h'):
                    position_X = ta.hor_pos
                    v_sweep_count +=1
                    #print('h:',sweep_offset)
                    h_t = sweep_offset

                elif (sweep_type == 'v'):
                    position_Y = ta.ver_pos
                    h_sweep_count +=1
                    #print('V:',sweep_offset)
                    v_t = sweep_offset
                
                sweep_ttl = 3
                if (v_sweep_count > 0 and h_sweep_count > 0 and v_sweep_count < sweep_ttl and h_sweep_count < sweep_ttl):
                    print(position_X, position_Y,)
                    #do the robot control code here
                
                    position = str(position_X)+","+str(position_Y)+","+str(h_t)+","+str(v_t)
                    f.write(position)
                    f.write("\n")
                    v_sweep_count = 0
                    h_sweep_count = 0


                elif(v_sweep_count >=sweep_ttl or h_sweep_count >=sweep_ttl):
                    v_sweep_count = 0
                    h_sweep_count = 0
            
            #else:
            #        print("offset noise",sweep_offset)
        
        

