from machine import Pin
import time

# Define default value if no object is detected
DEFAULT_DISTANCE = 200

# Define timeout in microseconds
TIMEOUT = 1_000_000

# Define the pins
trig = Pin('P12', mode=Pin.OUT)
echo = Pin('P11', mode=Pin.IN)

def measure_distance():
    # Send a 10us pulse.
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Start a timer
    start = time.ticks_us()

    # Wait for the pulse to be sent and return.
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start) > TIMEOUT:
            return DEFAULT_DISTANCE # returned value is DEFAULT_DISTANCE (if no object is detected)

    pulse_start = time.ticks_us()

    # Wait for the pulse to return.
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start) > TIMEOUT:
            return DEFAULT_DISTANCE # returned value is DEFAULT_DISTANCE (if no object is detected)
    pulse_end = time.ticks_us()

    # Calculate the distance in cm (sound travels at about 343m/s).
    distance = ((pulse_end - pulse_start) / 1_000_000) * 34300 / 2

    return distance