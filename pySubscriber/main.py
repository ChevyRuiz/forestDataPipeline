import json
import math
import psycopg2
import paho.mqtt.client as mqtt
import os


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "forest_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def normalize_value(value):
    if isinstance(value, str) and value.upper() == "NAN":
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


def get_box_number(cursor, logger_serial_number):
    cursor.execute(
        """
        SELECT boxNumber
        FROM loggerBox
        WHERE loggerSerialNumber = %s
        """,
        (logger_serial_number,)
    )

    row = cursor.fetchone()
    return row[0] if row else None


def get_sensor_info(cursor, box_number, logger_var_name):
    cursor.execute(
        """
        SELECT stationCode, boxNumber, sensorNumber, sensorType
        FROM sensor
        WHERE boxNumber = %s
          AND loggerVarName = %s
        """,
        (box_number, logger_var_name)
    )

    return cursor.fetchone()


def insert_measurement(cursor, measured_at, sensor_info, field_name, value, unit):
    station_code, box_number, sensor_number, sensor_type = sensor_info

    cursor.execute(
        """
        INSERT INTO measurement (
            measured_at,
            stationCode,
            boxNumber,
            sensorNumber,
            sensorType,
            fieldName,
            value,
            unit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (
            measured_at,
            stationCode,
            boxNumber,
            sensorNumber,
            sensorType,
            fieldName
        )
        DO UPDATE SET
            value = EXCLUDED.value,
            unit = EXCLUDED.unit,
            receivedAt = now()
        """,
        (
            measured_at,
            station_code,
            box_number,
            sensor_number,
            sensor_type,
            field_name,
            value,
            unit,
        )
    )


def handle_payload(payload):
    conn = get_db_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                environment = payload["head"]["environment"]
                fields = payload["head"]["fields"]
                data_rows = payload["data"]

                logger_serial_number = environment["serial_no"]

                box_number = get_box_number(cursor, logger_serial_number)

                if box_number is None:
                    print(f"No box found for logger serial number {logger_serial_number}", flush=True)
                    return

                for data_row in data_rows:
                    measured_at = data_row["time"]
                    values = data_row["vals"]

                    for field, raw_value in zip(fields, values):
                        field_name = field["name"]
                        unit = field.get("units", "")
                        value = normalize_value(raw_value)

                        if value is None:
                            print(f"Skipping {field_name}: value is NAN/null", flush=True)
                            continue

                        sensor_info = get_sensor_info(cursor, box_number, field_name)

                        if sensor_info is None:
                            print(f"Skipping {field_name}: no matching sensor in DB", flush=True)
                            continue

                        insert_measurement(
                            cursor,
                            measured_at,
                            sensor_info,
                            field_name,
                            value,
                            unit
                        )

                        print(f"Inserted {field_name} = {value} {unit} at {measured_at}", flush=True)

    finally:
        conn.close()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}", flush=True)
    else:
        print("Connected successfully", flush=True)
        client.subscribe(MQTT_TOPIC, qos=1)


def on_message(client, userdata, message):
    print("----- MESSAGE RECEIVED -----", flush=True)
    print(f"Topic: {message.topic}", flush=True)
    print(f"Payload size: {len(message.payload)} bytes", flush=True)

    try:
        payload = json.loads(message.payload.decode("utf-8"))
        handle_payload(payload)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", flush=True)
    except Exception as e:
        print(f"Error while processing message: {e}", flush=True)

    print()


mqttc = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="pySubscriberDocker",
    clean_session=False
)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(MQTT_BROKER, MQTT_PORT)
mqttc.loop_forever()
