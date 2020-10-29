import logging
import json
import datetime
import pytz
from drivers.napalm_driver import Napalm
from drivers.netmiko_driver import Netmiko
from common.device_lookup import load_devices
from common.secrets_manager import get_secret
from storage.dynamodb import DynamoDB


logger = logging.getLogger()
logger.setLevel(logging.INFO)


database = DynamoDB(database="tasks")


def generate_timestamp() -> str:
    d = datetime.datetime.utcnow()
    d_with_timezone = d.replace(tzinfo=pytz.UTC)
    d_with_timezone.isoformat()
    return str(d_with_timezone)


def app(event: dict, context: dict) -> None:
    logger.info(event)

    credentials = json.loads(get_secret())
    devices = load_devices()

    for record in event["Records"]:
        logger.info(record["body"])

        data = json.loads(record["body"])
        device = devices.get(data["device"])

        data["status"] = "in_progress"
        database.update(data)

        if data["library"] == "netmiko":
            netmiko = Netmiko(
                **{
                    "device_type": device["device_type"],
                    "hostname": device["ip_address"],
                    "username": credentials["router_username"],
                    "password": credentials["router_password"],
                }
            )
            data["output"] = netmiko.send_command(data["command"])

        elif data["library"] == "napalm":
            napalm = Napalm(
                **{
                    "device_type": device["device_type"],
                    "hostname": device["ip_address"],
                    "username": credentials["router_username"],
                    "password": credentials["router_password"],
                }
            )
            data["output"] = napalm.send_command(data["command"])

        data["completed_time"] = generate_timestamp()
        data["status"] = "completed"
        database.update(data)
