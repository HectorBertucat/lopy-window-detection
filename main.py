import machine
import time
import pycom

# Set the LED to red.
pycom.rgbled(0xFF0000)

# Define the pins for TRIG and ECHO
trig = machine.Pin('P12', mode=machine.Pin.OUT)
echo = machine.Pin('P11', mode=machine.Pin.IN)

def measure_distance():
    # Send a 10us pulse.
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Wait for the pulse to be sent and return.
    while echo.value() == 0:
        pass
    start = time.ticks_us()

    # Wait for the pulse to return.
    while echo.value() == 1:
        pass
    finish = time.ticks_us()

    # Calculate the distance in cm (sound travels at about 343m/s).
    distance = ((finish - start) / 1_000_000) * 34300 / 2

    return distance

while True:
    distance = measure_distance()
    if distance < 10: # 10cm
        print("Object is close!")
        # set led to white
        pycom.rgbled(0xFFFFFF)
    else:
        print("Object is far away.")
        # set led to red
        pycom.rgbled(0xFF0000)
    time.sleep(1)  # Wait for a second before the next measurement.