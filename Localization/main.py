#-*- coding: utf-8 -*-
from time_angle import Time_angle
from pulse_class import Pulse_classifier
import RPi.GPIO as GPIO
import time
from move_to_goal import MoveToPointController

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
V_hor = [0.0, 0.0, 0.0]
V_ver = [0.0, 0.0, 0.0]
v_sweep_count = 0
h_sweep_count = 0

while True:
    ir_get = not GPIO.input(23)
        
    if (ir_get and (p_rise==0)):
            uptime = time.clock()
            p_rise = 1
        
    elif((not ir_get) and (p_rise == 1)):
            downtime = time.clock()
            delta_t = (downtime - uptime) * 1000000 #Convert to microseconds

            #time offset calculation
            print("delta_t", delta_t)
            pc = Pulse_classifier(delta_t)
            #print(pc.pulse, pc.angle)

            if pc.pulse =='s':
                offset_start = time.clock()
                sweep_type = pc.angle
                #print("iam sync")

            elif ((pc.pulse == 'p') and (offset_start > 0)):
                offset_end = time.clock()
                offset_delta = ((offset_end - offset_start)* 1000000)- delta_t;  #substracting deltatime to remove pulse width
                offset_start=0
                #print("iam pulse")

                offset_delta = offset_delta/1000.00
                #print("pulse offset", offset_delta)

                #Do position calculation
                if ((offset_delta > 0) and (offset_delta <= (8333))): #104 possible minimum sync pulse width
                    #Returns V_hor, V_ver in radiants (vector)
                    #print("offset", offset_delta, sweep_type)
                    ta = Time_angle(offset_delta, sweep_type)

                    if (sweep_type == 'h'):
                       V_hor = ta.V_hor
                       v_sweep_count +=1
                    elif (sweep_type == 'v'):
                       V_ver = ta.V_ver
                       h_sweep_count +=1
                    #print(v_sweep_count,h_sweep_count)
                    if (v_sweep_count < 5 and v_sweep_count > 0 and h_sweep_count < 5 and h_sweep_count > 0):
                       print(v_sweep_count,h_sweep_count, V_hor, V_ver)

                       v_sweep_count = 0
                       h_sweep_count = 0

                       #Cross product of V_hor × V_ver
                       #U be perpendicular to both V_hor and V_ver[]
                       U[0] = V_hor[1] * V_ver[2] - V_hor[2] * V_ver[1]
                       U[1] = V_hor[2] * V_ver[0] - V_hor[0] * V_ver[2]
                       U[2] = V_hor[0] * V_ver[1] - V_hor[1] * V_ver[0]

                       #Do scaler multiplication and calculate current position
                       for x in range(3):
                           U[x] = U[x] * 1.5; #1.5 is a random scaler parameter
                           current_pos[x] = base[x] + U[x]
                    
                       print("Current position")
                       print(current_pos[0], current_pos[1], current_pos[2])
                    
                       # MoveToPointController(home_x, home_y, current_x, current_y)
                       #MoveToPointController(base[0], base[2], current_pos[0], current_pos[2])
                
                else:
                    print(".......................",offset_delta)

            p_rise = 0