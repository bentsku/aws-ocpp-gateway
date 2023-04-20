import boto3
# from mypy_boto3_iot.client import IoTClient
from mypy_boto3_iot_data.client import IoTDataPlaneClient

session = boto3.Session(
    region_name="eu-central-1",  # TODO: make it configurable
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# iot_client: IoTClient = session.client("iot", endpoint_url="http://localhost:4566")
iot_data_client: IoTDataPlaneClient = session.client("iot-data", endpoint_url="http://localhost:4566")

resp = iot_data_client.get_thing_shadow(thingName="CP1")
# resp = iot_data_client.get_thing_shadow(thingName="CP1", shadowName="classic")
print(resp["payload"].read())
