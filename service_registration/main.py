from client import DockerSDKClient
from registry import MySQLRegistry
from registrator import Registrator
import yaml

if __name__ == "__main__":
    with open("config.yml", 'r') as conf_file:
        config = yaml.safe_load(conf_file)

        docker_client = DockerSDKClient()
        registry = MySQLRegistry(config['mysqlDB'])

        registrator = Registrator(docker_client, registry)

    registrator.start()
