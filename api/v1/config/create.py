import json
from storage.dynamodb import DynamoDB
from pydantic import BaseModel
from enum import Enum
from pydantic.error_wrappers import ValidationError
from typing import List, Optional
from uuid import uuid4
import boto3
import os
import logging
import datetime
import pytz


logger = logging.getLogger()
logger.setLevel(logging.INFO)


sqs = boto3.client("sqs")
queue_url = os.getenv("config_worker", "")


database = DynamoDB(database="tasks")

headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True}


class Library(str, Enum):
    netmiko = "netmiko"
    napalm = "napalm"


class Task(BaseModel):
    device: str
    commands: List[str]
    library: Library
    task_id: Optional[str]
    status: Optional[str]
    enqueued_time: Optional[str]
    completed_time: Optional[str]


def create_task(message: dict) -> dict:
    return sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))


def generate_timestamp() -> str:
    d = datetime.datetime.utcnow()
    d_with_timezone = d.replace(tzinfo=pytz.UTC)
    d_with_timezone.isoformat()
    return str(d_with_timezone)


def app(event: dict, context: dict) -> dict:
    logger.info(event)

    user_data = json.loads(event["body"])

    try:
        task = Task(**user_data)
    except ValidationError as error:
        message = {"status": "failed", "message": json.loads(error.json())}
        return {"statusCode": 400, "body": json.dumps(message), "headers": headers}

    task.task_id = str(uuid4())
    task.status = "requested"
    task.enqueued_time = generate_timestamp()
    database.create(task.dict())
    create_task(task.dict())

    message = {"status": "success", "message": "request has been accepted", "task_id": task.task_id}
    return {"statusCode": 202, "body": json.dumps(message), "headers": headers}
