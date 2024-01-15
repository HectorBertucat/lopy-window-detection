from network import WLAN
import machine
import time

# Define the static IP address
STATIC_IP = "192.168.1.100"
GATEWAY_IP = "192.168.1.1"
DNS = "8.8.8.8"

# Network Credentials
WIFI_SSID = "Vodafone-2998D2"
PASSWORD = "GMkDV28KjDABFh37"

def connect_to_wifi(ssid, password):
    print("Connecting to Wifi...", end='')
    wlan = WLAN(mode=WLAN.STA)
    wlan.antenna(WLAN.EXT_ANT)
    wlan.connect(ssid=ssid, auth=(WLAN.WPA2, password))

    while not wlan.isconnected():
        print(".", end='')
        time.sleep(1)

    print("\nConnected to Wifi\n")    
    return wlan

def reconnect_to_wifi(wlan):
    # If the device was not rebooted, set the static IP
    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.init(mode=WLAN.STA)
        wlan.ifconfig(config=(STATIC_IP, '255.255.255.0', GATEWAY_IP, DNS))