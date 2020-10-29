import boto3
from botocore.exceptions import ClientError
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secret_name = os.getenv("secret_name", "")
region_name = os.getenv("region_name", "")


def get_secret() -> str:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logging.info("The requested secret " + secret_name + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            logging.info("The request was invalid due to:", e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            logging.info("The request had invalid params:", e)
    else:
        return get_secret_value_response["SecretString"]

    raise Exception
