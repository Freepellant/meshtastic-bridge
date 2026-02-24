import paho.mqtt.client as mqtt
import json
import os
import urllib.request

ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")

MESH_BROKER = "mqtt.meshtastic.org"
MESH_USER = "meshdev"
MESH_PASS = "large4cats"
MESH_TOPIC = "msh/ANZ/2/json/LongMod/#"

def send_to_adafruit(lat, lon):
    url = "https://io.adafruit.com/api/v2/{}/feeds/location/data".format(ADAFRUIT_USERNAME)
    payload = json.dumps({"value": "0", "lat": lat, "lon": lon}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "X-AIO-Key": ADAFRUIT_KEY,
        "Content-Type": "application/json"
    })
    urllib.request.urlopen(req)
    print("Sent location: {}, {}".format(lat, lon))

def on_connect(client, userdata, flags, rc):
    print("Connected to Meshtastic MQTT")
    client.subscribe(MESH_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        if data.get("type") == "position" and data.get("from") == 2435866688:
            lat = data["payload"]["latitude_i"] / 10000000
            lon = data["payload"]["longitude_i"] / 10000000
            send_to_adafruit(lat, lon)
    except Exception as e:
        print("Error: {}".format(e))

client = mqtt.Client()
client.username_pw_set(MESH_USER, MESH_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MESH_BROKER, 1883, 60)
client.loop_forever()



