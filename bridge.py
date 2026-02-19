import paho.mqtt.client as mqtt
from Adafruit_IO import Client
import json
import os

# Adafruit IO settings
ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")

# Meshtastic MQTT settings
MESH_BROKER = "mqtt.meshtastic.org"
MESH_USER = "meshdev"
MESH_PASS = "large4cats"
MESH_TOPIC = "msh/ANZ/2/json/LongFast/!91306040"

# Adafruit IO client
aio = Client(ADAFRUIT_USERNAME, ADAFRUIT_KEY)

def on_connect(client, userdata, flags, rc):
    print("Connected to Meshtastic MQTT")
    client.subscribe(MESH_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        if data.get("type") == "position":
            lat = data["payload"]["latitude_i"] / 10000000
            lon = data["payload"]["longitude_i"] / 10000000
            location = "{},{}".format(lat, lon)
            aio.send("location", location)
            print("Sent location: {}".format(location))
    except Exception as e:
        print("Error: {}".format(e))

client = mqtt.Client()
client.username_pw_set(MESH_USER, MESH_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MESH_BROKER, 1883, 60)
client.loop_forever()
