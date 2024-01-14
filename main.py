import machine
import time
import pycom
import network
import os

# Define the network credentials
WIFI_SSID = 'SSID'
PASSWORD = "PASSWORD"

# Define the pins for TRIG and ECHO
trig = machine.Pin('P12', mode=machine.Pin.OUT)
echo = machine.Pin('P11', mode=machine.Pin.IN)

# Initialize the WiFi interface
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Connect to the WiFi network
wifi.connect(WIFI_SSID, PASSWORD)

# Wait until the device is connected to the WiFi network
while not wifi.isconnected():
    time.sleep(1)
    # display a red led while waiting for the connection
    pycom.rgbled(0xFF0000)

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