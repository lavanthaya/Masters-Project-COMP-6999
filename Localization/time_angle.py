# -*- coding: utf-8 -*-
# This function takes the time offset reading and calculate the
# Distance of sensor from origin

import math


PI = math.pi
Sin = math.sin
Cos = math.cos
Tan = math.tan

omega = PI/(8.33*10**-3) #rad/sec : laser drum angular velocity
height = 2.4 # lighthouse height in meters

class Time_angle:
    def __init__(self, offset_delta, oriantation):
        #offset_delta ==> in micro_sec
        sweep_angle = omega * (offset_delta * 10**-6) # units in rad
        angle_degree = math.degrees(sweep_angle)

        if angle_degree < 90:
            distance = height/Tan(sweep_angle) #pass angles in rad unit inside Tan

        elif angle_degree > 90:
            distance = height * Tan((PI/2) -sweep_angle) 

        else:
            distance = 0


        if (oriantation == 'h'):
            self.hor_pos = distance 
         
          

        elif (oriantation == 'v'):
            self.ver_pos = distance 
          
