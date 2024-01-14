import time
import pycom
from network import WLAN
import machine
from mqtt import MQTTClient

# ----- Define Variables -----

# Network Credentials
WIFI_SSID = "Vodafone-2998D2"
PASSWORD = "GMkDV28KjDABFh37"

# Define ThingSpeak variables
THINGSPEAK_API_KEY = '74Z2BWQHJHOPFQCG'  # Replace with your ThingSpeak API key
THINGSPEAK_BASE_URL = 'https://api.thingspeak.com/update'
THINGSPEAK_CHANNEL_ID = '2402760'
THINGSPEAK_CLIENT_ID = 'GRwEKA8PGiAkDAMNEQoiFT0'
THINGSPEAK_MQTT_HOST = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PASSWORD = 'U0rTBfXygeELaHRtv7Pn4zEw'
THINGSPEAK_PUB_FIELD = 'field1'

last_distance = None

# ----- Define Pins -----

# Define the pins for TRIG and ECHO (Ultrasonic Sensor)
trig = machine.Pin('P12', mode=machine.Pin.OUT)
echo = machine.Pin('P11', mode=machine.Pin.IN)

# ----- Define Functions -----

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

# ----- WiFi Setup -----

# Initialize the WiFi interface and set antenna
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    wlan.ifconfig(config=('192.168.1.109', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

# Connect to the WiFi network
wlan.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, PASSWORD))

print("Connecting to Wifi...", end='')

# Wait until the device is connected to the WiFi network
while not wlan.isconnected():
    print(".", end='')
    time.sleep(1)

print("\nConnected to Wifi\n")
print(wlan.ifconfig())

# ----- ThingSpeak Setup (MQTT)-----

print("Connecting to ThingSpeak MQTT....")
# Define the MQTT client
client = MQTTClient(THINGSPEAK_CLIENT_ID, "mqtt3.thingspeak.com", port=1883, user=THINGSPEAK_CLIENT_ID, password=THINGSPEAK_MQTT_PASSWORD)
client.connect()

print("Connected to ThingSpeak MQTT\n")

while True:
    # Measure the distance
    distance = measure_distance()

    # Print the distance
    print("Distance: {} cm".format(distance))

    # Publish the distance to ThingSpeak
    client.publish(topic="channels/{:s}/publish/fields/{:s}".format(THINGSPEAK_CHANNEL_ID, THINGSPEAK_PUB_FIELD), msg=str(distance))

    # Wait 5 seconds
    time.sleep(5)