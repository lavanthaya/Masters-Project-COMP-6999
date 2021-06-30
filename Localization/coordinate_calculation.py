from time_angle import Time_angle
from pulse_class import Pulse_classifier

print("hello world")

while True:
    IR_in = input("Sensor input: ")
    print("IR:", IR_in)

    #ta=Time_angle(5550,'h')
    #print(ta.V_hor[2]) 

    pc = Pulse_classifier(10)
    print(pc.pulse, pc.angle) 
    