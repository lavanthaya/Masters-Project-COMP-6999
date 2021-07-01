#!/usr/bin/env python

from three_pi.ThreePi import ThreePi
from time import sleep

FORWARD_TIME = 2.0 #=>32 cm
TURN_TIME = 0.52

with ThreePi() as three_pi:

    for i in range(4):
        #1:forward | 0:stop | -1:reverse
        three_pi.send_speeds(1, 1)
        sleep(FORWARD_TIME)
        three_pi.send_speeds(0, 0)
        sleep(0.1)

        three_pi.send_speeds(0, 0.95)
        sleep(TURN_TIME)
        three_pi.send_speeds(0, 0)
        sleep(0.1)
