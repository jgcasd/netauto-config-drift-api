from typing import List
import boto3

dynamodb = boto3.resource("dynamodb")


class DynamoDB(object):
    def __init__(self, database: str) -> None:
        self.table = dynamodb.Table(database)

    def create(self, data: dict) -> None:
        self.table.put_item(Item=data)

    def read(self, key: dict) -> dict:
        response = self.table.get_item(Key=key)
        return response["Item"]

    def update(self, data: dict) -> None:
        self.table.put_item(Item=data)

    def delete(self, key: dict) -> None:
        self.table.delete_item(Key=key)

    def list(self) -> List:
        response = self.table.scan()
        return response["Items"]
