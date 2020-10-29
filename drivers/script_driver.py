import importlib
import re


class Script(object):
    def __init__(self, module_name: str) -> None:
        module_name = "scripts.{0}".format(re.sub(".py", "", module_name))
        self.run = getattr(importlib.import_module(module_name), "run")

    def execute(self, device_type: str, username: str, password: str) -> None:
        self.run(device_type, username, password)
