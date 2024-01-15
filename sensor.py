from machine import Pin
import time

# Define default value if no object is detected
DEFAULT_DISTANCE = 200

# Define timeout in microseconds
TIMEOUT = 1_000_000

class Sensor:
    def __init__(self, trig_pin_number, echo_pin_number):
        self.trig = Pin(trig_pin_number, mode=Pin.OUT)
        self.echo = Pin(echo_pin_number, mode=Pin.IN)

    def measure_distance(self):
        # Send a 10us pulse.
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        # Start a timer
        start = time.ticks_us()

        # Wait for the pulse to be sent and return.
        while self.echo.value() == 0:
            if time.ticks_diff(time.ticks_us(), start) > TIMEOUT:
                return DEFAULT_DISTANCE # returned value is DEFAULT_DISTANCE (if no object is detected)

        pulse_start = time.ticks_us()

        # Wait for the pulse to return.
        while self.echo.value() == 1:
            if time.ticks_diff(time.ticks_us(), start) > TIMEOUT:
                return DEFAULT_DISTANCE # returned value is DEFAULT_DISTANCE (if no object is detected)
        pulse_end = time.ticks_us()

        # Calculate the distance in cm (sound travels at about 343m/s).
        distance = ((pulse_end - pulse_start) / 1_000_000) * 34300 / 2

        return distance
    
    def window_state(nb_sensors, sensor_1, sensor_2=0):
        if nb_sensors == 1:
            return sensor_1
        if sensor_1 == 0 and sensor_2 == 0:
            return 0
        elif sensor_1 == 1 and sensor_2 == 1:
            return 2
        else:
            return 1