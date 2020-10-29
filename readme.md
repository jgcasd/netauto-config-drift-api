# NetAuto ConfigDrift API
A serverless API that allows network operators to manage their network.

# Motivation
This project serves as a demonstration of how to implement a highly-available, highly-scalable, low-cost,
serverless API for managing your network.

# Build Status

# Screenshots
![Send Command](https://github.com/jgcasd/netauto-config-drift-api/blob/main/docs/send_command_api.png)
![Task Output](https://github.com/jgcasd/netauto-config-drift-api/blob/main/docs/tasks_output_api.png)

# Code Style
* Code formatter: black
* Code Linting: flake8
* Max line length set to 119

# Tech/framework
* Python3.x
* Netmiko
* AWS API Gateway
* AWS SQS
* AWS SNS
* AWS Lambda
* AWS Secrets Manager

# Installation
* Ensure serverless framework has been installed
* Create a JSON formatted secret in secrets manager with your credentials:
```json
{
  "router_username": "admin",
  "router_password": "admin"
}
```
* Create config.yml in the root of your directory with the following parameters:
```yaml
secret_name: netauto-config-drift-api # name of your credentials in secrets manager
account_name: 01234567890 # aws account id
```
* Populate your device configs under configs/devices.yml
```yaml
# list of devices
router01:
  ip_address: 192.168.1.1
  device_type: cisco_ios
router02:
  ip_address: 192.168.1.2
  device_type: cisco_ios
```

* Create an .env file with your AWS credentials
```bash
AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXX
AWS_DEFAULT_REGION=us-west-2
```

* Deploy the code: ```make deploy```


# Sample Payloads
POST /api/v1/command:
```json
{
    "device": "router01",
    "command": "show ip route",
    "library": "netmiko"
}
```

RESPONSE:
```json
{
    "status": "success",
    "message": "request has been accepted",
    "task_id": "4aa78460-1214-4eee-a317-d6c08b9756d1"
}
```

GET /api/v1/tasks
```json
[
  {
    "completed_time": "2020-10-29 08:40:23.777350+00:00",
    "library": "netmiko",
    "enqueued_time": "2020-10-29 08:40:21.862726+00:00",
    "task_id": "c261696a-7210-41fd-b143-e46aefd138b5",
    "output": "Interface              IP-Address      OK? Method Status                Protocol\nGigabitEthernet1       192.168.100.162 YES DHCP   up                    up      \nLoopback0              unassigned      YES unset  up                    up      \nVirtualPortGroup0      192.168.35.101  YES TFTP   up                    up      ",
    "device": "router01",
    "status": "completed",
    "command": "show ip int bri"
  }
]
```


# Contribute
1) Install requirements: ```pip install flake8 black```
2) Fork this repository
3) Create a branch: ```git checkout -b <branch name>```
4) Make your changes and commit them: ```git commit -m <commit message>```
5) Push to the original branch: ```git push origin <project_name>/<location>```
6) Create the pull request.

# Todo
* Implement authentication and authorization
* Add support for retrieving device vars from external source (S3, DynamoDB, Netbox)
* Add support for running scripts or templates of configs
* Implement step functions to handle more complex workflows
* Improve error handling