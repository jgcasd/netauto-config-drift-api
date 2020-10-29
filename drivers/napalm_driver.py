import napalm


class Napalm(object):
    def __init__(self, device_type: str, hostname: str, username: str, password: str) -> None:
        driver = napalm.get_network_driver(device_type)
        self.device = driver(hostname=hostname, username=username, password=password)

    def send_config(self, config_file: str) -> str:
        self.device.open()
        self.device.load_merge_candidate(filename=config_file)
        output = self.device.compare_config()
        self.device.commit_config()
        self.device.close()
        return output

    def send_command(self, command: str) -> dict:
        self.device.open()
        return self.device.cli([command])
