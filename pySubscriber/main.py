import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected successfully")
        client.subscribe("#", qos=1)

def on_message(client, userdata, message):
    print("----- MESSAGE RECEIVED -----")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload.decode(errors='ignore')}")
    print(f"QoS: {message.qos}")
    print()

mqttc = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="pySubscriber",
    clean_session=False
)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883) # Change ip address

mqttc.loop_forever()