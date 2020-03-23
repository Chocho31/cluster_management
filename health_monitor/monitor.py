from errors import CheckAlreadyExists, UnknownCheckTypeException, CheckConfigurationException, HealthCheckException
from utils import serialize_env, parse_period

class HealthMonitor:
	def __init__(self, docker_client, registry_client, scheduler, network):
		self.docker_client = docker_client
		self.registry_client = registry_client
		self.scheduler = scheduler
		self.network = network
		self.checkers = {}

	def start(self):
		containers = self.docker_client.get_containers()

		for container in containers:
			try:
				self.create_periodic_check(container)
			except CheckConfigurationException:
				continue

		for event in self.docker_client.get_events():
			if event["Type"] == "container":
				if event["status"] == "start":
					container = self.docker_client.get_container(event["id"])
					self.create_periodic_check(container)

				elif event["status"] == "stop":
					self.remove_periodic_check(event["id"])
		
	def checker_exists(self, check_type):
		return check_type in self.checkers

	def add_checker(self, check_type, func):
		if self.check_exists(check_type):
			raise CheckAlreadyExistsException(check_type)

		self.checkers[check_type] = func

	def remove_checker(self, check_type):
		if not self.check_exists(check_type):
			raise UnknownCheckTypeException(check_type)

		del self.checkers[check_type]

	def create_periodic_check(self, container):
		container_raw = container.attrs
		env = container_raw["Config"]["Env"]
		check_props = parse_env(env, 'HEALTH_CHECK_')

		if not check_props:
			raise CheckConfigurationException()

		# period is in time format such as 30s, 1m, 2hr
		# interval is period converted to integer,
		# representing the value of period in seconds
		period = check_props.pop('interval', '30s')
		interval = parse_period(period)

		self.scheduler.add_job(
			func=self.execute_check,
			args=[check_props, container.id],
			id=container.id,
			trigger='interval',
			seconds=interval
		)

	def remove_periodic_check(self, job_id):
		self.scheduler.remove_job(job_id)

	def execute_check(self, check_props, container_id):
		check_type = check_props.pop('type', None)

		if not check_type:
			raise CheckConfigurationException()

		if not checker_exists(check_type):
			raise UnknownCheckTypeException(check_type)

		check_handler = self.checkers.get(check_type)
		ip = self.docker_client.get_container_IP(container_id, self.network)
		port = self.docker_client.get_container_exposed_port(container_id)

		try:
			check_handler(ip, port, **check_props)
			print("check executed")

		except HealthCheckException:
			self.registry_client.deregister(container_id)