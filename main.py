import time # for time.sleep()
import machine # for machine.deepsleep()
from network import connect_to_wifi, reconnect_to_wifi
from sensor import Sensor
from thingspeak import connect_to_thingspeak, pub_to_thingspeak

# Network Credentials
WIFI_SSID = "Vodafone-2998D2"
PASSWORD = "GMkDV28KjDABFh37"

# Define ThingSpeak variables
# Statics
THINGSPEAK_BASE_URL = 'https://api.thingspeak.com/update'
THINGSPEAK_MQTT_HOST = 'mqtt3.thingspeak.com'
THINGSPEAK_PUB_FIELD = 'field1'

# Account MQTT credentials
THINGSPEAK_CLIENT_ID = 'GRwEKA8PGiAkDAMNEQoiFT0'
THINGSPEAK_MQTT_PASSWORD = 'U0rTBfXygeELaHRtv7Pn4zEw'

# Channel credentials
THINGSPEAK_CHANNEL_ID = '2402819'
THINGSPEAK_API_KEY = 'V1WGRM3WH4CZJSZW'  # Replace with your ThingSpeak API key

# Constants about calculation and logic
THREESHOLD = 4 # Value where window is considered opened (in cm)
NB_SENSORS = 1 # Number of sensors

# Define pin numbers for the sensors
# Pin are are like such :
# ECHO_PINS = [ECHO_SENSOR_1, ECHO_SENSOR_2]
# TRIG_PINS = [TRIG_SENSOR_1, TRIG_SENSOR_2]
ECHO_PINS = [11, 13]
TRIG_PINS = [12, 14]

# ----- Initial setup -----
sensors = [Sensor(TRIG_PINS[i], ECHO_PINS[i]) for i in range(NB_SENSORS)]

window_state = None

wlan = connect_to_wifi(WIFI_SSID, PASSWORD)
reconnect_to_wifi(wlan)

client = connect_to_thingspeak(THINGSPEAK_CLIENT_ID, THINGSPEAK_MQTT_HOST, THINGSPEAK_MQTT_PASSWORD)

# ----- Main loop -----

while True:
    new_states = [None for _ in range(NB_SENSORS)]
    for i in range(NB_SENSORS):
        # Measure the distance
        distance = sensors[i].measure_distance()

        # Define the new state
        new_states[i] = 0 if distance < THREESHOLD else 1

        # If we are in the last iteration, we check state changes
        if i == NB_SENSORS - 1:
            # Always publish the window state if it is None (in case of first launch or reboot)
            if window_state is None:
                window_state = sensors[i].window_state(NB_SENSORS, new_states[0], new_states[1] if NB_SENSORS == 2 else 0)
                pub_to_thingspeak(client, THINGSPEAK_CHANNEL_ID, THINGSPEAK_API_KEY, THINGSPEAK_PUB_FIELD, window_state)
            else:
                # If the window state is not None, we check new_window_state
                new_window_state = sensors[i].window_state(NB_SENSORS, new_states[0], new_states[1] if NB_SENSORS == 2 else 0)
                if new_window_state != window_state:
                    window_state = new_window_state
                    pub_to_thingspeak(client, THINGSPEAK_CHANNEL_ID, THINGSPEAK_API_KEY, THINGSPEAK_PUB_FIELD, window_state)

    # Wait x seconds (test purposes)
    time.sleep(5)

    # Put in deep sleep for 1 minute (in production to save battery)
    # machine.deepsleep(60000)