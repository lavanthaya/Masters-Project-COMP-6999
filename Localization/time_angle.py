# -*- coding: utf-8 -*-
# This function takes the time offset reading and convert it into 
# vertical or horzontal angles of emmited laser sweep.

import math


PI = math.pi
Sin = math.sin
Cos = math.cos

class Time_angle:
    def __init__(self, offset_delta, oriantation):
    #<time offset in µs> ; <central time offset = 4000> ; <cycle period = 8333>

        self.V_hor = [0.0, 0.0, 0.0]
        self.V_ver = [0.0, 0.0, 0.0]
        
        sweep_angle = (offset_delta - 4000) * PI / 8333

        if (oriantation == 'h'):
            self.V_hor = [0.0, Cos(sweep_angle), Sin(sweep_angle)]

        elif (oriantation == 'v'):
            self.V_ver = [Cos(sweep_angle), 0.0, -Sin(sweep_angle)]
