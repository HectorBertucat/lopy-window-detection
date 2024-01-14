import time
import pycom
from network import WLAN
import machine
import os

print("Starting the program...")

pycom.heartbeat(False)

# Define the network credentials
WIFI_SSID = "Vodafone-2998D2"
PASSWORD = "GMkDV28KjDABFh37"

# Define the pins for TRIG and ECHO
trig = machine.Pin('P12', mode=machine.Pin.OUT)
echo = machine.Pin('P11', mode=machine.Pin.IN)

# Initialize the WiFi interface
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, PASSWORD))

# Wait until the device is connected to the WiFi network
while not wlan.isconnected():
    machine.idle()

# Display a green led when the device is connected to the WiFi network
pycom.rgbled(0x00FF00)

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
    else:
        print("Object is far away.")
    time.sleep(1)  # Wait for a second before the next measurement.