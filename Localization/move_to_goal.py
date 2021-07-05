from three_pi.ThreePi import ThreePi
from math import sqrt, atan2, pi
from utils.angles import get_smallest_signed_angular_difference
from time import sleep

v_left = 0.0 
v_right = 0.0
class MoveToPointController():
    def __init__(self, goal_x, goal_y, current_x, current_y):
        with ThreePi() as three_pi:
            
            # Constants for controller
            self.K_RHO = 10
            self.K_ALPHA = 50

            # Distance between the robot's wheels
            self.BASELINE = 9

            # The arena's size is measured in pixels and is currently set to
            # 1280x720.  So the largest possible distance between two points (and
            # hence the largest possible rho value) is the following.
            self.ARENA_DIAGONAL = sqrt(1280**2 + 720**2)

            # Compute a normalizing factor which is based on the largest possible
            # value for either v_right or v_left.  v is in the range [0,
            # k_rho*ARENA_DIAGONAL] while w is in the range [-k_alpha*pi,
            # k_alpha*pi].  The largest value for either v_right or v_left occurs
            # when when v = k_rho*ARENA_DIAGONAL and w=-k_alpha*pi.
            self.normalizing_factor = (2.0*self.K_RHO*self.ARENA_DIAGONAL \
                                    + self.K_ALPHA*pi) / 2.0

        #def update(self, sensor_data):
            x = current_x   #sensor_data.pose.x
            y = current_y   #sensor_data.pose.y
            theta = 0   #sensor_data.pose.yaw
            #print((x, y, theta))

            # Compute the position of the goal in polar coordinates (rho, alpha)
            dx = goal_x - x
            dy = goal_y - y
            rho = sqrt(dx**2 + dy**2)
            alpha = get_smallest_signed_angular_difference(atan2(dy, dx), theta)

            # Apply constants to convert to forward and angular speed (v, w)
            v = self.K_RHO * rho
            w = self.K_ALPHA * alpha

            # Convert to right and left speeds and send to robot.
            v_right = (2.0*v - w*self.BASELINE) / 2.0
            v_left = w*self.BASELINE + v_right

            v_left /= self.normalizing_factor
            v_right /= self.normalizing_factor

            # If the computed (v_left, v_right) speeds are too small then there
            # won't be enough torque to overcome friction and drive the robot.
            # This is known as deadband.  We solve this problem here by
            # treating (v_left, v_right) as a vector and amplify it if its
            # length is too small.
            mag = sqrt(v_left**2 + v_right**2)
            DEAD_THRESHOLD = 0.6
            if mag < DEAD_THRESHOLD:
                factor = DEAD_THRESHOLD / mag
                v_left *= factor
                v_right *= factor

        
            print((v_left, v_right))
            three_pi.send_speeds(v_left, v_right)
            sleep(0.32)

#MoveToPointController(345, 365)