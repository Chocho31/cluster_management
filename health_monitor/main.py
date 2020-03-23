from apscheduler.schedulers.background import BackgroundScheduler
from checks import http_check, tcp_check
from registry import MySQLRegistry
from client import DockerSDKClient
from monitor import HealthMonitor
import yaml

if __name__ == "__main__":
	with open("config.yml", 'r') as conf_file:
		config = yaml.safe_load(conf_file)
		print(config['mysqlDB'])
		docker_client = DockerSDKClient()
		scheduler = BackgroundScheduler()
		# registry = MySQLRegistry(config['mysqlDB'])
		network = config['network']

		health_monitor = HealthMonitor(docker_client, scheduler, network)
		health_monitor.add_checker('http', http_check)
		health_monitor.add_checker('tcp', tcp_check)

	health_monitor.start()
