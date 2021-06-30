#-*- coding: utf-8 -*-
from time_angle import Time_angle
from pulse_class import Pulse_classifier
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# For GPIO numbering,
GPIO.setmode(GPIO.BCM)

# GPIO pin 23 connected to IR receiver
GPIO.setup(23, GPIO.IN, GPIO.PUD_DOWN)

p_rise = 0
offset_start = 0
U=[0.0, 0.0, 0.0]
base = [5.0, 0.0, 2.0]
current_pos = [0.0, 0.0, 0.0]

while True:
    ir_get = not GPIO.input(23)
        
    if (ir_get and (p_rise==0)):
            uptime = time.clock()
            p_rise = 1
            #print("UP")
        
    elif((not ir_get) and (p_rise == 1)):
            downtime = time.clock()
            delta_t = (downtime - uptime) * 1000000 #Convert to microseconds
            #print("Down")

            #time offset calculation
            pc = Pulse_classifier(delta_t)
            #print(pc.pulse, pc.angle)
            if pc.pulse =='s':
                offset_start = time.clock()

            elif ((pc.pulse == 'p') and (offset_start > 0)):
                offset_end = time.clock()
                offset_delta = ((offset_end - offset_start)* 1000000)- delta_t;  #substracting deltatime to remove pulse width
                offset_start=0

                #Do position calculation
                if ((offset_delta > 0) and (offset_delta <= (8333-104-delta_t))): #104 possible minimum sync pulse width
                    #Returns V_hor, V_ver in radiants (vector)
                    print("offset", offset_delta)
                    ta = Time_angle(offset_delta, pc.angle)

                    #Cross product of V_hor × V_ver
                    #U be perpendicular to both V_hor and V_ver[]
                    U[0] = ta.V_hor[1] * ta.V_ver[2] - ta.V_hor[2] * ta.V_ver[1]
                    U[1] = ta.V_hor[2] * ta.V_ver[0] - ta.V_hor[0] * ta.V_ver[2]
                    U[2] = ta.V_hor[0] * ta.V_ver[1] - ta.V_hor[1] * ta.V_ver[0]

                    #Do scaler multiplication and calculate current position
                    for x in range(3):
                        U[x] = U[x] * 1.5; #1.5 is a random value
                        current_pos[x] = base[x] + U[x]
                    
                    print("Current position")
                    print(current_pos[0], current_pos[1], current_pos[2])
                
                else:
                    print("Error offset value")

            p_rise = 0
                    