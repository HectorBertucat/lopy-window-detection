import time # for time.sleep()
import machine # for machine.deepsleep()
from network import connect_to_wifi, reconnect_to_wifi
from sensor import measure_distance
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

window_state = None

# ----- Initial setup -----
wlan = connect_to_wifi(WIFI_SSID, PASSWORD)
reconnect_to_wifi(wlan)

client = connect_to_thingspeak(THINGSPEAK_CLIENT_ID, THINGSPEAK_MQTT_HOST, THINGSPEAK_MQTT_PASSWORD)

while True:
    # Measure the distance
    distance = measure_distance()

    new_state = 0 if distance < THREESHOLD else 1
    
    if window_state is not None and window_state != new_state:
        print('Window has been ' + ('closed' if new_state == 0 else 'opened'))
        pub_to_thingspeak(new_state)
    else:
        print('No change in window state')

    if window_state is None:
        # Always publish the first state (in case of reboot)
        print('Sending first state: ' + ('closed' if new_state == 0 else 'opened'))
        pub_to_thingspeak(new_state)

    # Update the window state
    window_state = new_state

    # Wait x seconds (test purposes)
    time.sleep(5)

    # Put in deep sleep for 1 minute (in production to save battery)
    # machine.deepsleep(60000)