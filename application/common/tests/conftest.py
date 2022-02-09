from pytest import fixture
import boto3
from moto import mock_dynamodb2
import os
import json

std_event_path = "event_processor/tests/STANDARD_EVENT.json"

with open(std_event_path, "r") as file:
    PHARMACY_STANDARD_EVENT = json.load(file)


@fixture
def change_event():
    change_event = PHARMACY_STANDARD_EVENT.copy()
    yield change_event


@fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["CHANGE_EVENTS_TABLE_NAME"] = "CHANGE_EVENTS_TABLE"
    os.environ["AWS_REGION"] = "us-east-2"


@fixture
def dynamodb_client(aws_credentials):
    with mock_dynamodb2():
        conn = boto3.client("dynamodb", region_name=os.environ["AWS_REGION"])
        yield conn


@fixture
def dead_letter_message():
    yield {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": "Test message.",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1545082649183",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1545082649185",
                },
                "messageAttributes": {
                    "ERROR_MESSAGE": {
                        "stringValue": "ApiDestination returned HTTP status 400 with payload: Dummy",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String",
                    },
                    "ERROR_CODE": {
                        "stringValue": "SDK_CLIENT_ERROR",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String",
                    },
                    "RULE_ARN": {
                        "stringValue": "arn:aws:events:eu:0:rule/dummy-eventbridge-bus/dummy-change-request-rule",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String",
                    },
                    "TARGET_ARN": {
                        "stringValue": "arn:aws:events:eu:0:api-destination/dummy-dos-api-gateway-api-destination/abc",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String",
                    },
                },
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:eventbridge-dlq-queue",
                "awsRegion": "us-east-2",
            }
        ]
    }
