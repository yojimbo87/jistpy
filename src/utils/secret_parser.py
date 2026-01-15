from os import path
from configparser import ConfigParser

class Secret:
    def __init__(self, secret_file_path: str, credential_section: str) -> None:
        self.__parse_secret(secret_file_path, credential_section)
    
    def __parse_secret(self, secret_file_path: str, credential_section: str) -> None:
        thisfolder = path.dirname(path.abspath(__file__))
        initfile = path.join(thisfolder, "../" + secret_file_path)
        config = ConfigParser()
        config.read(initfile)

        self.hostname = config[credential_section]["hostname"]
        self.username = config[credential_section]["username"]
        self.password = config[credential_section]["password"]