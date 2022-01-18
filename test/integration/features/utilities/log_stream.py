from datetime import datetime, timedelta
from os import getenv as get_env
from time import sleep
from boto3 import client
from datetime import datetime
from json import dumps
import json
from json.decoder import JSONDecodeError

lambda_client_logs = client("logs")
log_group_name_event_processor = get_env("LOG_GROUP_NAME_EVENT_PROCESSOR")
log_group_name_event_sender = get_env("LOG_GROUP_NAME_EVENT_SENDER")
event_processor = get_env("EVENT_PROCESSOR")
event_sender = get_env("EVENT_SENDER")


def get_processor_log_stream_name() -> str:
    sleep(1)
    log_stream = lambda_client_logs.describe_log_streams(
        logGroupName=log_group_name_event_processor,
        orderBy="LastEventTime",
        descending=True,
    )
    return log_stream["logStreams"][0]["logStreamName"]

def get_sender_log_stream_name() -> str:
    sleep(1)
    log_stream = lambda_client_logs.describe_log_streams(
        logGroupName=log_group_name_event_sender,
        orderBy="LastEventTime",
        descending=True,
    )
    return log_stream["logStreams"][0]["logStreamName"]

def get_logs(query: str) -> str:
    logs_found = False
    counter = 0
    while logs_found is False:
        start_query_response = lambda_client_logs.start_query(
            logGroupName=log_group_name_event_processor,
            startTime=int((datetime.today() - timedelta(minutes=5)).timestamp()),
            endTime=int(datetime.now().timestamp()),
            queryString=query
        )
        query_id = start_query_response['queryId']
        response = None
        while response == None or response['status'] != 'Complete':
            sleep(15)
            response = lambda_client_logs.get_query_results(
                queryId=query_id
            )
        counter +=1
        if response["results"] != []:
            logs_found = True
        elif counter == 6:
            raise Exception("Log search retries exceeded")
    return (dumps(response, indent=2))

def get_processor_logs_list_for_debug(seconds_ago: int=0) -> list:

    # Work out timestamps
    now = datetime.utcnow()
    past = now - timedelta(seconds=seconds_ago)

    # Get log events
    event_log = lambda_client_logs.get_log_events(
            logGroupName=log_group_name_event_processor,
            logStreamName=get_processor_log_stream_name(),
            startTime=int(past.timestamp() * 1000),
            endTime=int(now.timestamp() * 1000)
    )

    # If a message is a JSON string, format the string before returning.
    messages = []
    for event in event_log["events"]:
        try:
            messages.append(json.dumps(json.loads(event["message"]), indent=2))
        except JSONDecodeError:
            messages.append(event["message"])

    return messages

def get_processor_logs_within_time_frame_for_debug(time_in_seconds: int=0) -> dict:
    logs = get_processor_logs_list(time_in_seconds)
    # values = {}
    for m in logs:
        print(m)
        # values.append(m["message"])
