import json
from storage.dynamodb import DynamoDB

database = DynamoDB(database="tasks")

headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True}


def app(event: dict, context: dict) -> dict:
    return {"statusCode": 202, "body": json.dumps(database.list()), "headers": headers}
