from netmiko import ConnectHandler


class Netmiko(object):
    def __init__(self, device_type: str, hostname: str, username: str, password: str) -> None:
        self.device_config = {"device_type": device_type, "host": hostname, "username": username, "password": password}

    def send_config(self, commands: list) -> str:
        net_connect = ConnectHandler(**self.device_config)
        output = net_connect.send_config_set(commands)
        net_connect.save_config()
        return output

    def send_command(self, command: str) -> dict:
        net_connect = ConnectHandler(**self.device_config)
        return net_connect.send_command(command)
