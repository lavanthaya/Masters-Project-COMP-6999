"""
Definitions and utilities for interfacing with the 3pi robot.  Note that functions defined here recall a SerialGateway to be passed in.
"""

from SerialGateway import SerialGateway

# The following is a subset of the commands available on the 3pi running
# Pololu's serial slave program: https://www.pololu.com/docs/0J21/10.a
RAW_SENSORS_CMD = "\x86"
CALIBRATED_SENSORS_CMD = "\x87"
TRIMPOT_CMD = "\xB0"
BATTERY_CMD = "\xB1"
PLAY_MUSIC_CMD ="\xB3"
CALIBRATE_CMD ="\xB4"
RESET_CALIBRATION_CMD ="\xB5"
LINE_POSITION_CMD ="\xB6"
AUTOCALIBRATE_CMD = "\xBA"
START_PID_CMD = "\xBB"
STOP_PID_CMD = "\xBC"
MOTOR_LEFT_FORWARD_CMD ="\xC1"
MOTOR_LEFT_BACKWARD_CMD ="\xC2"
MOTOR_RIGHT_FORWARD_CMD ="\xC5"
MOTOR_RIGHT_BACKWARD_CMD ="\xC6"

# The following commands are not in the above list because they are (in some
# way) not supported here.  For example, the LCD screen is not present on the
# kodama, so LCD screen related comments are not included.  SIGNATURE_CMD is not
# supported because it has a response consisting of character bytes, whereas
# all other commands have responses consisting of 2-byte sequences.
#CLEAR_LCD_CMD = "\xB7"
#PRINT_CMD = "\xB8"
#LCD_GOTO_XY_CMD = "\xB9"
#SIGNATURE_CMD = "\x81"

# Internally imposed speed to be sent to either motor.  Should be positive with
# a maximum possible value of 127.
MAX_SPEED = 40

class ThreePi:

    def __init__(self):
        self.gateway = SerialGateway()
        self.gateway.start()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.send_speeds(0, 0)
        self.gateway.stop()

    def _get_buffer_ints(self, byte_buffer):
        """Interpret the given byte buffer as containing pairs of two-byte
        ints.  So if the buffer contains 6 bytes, for example, we should
        return a list of 3 integer values.  In each two-byte pairs the least
        significant byte is sent first."""

        int_buffer = []
        n = len(byte_buffer)

        # The byte_buffer should contain an even number of items.
        assert n % 2 == 0

        for i in range(0, n, 2):
            least_sig = ord(byte_buffer[i])
            most_sig = ord(byte_buffer[i+1])
            number = most_sig * 256 + least_sig
            int_buffer.append(number)

        return int_buffer

    def send_speeds(self, leftSpeedProportion, rightSpeedProportion):
        """Sends the given speeds to the left and right motors.  These are
        specified as proportions of full speed where -1 is full-speed
        backwards, 0 is stopped, and +1 is full speed forwards."""
        if leftSpeedProportion >= 0:
            self.gateway.write(MOTOR_LEFT_FORWARD_CMD)
            self.send_speed_proportion(leftSpeedProportion)
        else:
            self.gateway.write(MOTOR_LEFT_BACKWARD_CMD)
            self.send_speed_proportion(-leftSpeedProportion)

        if rightSpeedProportion >= 0:
            self.gateway.write(MOTOR_RIGHT_FORWARD_CMD)
            self.send_speed_proportion(rightSpeedProportion)
        else:
            self.gateway.write(MOTOR_RIGHT_BACKWARD_CMD)
            self.send_speed_proportion(-rightSpeedProportion)

    def send_speed_proportion(self, value_from_minus_one_to_one):
        # First clamp in case values are too large.
        if value_from_minus_one_to_one > 1:
            value_from_minus_one_to_one = 1
        if value_from_minus_one_to_one < -1:
            value_from_minus_one_to_one = -1
        converted = int(MAX_SPEED * value_from_minus_one_to_one)
        #print("converted: {}".format(converted))
        self.gateway.write(chr(converted))

    def get_battery_voltage(self):
        self.gateway.clear_buffer()
        self.gateway.write(BATTERY_CMD)
        self.gateway.wait_for_buffer_fill(2)
        return self._get_buffer_ints(self.gateway.get_buffer())[0]

    def get_raw_sensors(self):
        self.gateway.clear_buffer()
        self.gateway.write(RAW_SENSORS_CMD)
        self.gateway.wait_for_buffer_fill(10)
        return self._get_buffer_ints(self.gateway.get_buffer())

    def get_calibrated_sensors(self):
        self.gateway.clear_buffer()
        self.gateway.write(CALIBRATED_SENSORS_CMD)
        self.gateway.wait_for_buffer_fill(10)
        return self._get_buffer_ints(self.gateway.get_buffer())

    def autocalibrate(self):
        self.gateway.clear_buffer()
        self.gateway.write(AUTOCALIBRATE_CMD)
        self.gateway.wait_for_buffer_fill(1)
        buffer_chr = self.gateway.get_buffer()[0]
        assert buffer_chr == 'c'

    def play_music(self, str):
        self.gateway.write(PLAY_MUSIC_CMD)
        n = len(str)
        self.gateway.write(chr(n))
        self.gateway.write(bytes(str))

    def play_c_major(self):
        self.play_music('!L16 V15 cdefgab>cbagfedc')

    def play_bach(self):
        self.play_music('!T240 L8 a gafaeada c+adaeafa >aa>bac#ada c#adaeaf4')

    def play_c_major(self):
        self.play_music('!L16 V15 cdefgab>cbagfedc')

    def play_happy_song(self):
        self.play_music('!L16 V10 cegb>c')

    def play_sad_song(self):
        self.play_music('!L16 V10 c<d<e<f')
