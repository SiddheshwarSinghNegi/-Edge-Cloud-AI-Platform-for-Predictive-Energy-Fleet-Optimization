import os, time, json, random
import paho.mqtt.client as mqtt

host = os.environ.get("MQTT_HOST","localhost")
port = int(os.environ.get("MQTT_PORT","1883"))
topic = "telemetry/ev"

client = mqtt.Client()
client.connect(host, port, 60)
client.loop_start()

print(f"[edge-simulator] publishing telemetry to mqtt://{host}:{port}/{topic}")

while True:
    payload = {
        "device_id": "ev-001",
        "ts": int(time.time()),
        "voltage": round(random.uniform(210, 240),1),
        "current": round(random.uniform(8, 32),1),
        "temp": round(random.uniform(20, 45),1),
        "status": random.choice(["idle","charging","fault"])
    }
    client.publish(topic, json.dumps(payload))
    time.sleep(3)
