import argparse

import boto3
from mypy_boto3_iot.client import IoTClient

session = boto3.Session(
    region_name="eu-central-1",  # TODO: make it configurable
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

iot_client: IoTClient = session.client("iot", endpoint_url="http://localhost:4566")


response = iot_client.create_thing(thingName="CP1")
response.pop("ResponseMetadata", None)
print(response)


if __name__ == '__main__':
    pass
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--thing-name", help="The Charge Point ID", required=True
    # )
