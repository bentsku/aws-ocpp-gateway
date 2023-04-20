import logging
import time
from urllib.parse import urlparse

import boto3
import paho.mqtt.client as mqtt
from mypy_boto3_iot.client import IoTClient

from secrets import token_hex

logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

session = boto3.Session(
    region_name="eu-central-1",  # TODO: make it configurable
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

iot_client: IoTClient = session.client("iot", endpoint_url="http://localhost:4566")

# get address
address = iot_client.describe_endpoint()["endpointAddress"]
broker_address = f"mqtt://{address}"

client_id = f"mqtt-monitor-{token_hex(8)}"

client = mqtt.Client(client_id=client_id)
client.enable_logger(logger=LOG)


def _on_connect(_client, userdata, flags, rc):
    LOG.info("Connected to the broker at %s", broker_address)
    mids = _client.subscribe([
        ("+/in", 1),
        ("+/out", 1),
    ])
    LOG.info("Subscribing to %s", mids)


def _on_message(_client, userdata, msg):
    try:
        LOG.info("Received MQTT message on topic: %s\n Payload: %s", msg.topic, msg.payload)
    except Exception as e:
        LOG.info('Unable to handle message from IoT MQTT topic "%s": %s', msg.topic, e)


def _on_subscribe(_client, userdata, mid, granted_qos):
    LOG.info("Subscribed to %s", mid)


client.on_connect = _on_connect
client.on_subscribe = _on_subscribe
client.on_message = _on_message

try:
    LOG.info("Starting the listener for %s", broker_address)
    parsed = urlparse(broker_address)
    client.connect(parsed.hostname, int(parsed.port))
    time.sleep(1)
    client.loop_forever()
except KeyboardInterrupt:
    LOG.info("Keyboard Interrupt: stopping the listener")
    client.disconnect()
