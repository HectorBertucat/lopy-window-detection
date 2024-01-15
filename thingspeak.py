from MQTTClient import MQTTClient

def connect_to_thingspeak(client_id, mqtt_host, mqtt_password):
    print("Connecting to ThingSpeak MQTT....")
    client = MQTTClient(client_id, mqtt_host, port=1883, user=client_id, password=mqtt_password)
    client.connect()

    print("Connected to ThingSpeak MQTT\n")
    return client

def pub_to_thingspeak(client, state, channel_id, pub_field):
    # Publish the distance to ThingSpeak
    client.publish(topic="channels/{:s}/publish/fields/{:s}".format(channel_id, pub_field), msg=str(state))