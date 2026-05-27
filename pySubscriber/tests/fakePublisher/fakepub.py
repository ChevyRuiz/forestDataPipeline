import json
import math
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
QOS = 1

TOPIC_SAPFLOW = "cs/v1/data/cr1000x/24833/sapflow_table/cj"
TOPIC_DENDRO = "cs/v1/data/cr1000x/24833/dendrometer_table/cj"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT, 60)

def current_time_iso():
    return datetime.now().replace(microsecond=0).isoformat()

while True:

    current_time = current_time_iso()

    sapflow_payload = {
        "head": {
            "transaction": 0,
            "signature": 37333,
            "environment": {
                "station_name": "24833",
                "table_name": "sapflow_table",
                "model": "CR1000X",
                "serial_no": "24833",
                "os_version": "CR1000X.8.5.1",
                "prog_name": "CPU:dendro_sapflow_soil_v12052026.CR1X"
            },
            "fields": [
                {"name": "BattV_Min", "type": "xsd:float", "units": "Volts", "process": "Min", "settable": False},
                {"name": "PTemp_C", "type": "xsd:float", "units": "DegC", "process": "Smp", "settable": False},
                {"name": "PA_uS(1)", "type": "xsd:float", "units": "microseconds", "process": "Smp", "settable": False},
                {"name": "PA_uS(2)", "type": "xsd:float", "units": "microseconds", "process": "Smp", "settable": False},
                {"name": "VW(1)", "type": "xsd:float", "units": "%", "process": "Smp", "settable": False},
                {"name": "VW(2)", "type": "xsd:float", "units": "%", "process": "Smp", "settable": False},
                {"name": "sapflow(1)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False},
                {"name": "sapflow(2)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False},
                {"name": "sapflow(3)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False}
            ]
        },
        "data": [
            {
                "time": current_time,
                "vals": [
                    round(random.uniform(12.0, 12.8), 2),
                    round(random.uniform(10.0, 25.0), 2),
                    round(random.uniform(20.0, 35.0), 2),
                    round(random.uniform(20.0, 35.0), 2),
                    round(random.uniform(15.0, 40.0), 2),
                    round(random.uniform(15.0, 40.0), 2),
                    round(random.uniform(0.0, 500.0), 2),
                    round(random.uniform(0.0, 500.0), 2),
                    round(random.uniform(0.0, 500.0), 2)
                ]
            }
        ]
    }

    dendro_payload = {
        "head": {
            "transaction": 0,
            "signature": 45023,
            "environment": {
                "station_name": "24833",
                "table_name": "dendrometer_table",
                "model": "CR1000X",
                "serial_no": "24833",
                "os_version": "CR1000X.8.5.1",
                "prog_name": "CPU:dendro_sapflow_soil_v12052026.CR1X"
            },
            "fields": [
                {"name": "BattV_Min", "type": "xsd:float", "units": "Volts", "process": "Min", "settable": False},
                {"name": "dendro(1)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False},
                {"name": "dendro(2)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False},
                {"name": "dendro(3)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False},
                {"name": "dendro(4)", "type": "xsd:float", "units": "mV", "process": "Smp", "settable": False}
            ]
        },
        "data": [
            {
                "time": current_time,
                "vals": [
                    round(random.uniform(12.0, 12.8), 2),
                    round(random.uniform(300.0, 500.0), 2),
                    round(random.uniform(300.0, 500.0), 2),
                    round(random.uniform(300.0, 500.0), 2),
                    round(random.uniform(300.0, 500.0), 2)
                ]
            }
        ]
    }

    client.publish(
        TOPIC_SAPFLOW,
        json.dumps(sapflow_payload),
        qos=QOS
    )

    client.publish(
        TOPIC_DENDRO,
        json.dumps(dendro_payload),
        qos=QOS
    )

    print(f"[{current_time}] Published sapflow message")
    print(f"[{current_time}] Published dendrometer message")

    time.sleep(60)
